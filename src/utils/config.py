"""Configuration management utilities."""

import json
from pathlib import Path
from typing import Dict, Any


def load_config() -> Dict[str, Any]:
    """Load configuration from settings.json file.
    
    Returns:
        Dict containing configuration settings
    """
    config_path = Path(__file__).parent.parent.parent / "config" / "settings.json"
    
    try:
        with open(config_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file not found at {config_path}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in configuration file: {e}")


def get_api_config() -> Dict[str, Any]:
    """Get API configuration settings.
    
    Returns:
        Dict containing API configuration
    """
    config = load_config()
    return config.get("api", {})


def get_camera_config() -> Dict[str, Any]:
    """Get camera configuration settings.
    
    Returns:
        Dict containing camera configuration
    """
    config = load_config()
    return config.get("camera", {})


def get_qr_config() -> Dict[str, Any]:
    """Get QR code configuration settings.
    
    Returns:
        Dict containing QR code configuration
    """
    config = load_config()
    return config.get("qr", {
        "url_pattern": "https://lu.ma/check-in/"
    })
