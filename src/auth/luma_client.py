"""Luma API client for authentication and check-in operations."""

import requests
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
            payload = {"email": email, "password": password}
            
            debug("Signing in with password")
            response = requests.post(url, json=payload, headers=self.headers)
            response.raise_for_status()
            
            # Extract cookies from response
            cookies = {}
            for cookie in response.cookies:
                cookies[cookie.name] = cookie.value
                debug(f"Extracted cookie: {cookie.name}={cookie.value}")
            
            # Create proper cookie string (name=value pairs only)
            cookie_string = "; ".join([f"{name}={value}" for name, value in cookies.items()])
            
            if not cookie_string:
                error("No cookies found in response")
                return False
                
            debug(f"Extracted cookie string: {cookie_string[:50]}...")
            
            # Store the proper cookie string
            self.credentials_manager.save_cookie(cookie_string)
            
            info("Authentication successful with cookie saved")
            return True
            
        except Exception as e:
            exception(f"Authentication error: {e}")
            return False
    
    def check_in_to_event(self, event_api_id: str, proxy_key: str) -> bool:
        """Check in to a Luma event using stored raw cookie string.
        
        Args:
            event_api_id: Event API ID from QR code
            proxy_key: Proxy key from QR code
            
        Returns:
            True if check-in successful, False otherwise
        """
        try:
            debug(f"Attempting check-in for event {event_api_id} with proxy key {proxy_key}")
            
            # Load raw cookie string
            cookie_string = self.credentials_manager.load_cookie()
            if not cookie_string:
                warning("No cookie found")
                return False
            
            # Make get-guest request with cookie header
            url = f"{self.base_url}/event/admin/get-guest"
            params = {
                "event_api_id": event_api_id,
                "proxy_key": proxy_key
            }
            
            # Set cookie header directly
            headers = self.headers.copy()
            headers["Cookie"] = cookie_string
            
            debug(f"Making request to: {url}")
            debug(f"With params: {params}")
            debug(f"Using Cookie header: {cookie_string[:30]}...")
            
            response = requests.get(url, params=params, headers=headers)
            
            # Check for status codes before attempting to parse JSON
            if response.status_code == 401:
                warning("Authentication expired, credentials invalid")
                return False
            elif response.status_code == 404:
                warning("Guest not found - invalid QR code or guest not registered")
                return False
            
            # Verify response has content before parsing
            if not response.text:
                error("Empty response received from server")
                return False
            
            response.raise_for_status()
            
            # Parse response to check guest details
            guest_data = response.json()
            guest_info = guest_data.get("guest", {})
            
            info(f"✅ Guest found: {guest_info.get('name', 'Unknown')} ({guest_info.get('email', 'No email')})")
            
            # Check if guest has already checked in
            last_checked_in = guest_info.get("last_checked_in_at")
            if last_checked_in:
                info(f"ℹ️ Guest already checked in at: {last_checked_in}")
            else:
                info("✅ New check-in detected")
            
            return True
            
        except requests.exceptions.JSONDecodeError as e:
            error(f"Invalid JSON response: {e}")
            error(f"Response text: {response.text[:100]}")  # Log part of the response
            return False
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
