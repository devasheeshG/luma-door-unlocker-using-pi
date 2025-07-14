"""QR code detection and scanning functionality using OpenCV and pyzbar."""

import cv2
import time
import numpy as np
from pyzbar import pyzbar
from typing import Optional, Callable
import threading
import urllib.parse
from src.utils.config import get_camera_config, get_qr_config
from src.utils.logger import info, error, warning, debug, exception


class QRScanner:
    """QR code scanner using camera input with improved detection."""
    
    def __init__(self):
        """Initialize QR scanner with camera configuration."""
        self.camera_config = get_camera_config()
        self.qr_config = get_qr_config()
        self.camera = None
        self.is_running = False
        self.scan_thread = None
        self.last_detected_qr = None
        self.last_detection_time = 0
        self.duplicate_threshold = self.qr_config.get("duplicate_threshold", 3)  # seconds to ignore duplicate QR codes
        debug("QR Scanner initialized")
        
    def initialize_camera(self) -> bool:
        """Initialize camera device with optimized settings.
        
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
            
            # Set camera properties for better QR detection
            frame_width = self.camera_config.get("frame_width", 1280)
            frame_height = self.camera_config.get("frame_height", 720)
            
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)
            self.camera.set(cv2.CAP_PROP_AUTOFOCUS, 1)
            
            info(f"Camera initialized successfully on device {device_index} ({frame_width}x{frame_height})")
            return True
            
        except Exception as e:
            exception(f"Error initializing camera: {e}")
            return False
    
    def preprocess_frame(self, frame: np.ndarray) -> list:
        """Preprocess frame with multiple techniques for better QR detection.
        
        Args:
            frame: Input frame from camera
            
        Returns:
            List of processed frames to try for QR detection
        """
        processed_frames = []
        
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            processed_frames.append(gray)
            
            # Gaussian blur to reduce noise
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            processed_frames.append(blurred)
            
            # Adaptive threshold for better contrast
            adaptive_thresh = cv2.adaptiveThreshold(
                gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
            )
            processed_frames.append(adaptive_thresh)
            
            # Histogram equalization
            equalized = cv2.equalizeHist(gray)
            processed_frames.append(equalized)
            
            return processed_frames
            
        except Exception as e:
            exception(f"Error preprocessing frame: {e}")
            return [cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)]  # Fallback
    
    def scan_qr_code(self, frame) -> Optional[str]:
        """Scan for QR codes using multiple detection strategies.
        
        Args:
            frame: Camera frame to scan
            
        Returns:
            QR code data if found, None otherwise
        """
        try:
            # Get multiple processed versions of the frame
            processed_frames = self.preprocess_frame(frame)
            
            for i, processed_frame in enumerate(processed_frames):
                try:
                    qr_codes = pyzbar.decode(processed_frame)
                    
                    if qr_codes:
                        debug(f"QR codes found using preprocessing method {i}")
                        
                        for qr_code in qr_codes:
                            try:
                                # Decode QR code data
                                qr_data = qr_code.data.decode('utf-8')
                                
                                # URL decode the data if it contains URL-encoded characters
                                if '%' in qr_data:
                                    original_qr_data = qr_data
                                    qr_data = urllib.parse.unquote(qr_data)
                                    debug(f"URL decoded QR code: {original_qr_data} → {qr_data}")
                                
                                # Check for duplicates
                                current_time = time.time()
                                if (self.last_detected_qr == qr_data and 
                                    current_time - self.last_detection_time < self.duplicate_threshold):
                                    debug(f"Ignoring duplicate QR code: {qr_data}")
                                    continue
                                
                                # Update last detection
                                self.last_detected_qr = qr_data
                                self.last_detection_time = current_time
                                
                                # Check if QR code matches expected Luma format
                                if self.is_valid_luma_qr(qr_data):
                                    info(f"Valid Luma QR code detected: {qr_data}")
                                    return qr_data
                                else:
                                    debug(f"Non-Luma QR code detected: {qr_data}")
                                    
                            except UnicodeDecodeError as e:
                                warning(f"Failed to decode QR code data: {e}")
                                continue
                                
                except Exception as e:
                    debug(f"Error in preprocessing method {i}: {e}")
                    continue
            
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
            
            # Handle both normal and URL-encoded question mark
            if "?pk=" in remaining:
                # Standard format
                event_id, query_params = remaining.split("?pk=", 1)
            elif "pk=" in remaining:
                # In case the question mark was already decoded
                parts = remaining.split("pk=", 1)
                # Extract event ID by removing any trailing characters
                event_id = parts[0].rstrip("?&")
                query_params = parts[1]
            else:
                debug("QR code missing proxy key parameter")
                return None, None
            
            # Get the proxy key (handle potential additional parameters)
            proxy_key = query_params.split("&")[0]
            
            debug(f"Extracted event_id: {event_id}, proxy_key: {proxy_key}")
            return event_id, proxy_key
            
        except Exception as e:
            exception(f"Error parsing QR code data: {e}")
            return None, None
    
    def start_scanning(self, qr_callback: Callable[[str, str, str], None]) -> None:
        """Start continuous QR code scanning with improved performance.
        
        Args:
            qr_callback: Callback function to call when QR code is detected
                        Parameters: (qr_data, event_api_id, proxy_key)
        """
        if not self.initialize_camera():
            error("Failed to initialize camera")
            return
        
        self.is_running = True
        
        info("Starting QR code scanning...")
        
        frame_count = 0
        successful_scans = 0
        
        try:
            while self.is_running:
                ret, frame = self.camera.read()
                
                if not ret or frame is None:
                    error("Could not read frame from camera")
                    time.sleep(0.1)
                    continue
                
                frame_count += 1
                
                # Skip some frames for performance (process every 3rd frame)
                if frame_count % 3 != 0:
                    continue
                
                # Scan for QR codes
                qr_data = self.scan_qr_code(frame)
                
                if qr_data:
                    event_id, proxy_key = self.extract_event_and_proxy_key(qr_data)
                    
                    if event_id and proxy_key:
                        successful_scans += 1
                        info(f"Processing QR code #{successful_scans} - Event: {event_id}")
                        qr_callback(qr_data, event_id, proxy_key)
                    else:
                        warning("Failed to parse event ID and proxy key from QR code")
                
        except KeyboardInterrupt:
            info("Scanning interrupted by user")
        except Exception as e:
            exception(f"Error during scanning: {e}")
        finally:
            info(f"Scan complete. Processed {frame_count} frames, found {successful_scans} valid QR codes")
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
