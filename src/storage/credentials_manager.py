"""Credentials management for storing and retrieving Luma auth tokens."""

import json
import os
from pathlib import Path
from typing import Optional, Dict, Any
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
    
    def save_credentials(self, auth_session_key: str, user_id: str, 
                        additional_data: Optional[Dict[str, Any]] = None) -> None:
        """Save authentication credentials to file.
        
        Args:
            auth_session_key: Luma auth session key
            user_id: User API ID
            additional_data: Additional credential data to store
        """
        credentials = {
            "auth_session_key": auth_session_key,
            "user_id": user_id
        }
        
        if additional_data:
            credentials.update(additional_data)
        
        try:
            debug("Saving credentials to file")
            with open(self.credentials_path, 'w') as file:
                json.dump(credentials, file, indent=2)
            info("Credentials saved successfully")
        except Exception as e:
            exception(f"Failed to save credentials: {e}")
            raise RuntimeError(f"Failed to save credentials: {e}")
    
    def load_credentials(self) -> Optional[Dict[str, Any]]:
        """Load authentication credentials from file.
        
        Returns:
            Dict containing credentials or None if file doesn't exist
        """
        if not self.credentials_path.exists():
            debug("Credentials file does not exist")
            return None
        
        try:
            debug("Loading credentials from file")
            with open(self.credentials_path, 'r') as file:
                credentials = json.load(file)
            debug("Credentials loaded successfully")
            return credentials
        except json.JSONDecodeError as e:
            error(f"Invalid JSON in credentials file: {e}")
            raise ValueError(f"Invalid JSON in credentials file: {e}")
        except Exception as e:
            exception(f"Failed to load credentials: {e}")
            raise RuntimeError(f"Failed to load credentials: {e}")
    
    def get_auth_session_key(self) -> Optional[str]:
        """Get the auth session key from stored credentials.
        
        Returns:
            Auth session key or None if not found
        """
        credentials = self.load_credentials()
        auth_key = credentials.get("auth_session_key") if credentials else None
        debug(f"Auth session key {'found' if auth_key else 'not found'}")
        return auth_key
    
    def has_valid_credentials(self) -> bool:
        """Check if valid credentials exist.
        
        Returns:
            True if credentials file exists and contains required fields
        """
        credentials = self.load_credentials()
        if not credentials:
            debug("No credentials found")
            return False
        
        required_fields = ["auth_session_key", "user_id"]
        has_valid = all(field in credentials for field in required_fields)
        debug(f"Credentials validation: {has_valid}")
        return has_valid
    
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
