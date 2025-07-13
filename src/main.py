"""Main application entry point for Luma door unlocker."""

import signal
import sys
import os
from pathlib import Path

# Add project root to Python path for imports
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.camera.qr_scanner import QRScanner
from src.auth.luma_client import LumaClient
from src.utils.logger import info, error, warning


class LumaDoorUnlocker:
    """Main application class for Luma door unlocker."""
    
    def __init__(self, email: str, password: str):
        """Initialize the door unlocker application.
        
        Args:
            email: Luma account email
            password: Luma account password
        """
        self.email = email
        self.password = password
        self.qr_scanner = QRScanner()
        self.luma_client = LumaClient()
        self.is_running = False
    
    def handle_qr_detection(self, qr_data: str, event_api_id: str, proxy_key: str) -> None:
        """Handle QR code detection and perform check-in.
        
        Args:
            qr_data: Full QR code data
            event_api_id: Event API ID extracted from QR code
            proxy_key: Proxy key extracted from QR code
        """
        info("=== QR Code Detected ===")
        info(f"QR Data: {qr_data}")
        info(f"Event ID: {event_api_id}")
        info(f"Proxy Key: {proxy_key}")
        
        # Perform check-in flow
        success = self.luma_client.handle_check_in_flow(
            event_api_id=event_api_id,
            proxy_key=proxy_key,
            email=self.email,
            password=self.password
        )
        
        if success:
            info("✅ Check-in succeeded")
        else:
            error("❌ Check-in failed")
        
        info("======================")
    
    def setup_signal_handlers(self) -> None:
        """Setup signal handlers for graceful shutdown."""
        def signal_handler(signum, frame):
            warning("Shutdown signal received, stopping application...")
            self.stop()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
    def start(self) -> None:
        """Start the door unlocker application."""
        info("Starting Luma Door Unlocker...")
        info(f"Configured for user: {self.email}")
        
        self.setup_signal_handlers()
        self.is_running = True
        
        # Start QR code scanning
        try:
            self.qr_scanner.start_scanning(self.handle_qr_detection)
        except Exception as e:
            error(f"Error starting QR scanner: {e}")
            self.stop()
    
    def stop(self) -> None:
        """Stop the door unlocker application."""
        info("Stopping Luma Door Unlocker...")
        self.is_running = False
        self.qr_scanner.stop_scanning()
        info("Application stopped")


def main():
    """Main entry point for the application."""
    # Check for environment variables first
    email = os.getenv("LUMA_EMAIL")
    password = os.getenv("LUMA_PASSWORD")
    
    if not email or not password:
        error("LUMA_EMAIL and LUMA_PASSWORD environment variables must be set")
        error("Please set your credentials:")
        error("  export LUMA_EMAIL='your-email@example.com'")
        error("  export LUMA_PASSWORD='your-password'")
        sys.exit(1)
    
    # Create and start the application
    app = LumaDoorUnlocker(email, password)
    app.start()


if __name__ == "__main__":
    main()
