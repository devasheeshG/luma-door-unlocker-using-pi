"""Luma API client for authentication and check-in operations."""

import requests
import json
from src.utils.config import get_api_config
from src.storage.credentials_manager import CredentialsManager
from src.utils.logger import info, error, warning, debug, exception


class LumaClient:
    """Client for interacting with Luma API."""
    
    def __init__(self):
        """Initialize Luma API client."""
        self.api_config = get_api_config()
        self.base_url = self.api_config.get("base_url", "https://api.lu.ma")
        self.headers = self.api_config.get("headers", {})
        self.credentials_manager = CredentialsManager()
        debug("Luma API client initialized")
    
    def authenticate(self, email: str, password: str) -> bool:
        """Authenticate with Luma and store raw cookie string.
        
        Args:
            email: User email address
            password: User password
            
        Returns:
            True if authentication successful, False otherwise
        """
        try:
            info(f"Starting authentication for {email}")
            
            # Sign in with password
            url = f"{self.base_url}/auth/sign-in-with-password"
            payload = json.dumps({
                "email": email,
                "password": password
            })
            
            debug("Signing in with password")
            response = requests.request("POST", url, headers=self.headers, data=payload)
            
            if response.status_code != 200:
                error(f"Authentication failed with status code {response.status_code}")
                return False
            
            # Extract cookies from response
            all_cookies = response.cookies.get_dict()
            cookie_string = "; ".join([f"{name}={value}" for name, value in all_cookies.items()])
            
            debug(f"Authentication successful, got {len(all_cookies)} cookies")
            for name, value in all_cookies.items():
                debug(f"Extracted cookie: {name}={value[:20]}..." if len(value) > 20 else f"Extracted cookie: {name}={value}")
            
            if not cookie_string:
                error("No cookies found in response")
                return False
                
            debug(f"Extracted cookie string: {cookie_string[:50]}...")
            
            # Store the cookie string
            self.credentials_manager.save_cookie(cookie_string)
            
            info("Authentication successful with cookie saved")
            return True
            
        except Exception as e:
            exception(f"Authentication error: {e}")
            return False
    
    def check_in_to_event(self, event_api_id: str, proxy_key: str) -> bool:
        """Check in to a Luma event using stored cookie string.
        
        Args:
            event_api_id: Event API ID from QR code
            proxy_key: Proxy key from QR code
            
        Returns:
            True if check-in successful, False otherwise
        """
        try:
            debug(f"Attempting check-in for event {event_api_id} with proxy key {proxy_key}")
            
            # Load cookie string
            cookie_string = self.credentials_manager.load_cookie()
            if not cookie_string:
                warning("No cookie found")
                return False
            
            # Prepare request
            url = f"{self.base_url}/event/admin/get-guest"
            query_params = f"?event_api_id={event_api_id}&proxy_key={proxy_key}"
            full_url = url + query_params
            
            debug(f"Making request to: {full_url}")
            debug(f"Using Cookie header: {cookie_string[:30]}...")
            
            # Make request using the approach from the example
            response = requests.request("GET", full_url, headers=self.headers, data={})
            
            # Handle response status codes
            if response.status_code == 401:
                warning("Authentication expired, credentials invalid")
                return False
            elif response.status_code == 404:
                warning("Guest not found - invalid QR code or guest not registered")
                return False
            elif response.status_code != 200:
                error(f"Unexpected status code: {response.status_code}")
                return False
            
            # Verify response has valid content before parsing
            try:
                guest_data = response.json()
                debug("Successfully parsed JSON response")
            except Exception as e:
                error(f"Failed to parse response as JSON: {e}")
                error(f"Response content: {response.text[:100]}...")
                return False
            
            guest_info = guest_data.get("guest", {})
            if not guest_info:
                warning("No guest information in response")
                return False
            
            info(f"✅ Guest found: {guest_info.get('name', 'Unknown')} ({guest_info.get('email', 'No email')})")
            
            # Check if guest has already checked in
            last_checked_in = guest_info.get("last_checked_in_at")
            if last_checked_in:
                info(f"ℹ️ Guest already checked in at: {last_checked_in}")
            else:
                info("✅ New check-in detected")
            
            return True
            
        except Exception as e:
            exception(f"Check-in error: {e}")
            return False
    
    def handle_check_in_flow(self, event_api_id: str, proxy_key: str, email: str, password: str) -> bool:
        """Handle complete check-in flow with authentication retry.
        
        Args:
            event_api_id: Event API ID from QR code
            proxy_key: Proxy key from QR code
            email: User email for re-authentication if needed
            password: User password for re-authentication if needed
            
        Returns:
            True if check-in successful, False otherwise
        """
        debug("Starting check-in flow")
        
        # Try check-in with existing cookie
        if self.credentials_manager.has_cookie():
            debug("Found existing cookie, attempting check-in")
            if self.check_in_to_event(event_api_id, proxy_key):
                return True
        
        # If check-in failed or no cookie, re-authenticate
        info("Re-authenticating due to invalid/missing cookie...")
        if not self.authenticate(email, password):
            error("Re-authentication failed")
            return False
        
        # Retry check-in with new cookie
        debug("Retrying check-in with new cookie")
        return self.check_in_to_event(event_api_id, proxy_key)
