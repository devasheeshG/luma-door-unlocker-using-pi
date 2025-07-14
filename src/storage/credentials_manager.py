"""Credentials management for storing and retrieving Luma auth tokens."""

import json
import os
from pathlib import Path
from typing import Optional
from src.utils.logger import info, error, warning, debug, exception


class CredentialsManager:
    """Manages storage and retrieval of Luma authentication credentials."""
    
    def __init__(self, credentials_file: str = "credentials.json"):
        """Initialize credentials manager.
        
        Args:
            credentials_file: Name of the credentials file
        """
        self.credentials_path = Path(__file__).parent.parent.parent / credentials_file
        debug(f"Credentials manager initialized with file: {self.credentials_path}")
    
    def save_cookie(self, cookie: str) -> None:
        """Save cookie string to file.
        
        Args:
            cookie: Raw cookie string from Set-Cookie header
        """
        credentials = {
            "cookie": cookie
        }
        
        try:
            debug("Saving cookie to file")
            with open(self.credentials_path, 'w') as file:
                json.dump(credentials, file, indent=2)
            info("Cookie saved successfully")
        except Exception as e:
            exception(f"Failed to save cookie: {e}")
            raise RuntimeError(f"Failed to save cookie: {e}")
    
    def load_cookie(self) -> Optional[str]:
        """Load cookie string from file.
        
        Returns:
            Cookie string or None if file doesn't exist
        """
        if not self.credentials_path.exists():
            debug("Credentials file does not exist")
            return None
        
        try:
            debug("Loading cookie from file")
            with open(self.credentials_path, 'r') as file:
                credentials = json.load(file)
            
            cookie = credentials.get("cookie")
            debug(f"Cookie {'found' if cookie else 'not found'}")
            return cookie
            
        except json.JSONDecodeError as e:
            error(f"Invalid JSON in credentials file: {e}")
            return None
        except Exception as e:
            exception(f"Failed to load cookie: {e}")
            return None
    
    def has_cookie(self) -> bool:
        """Check if cookie exists.
        
        Returns:
            True if credentials file exists and contains cookie
        """
        cookie = self.load_cookie()
        return cookie is not None and len(cookie) > 0
    
    def clear_credentials(self) -> None:
        """Remove the credentials file."""
        if self.credentials_path.exists():
            try:
                debug("Clearing credentials file")
                os.remove(self.credentials_path)
                info("Credentials cleared successfully")
            except Exception as e:
                exception(f"Failed to clear credentials: {e}")
                raise RuntimeError(f"Failed to clear credentials: {e}")
        else:
            debug("No credentials file to clear")
        credentials = self.load_credentials()
        if not credentials:
            debug("No credentials found")
            return False
        
        # Only check if we have cookie string
        has_cookie = "cookie" in credentials and len(credentials["cookie"]) > 0
        
        debug(f"Credentials validation - cookie: {has_cookie}")
        return has_cookie
    
    def clear_credentials(self) -> None:
        """Remove the credentials file."""
        if self.credentials_path.exists():
            try:
                debug("Clearing credentials file")
                os.remove(self.credentials_path)
                info("Credentials cleared successfully")
            except Exception as e:
                exception(f"Failed to clear credentials: {e}")
                raise RuntimeError(f"Failed to clear credentials: {e}")
        else:
            debug("No credentials file to clear")
