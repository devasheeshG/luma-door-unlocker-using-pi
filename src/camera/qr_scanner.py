"""QR code detection and scanning functionality using OpenCV and pyzbar."""

import cv2
import time
from pyzbar import pyzbar
from typing import Optional, Callable
import threading
from src.utils.config import get_camera_config, get_qr_config
from src.utils.logger import info, error, warning, debug, exception


class QRScanner:
    """QR code scanner using camera input."""
    
    def __init__(self):
        """Initialize QR scanner with camera configuration."""
        self.camera_config = get_camera_config()
        self.qr_config = get_qr_config()
        self.camera = None
        self.is_running = False
        self.scan_thread = None
        debug("QR Scanner initialized")
        
    def initialize_camera(self) -> bool:
        """Initialize camera device.
        
        Returns:
            True if camera initialized successfully, False otherwise
        """
        try:
            device_index = self.camera_config.get("device_index", 0)
            debug(f"Initializing camera on device {device_index}")
            self.camera = cv2.VideoCapture(device_index)
            
            if not self.camera.isOpened():
                error(f"Could not open camera device {device_index}")
                return False
            
            # Set camera properties
            frame_width = self.camera_config.get("frame_width", 640)
            frame_height = self.camera_config.get("frame_height", 480)
            
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)
            
            info(f"Camera initialized successfully on device {device_index} ({frame_width}x{frame_height})")
            return True
            
        except Exception as e:
            exception(f"Error initializing camera: {e}")
            return False
    
    def scan_qr_code(self, frame) -> Optional[str]:
        """Scan for QR codes in the given frame.
        
        Args:
            frame: Camera frame to scan
            
        Returns:
            QR code data if found, None otherwise
        """
        try:
            debug(f"Scanning frame at {time.time()}")
            
            # Convert frame to grayscale for better QR detection
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Detect QR codes
            qr_codes = pyzbar.decode(gray_frame)
            
            for qr_code in qr_codes:
                # Decode QR code data
                qr_data = qr_code.data.decode('utf-8')
                
                # Check if QR code matches expected Luma format
                if self.is_valid_luma_qr(qr_data):
                    debug(f"Valid Luma QR code detected: {qr_data}")
                    return qr_data
                else:
                    debug(f"Non-Luma QR code detected: {qr_data}")
            
            return None
            
        except Exception as e:
            exception(f"Error scanning QR code: {e}")
            return None
    
    def is_valid_luma_qr(self, qr_data: str) -> bool:
        """Check if QR code data matches Luma check-in format.
        
        Args:
            qr_data: QR code data string
            
        Returns:
            True if QR code is a valid Luma check-in QR code
        """
        url_pattern = self.qr_config.get("url_pattern", "https://lu.ma/check-in/")
        is_valid = qr_data.startswith(url_pattern) and "?pk=" in qr_data
        debug(f"QR code validation: {qr_data} -> {is_valid}")
        return is_valid
    
    def extract_event_and_proxy_key(self, qr_data: str) -> tuple[Optional[str], Optional[str]]:
        """Extract event ID and proxy key from QR code data.
        
        Args:
            qr_data: QR code data string
            
        Returns:
            Tuple of (event_api_id, proxy_key) or (None, None) if parsing fails
        """
        try:
            # Expected format: https://lu.ma/check-in/evt-6SAYBD09zCBjNNg?pk=g-r3DlcAelLjxttUG
            url_pattern = self.qr_config.get("url_pattern", "https://lu.ma/check-in/")
            
            if not qr_data.startswith(url_pattern):
                debug("QR code does not match expected URL pattern")
                return None, None
            
            # Remove base URL to get event ID and query params
            remaining = qr_data[len(url_pattern):]
            
            if "?pk=" not in remaining:
                debug("QR code missing proxy key parameter")
                return None, None
            
            # Split event ID and proxy key
            event_id, query_params = remaining.split("?pk=", 1)
            proxy_key = query_params.split("&")[0]  # Get first param in case there are multiple
            
            debug(f"Extracted event_id: {event_id}, proxy_key: {proxy_key}")
            return event_id, proxy_key
            
        except Exception as e:
            exception(f"Error parsing QR code data: {e}")
            return None, None
    
    def start_scanning(self, qr_callback: Callable[[str, str, str], None]) -> None:
        """Start continuous QR code scanning.
        
        Args:
            qr_callback: Callback function to call when QR code is detected
                        Parameters: (qr_data, event_api_id, proxy_key)
        """
        if not self.initialize_camera():
            error("Failed to initialize camera")
            return
        
        self.is_running = True
        # scan_interval = self.camera_config.get("scan_interval", 0.5)
        
        info("Starting QR code scanning...")
        # info(f"Scan interval: {scan_interval}s")
        
        try:
            while self.is_running:
                ret, frame = self.camera.read()
                
                if not ret:
                    error("Could not read frame from camera")
                    break
                
                # Scan for QR codes
                qr_data = self.scan_qr_code(frame)
                
                if qr_data:
                    event_id, proxy_key = self.extract_event_and_proxy_key(qr_data)
                    
                    if event_id and proxy_key:
                        debug(f"Processing QR code - Event: {event_id}, Proxy: {proxy_key}")
                        qr_callback(qr_data, event_id, proxy_key)
                    else:
                        warning("Failed to parse event ID and proxy key from QR code")
                
                # Wait before next scan
                # time.sleep(scan_interval)
                
        except KeyboardInterrupt:
            info("Scanning interrupted by user")
        except Exception as e:
            exception(f"Error during scanning: {e}")
        finally:
            self.stop_scanning()
    
    def start_scanning_async(self, qr_callback: Callable[[str, str, str], None]) -> None:
        """Start QR code scanning in a separate thread.
        
        Args:
            qr_callback: Callback function to call when QR code is detected
        """
        if self.scan_thread and self.scan_thread.is_alive():
            warning("Scanning already in progress")
            return
        
        self.scan_thread = threading.Thread(
            target=self.start_scanning, 
            args=(qr_callback,),
            daemon=True
        )
        self.scan_thread.start()
    
    def stop_scanning(self) -> None:
        """Stop QR code scanning and release camera."""
        self.is_running = False
        
        if self.camera:
            self.camera.release()
            self.camera = None
        
        info("QR code scanning stopped")
    
    def __del__(self):
        """Cleanup resources when object is destroyed."""
        self.stop_scanning()
