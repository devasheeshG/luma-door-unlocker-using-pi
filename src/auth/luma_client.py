"""Luma API client for authentication and check-in operations."""

import requests
from typing import Dict, Any, Optional
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
        self.session = requests.Session()
        
        # Set default headers
        self.session.headers.update(self.headers)
        debug("Luma API client initialized")
    
    def authenticate(self, email: str, password: str) -> bool:
        """Authenticate with Luma and store credentials.
        
        Args:
            email: User email address
            password: User password
            
        Returns:
            True if authentication successful, False otherwise
        """
        try:
            info(f"Starting authentication for {email}")
            
            # Sign in with password
            auth_response = self._sign_in_with_password(email, password)
            if not auth_response:
                error("Failed to sign in with password")
                return False
            
            # Extract auth session key from response cookies
            auth_session_key = self._extract_auth_session_key(auth_response)
            if not auth_session_key:
                error("Failed to extract auth session key")
                return False
            
            # Store credentials
            self.credentials_manager.save_credentials(
                auth_session_key=auth_session_key,
                user_id="",  # Will be populated when needed
                additional_data={"email": email}
            )
            
            info("Authentication successful")
            return True
            
        except Exception as e:
            exception(f"Authentication error: {e}")
            return False
    
    def _sign_in_with_password(self, email: str, password: str) -> Optional[requests.Response]:
        """Sign in with email and password.
        
        Args:
            email: User email address
            password: User password
            
        Returns:
            Response object or None if failed
        """
        try:
            url = f"{self.base_url}/auth/sign-in-with-password"
            payload = {"email": email, "password": password}
            
            debug("Signing in with password")
            response = self.session.post(url, json=payload)
            response.raise_for_status()
            
            debug("Password sign-in successful")
            return response
            
        except Exception as e:
            exception(f"Sign in error: {e}")
            return None
    
    def _extract_auth_session_key(self, response: requests.Response) -> Optional[str]:
        """Extract auth session key from response cookies.
        
        Args:
            response: HTTP response object
            
        Returns:
            Auth session key or None if not found
        """
        try:
            for cookie in response.cookies:
                if cookie.name == "luma.auth-session-key":
                    debug("Auth session key extracted successfully")
                    return cookie.value
            
            warning("Auth session key not found in response cookies")
            return None
            
        except Exception as e:
            exception(f"Error extracting auth session key: {e}")
            return None
    
    def check_in_to_event(self, event_api_id: str, proxy_key: str) -> bool:
        """Check in to a Luma event using the get-guest endpoint.
        
        Args:
            event_api_id: Event API ID from QR code
            proxy_key: Proxy key from QR code
            
        Returns:
            True if check-in successful, False otherwise
        """
        try:
            debug(f"Attempting check-in for event {event_api_id} with proxy key {proxy_key}")
            
            # Load credentials
            auth_session_key = self.credentials_manager.get_auth_session_key()
            if not auth_session_key:
                warning("No auth session key found")
                return False
            
            # Set auth cookie
            self.session.cookies.set("luma.auth-session-key", auth_session_key, domain=".lu.ma")
            
            # Make get-guest request to verify the guest exists (based on research)
            url = f"{self.base_url}/event/admin/get-guest"
            params = {
                "event_api_id": event_api_id,
                "proxy_key": proxy_key
            }
            
            response = self.session.get(url, params=params)
            
            if response.status_code == 401:
                warning("Authentication expired, credentials invalid")
                return False
            elif response.status_code == 404:
                warning("Guest not found - invalid QR code or guest not registered")
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
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                warning("Authentication expired")
                return False
            elif e.response.status_code == 404:
                warning("Guest not found")
                return False
            else:
                error(f"HTTP error during check-in: {e}")
                return False
        except Exception as e:
            exception(f"Check-in error: {e}")
            return False
    
    def validate_credentials(self) -> bool:
        """Validate stored credentials by making a test API call.
        
        Returns:
            True if credentials are valid, False otherwise
        """
        try:
            debug("Validating stored credentials")
            
            # Load credentials
            auth_session_key = self.credentials_manager.get_auth_session_key()
            if not auth_session_key:
                debug("No auth session key found for validation")
                return False
            
            # Set auth cookie
            self.session.cookies.set("luma.auth-session-key", auth_session_key, domain=".lu.ma")
            
            # Make a simple test request (adjust endpoint as needed)
            url = f"{self.base_url}/user/me"  # Assuming this endpoint exists
            response = self.session.get(url)
            
            is_valid = response.status_code != 401
            debug(f"Credential validation result: {is_valid}")
            return is_valid
            
        except Exception as e:
            exception(f"Credential validation error: {e}")
            return False
    
    def handle_check_in_flow(self, event_api_id: str, proxy_key: str, 
                           email: str, password: str) -> bool:
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
        
        # Try check-in with existing credentials
        if self.credentials_manager.has_valid_credentials():
            debug("Found existing credentials, attempting check-in")
            if self.check_in_to_event(event_api_id, proxy_key):
                return True
        
        # If check-in failed or no credentials, re-authenticate
        info("Re-authenticating due to invalid/missing credentials...")
        if not self.authenticate(email, password):
            error("Re-authentication failed")
            return False
        
        # Retry check-in with new credentials
        debug("Retrying check-in with new credentials")
        return self.check_in_to_event(event_api_id, proxy_key)
