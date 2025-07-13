"""QR code detection and scanning functionality using OpenCV and pyzbar."""

import cv2
import time
import numpy as np
from pyzbar import pyzbar
from typing import Optional, Callable, List, Tuple
import threading
from src.utils.config import get_camera_config, get_qr_config
from src.utils.logger import info, error, warning, debug, exception


class QRScanner:
    """Advanced QR code scanner using camera input with improved detection."""
    
    def __init__(self):
        """Initialize QR scanner with camera configuration."""
        self.camera_config = get_camera_config()
        self.qr_config = get_qr_config()
        self.camera = None
        self.is_running = False
        self.scan_thread = None
        self.last_detected_qr = None
        self.last_detection_time = 0
        self.duplicate_threshold = 2.0  # seconds to ignore duplicate QR codes
        debug("QR Scanner initialized")
        
    def initialize_camera(self) -> bool:
        """Initialize camera device with optimized settings.
        
        Returns:
            True if camera initialized successfully, False otherwise
        """
        try:
            device_index = self.camera_config.get("device_index", 0)
            debug(f"Initializing camera on device {device_index}")
            
            # Try different backends for better compatibility
            backends = [cv2.CAP_V4L2, cv2.CAP_GSTREAMER, cv2.CAP_ANY]
            
            for backend in backends:
                self.camera = cv2.VideoCapture(device_index, backend)
                if self.camera.isOpened():
                    debug(f"Camera opened successfully with backend {backend}")
                    break
                else:
                    debug(f"Failed to open camera with backend {backend}")
            
            if not self.camera or not self.camera.isOpened():
                error(f"Could not open camera device {device_index}")
                return False
            
            # Set camera properties for better QR detection
            frame_width = self.camera_config.get("frame_width", 640)
            frame_height = self.camera_config.get("frame_height", 480)
            fps = self.camera_config.get("fps", 30)
            
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)
            self.camera.set(cv2.CAP_PROP_FPS, fps)
            self.camera.set(cv2.CAP_PROP_AUTOFOCUS, 1)
            self.camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)  # Enable auto exposure
            
            # Verify settings
            actual_width = int(self.camera.get(cv2.CAP_PROP_FRAME_WIDTH))
            actual_height = int(self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
            actual_fps = int(self.camera.get(cv2.CAP_PROP_FPS))
            
            info(f"Camera initialized: {actual_width}x{actual_height} @ {actual_fps}fps")
            
            # Test frame capture
            ret, test_frame = self.camera.read()
            if not ret or test_frame is None:
                error("Failed to capture test frame")
                return False
            
            debug(f"Test frame captured: shape={test_frame.shape}")
            return True
            
        except Exception as e:
            exception(f"Error initializing camera: {e}")
            return False
    
    def preprocess_frame(self, frame: np.ndarray) -> List[np.ndarray]:
        """Preprocess frame with multiple techniques for better QR detection.
        
        Args:
            frame: Input frame from camera
            
        Returns:
            List of processed frames to try for QR detection
        """
        processed_frames = []
        
        try:
            # Original grayscale
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
            
            # Histogram equalization for better lighting
            equalized = cv2.equalizeHist(gray)
            processed_frames.append(equalized)
            
            # Morphological operations to clean up
            kernel = np.ones((3, 3), np.uint8)
            morphed = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel)
            processed_frames.append(morphed)
            
            # Edge enhancement
            laplacian = cv2.Laplacian(gray, cv2.CV_8U)
            enhanced = cv2.add(gray, laplacian)
            processed_frames.append(enhanced)
            
            debug(f"Generated {len(processed_frames)} processed frames")
            return processed_frames
            
        except Exception as e:
            exception(f"Error preprocessing frame: {e}")
            return [cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)]  # Fallback to basic grayscale
    
    def scan_qr_code(self, frame: np.ndarray) -> Optional[str]:
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
                    # Try different pyzbar settings
                    qr_codes = pyzbar.decode(processed_frame)
                    
                    if qr_codes:
                        debug(f"QR codes found using preprocessing method {i}")
                        
                        for qr_code in qr_codes:
                            try:
                                # Decode QR code data
                                qr_data = qr_code.data.decode('utf-8')
                                
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
                                    
                                    # Log QR code position for debugging
                                    rect = qr_code.rect
                                    debug(f"QR code position: x={rect.left}, y={rect.top}, w={rect.width}, h={rect.height}")
                                    
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
        try:
            url_pattern = self.qr_config.get("url_pattern", "https://lu.ma/check-in/")
            
            # Basic format check
            if not qr_data.startswith(url_pattern):
                debug(f"QR code doesn't start with expected pattern: {url_pattern}")
                return False
            
            if "?pk=" not in qr_data:
                debug("QR code missing proxy key parameter")
                return False
            
            # More detailed validation
            remaining = qr_data[len(url_pattern):]
            if not remaining:
                debug("QR code has no content after URL pattern")
                return False
            
            # Check event ID format (should start with 'evt-')
            event_part = remaining.split("?pk=")[0]
            if not event_part.startswith("evt-"):
                debug(f"Event ID doesn't start with 'evt-': {event_part}")
                return False
            
            # Check proxy key format (should start with 'g-')
            proxy_part = remaining.split("?pk=")[1].split("&")[0]
            if not proxy_part.startswith("g-"):
                debug(f"Proxy key doesn't start with 'g-': {proxy_part}")
                return False
            
            debug(f"QR code validation passed: {qr_data}")
            return True
            
        except Exception as e:
            debug(f"Error validating QR code: {e}")
            return False
    
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
        """Start continuous QR code scanning with improved frame handling.
        
        Args:
            qr_callback: Callback function to call when QR code is detected
                        Parameters: (qr_data, event_api_id, proxy_key)
        """
        if not self.initialize_camera():
            error("Failed to initialize camera")
            return
        
        self.is_running = True
        scan_interval = self.camera_config.get("scan_interval", 0.1)  # Faster scanning
        frame_skip = self.camera_config.get("frame_skip", 2)  # Skip frames for performance
        
        info("Starting QR code scanning...")
        info(f"Scan interval: {scan_interval}s, Frame skip: {frame_skip}")
        
        frame_count = 0
        successful_scans = 0
        
        try:
            while self.is_running:
                ret, frame = self.camera.read()
                
                if not ret or frame is None:
                    error("Could not read frame from camera")
                    time.sleep(0.1)  # Brief pause before retrying
                    continue
                
                frame_count += 1
                
                # Skip frames for performance
                if frame_count % (frame_skip + 1) != 0:
                    continue
                
                # Check frame quality
                if frame.size == 0:
                    warning("Received empty frame")
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
                
                # Wait before next scan
                time.sleep(scan_interval)
                
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
            qr_callback: Callable function to process the QR code data
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
        
        cv2.destroyAllWindows()
        info("QR code scanning stopped")
    
    def __del__(self):
        """Cleanup resources when object is destroyed."""
        self.stop_scanning()
