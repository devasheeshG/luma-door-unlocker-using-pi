"""Centralized logging utility for the Luma door unlocker application."""

import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional


class LumaLogger:
    """Centralized logger for the application."""
    
    _instance: Optional['LumaLogger'] = None
    _logger: Optional[logging.Logger] = None
    
    def __new__(cls) -> 'LumaLogger':
        """Singleton pattern to ensure one logger instance."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize the logger if not already initialized."""
        if self._logger is None:
            self._setup_logger()
    
    def _setup_logger(self) -> None:
        """Setup logger with file and console handlers."""
        # Create logger
        self._logger = logging.getLogger('luma_door_unlocker')
        self._logger.setLevel(logging.DEBUG)
        
        # Prevent duplicate handlers
        if self._logger.handlers:
            return
        
        # Create logs directory
        logs_dir = Path(__file__).parent.parent.parent / "logs"
        logs_dir.mkdir(exist_ok=True)
        
        # Create log filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = logs_dir / f"{timestamp}.log"
        
        # Create formatters
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(funcName)s:%(lineno)d - %(message)s'
        )
        console_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        )
        
        # Create file handler
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(file_formatter)
        
        # Create console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(console_formatter)
        
        # Add handlers to logger
        self._logger.addHandler(file_handler)
        self._logger.addHandler(console_handler)
        
        # Log startup message
        self._logger.info(f"Logging initialized - Log file: {log_file}")
    
    def get_logger(self) -> logging.Logger:
        """Get the logger instance."""
        return self._logger
    
    def debug(self, message: str) -> None:
        """Log debug message."""
        self._logger.debug(message)
    
    def info(self, message: str) -> None:
        """Log info message."""
        self._logger.info(message)
    
    def warning(self, message: str) -> None:
        """Log warning message."""
        self._logger.warning(message)
    
    def error(self, message: str) -> None:
        """Log error message."""
        self._logger.error(message)
    
    def critical(self, message: str) -> None:
        """Log critical message."""
        self._logger.critical(message)
    
    def exception(self, message: str) -> None:
        """Log exception with traceback."""
        self._logger.exception(message)


# Global logger instance
logger = LumaLogger()

# Convenience functions for easy import
def debug(message: str) -> None:
    """Log debug message."""
    logger.debug(message)

def info(message: str) -> None:
    """Log info message."""
    logger.info(message)

def warning(message: str) -> None:
    """Log warning message."""
    logger.warning(message)

def error(message: str) -> None:
    """Log error message."""
    logger.error(message)

def critical(message: str) -> None:
    """Log critical message."""
    logger.critical(message)

def exception(message: str) -> None:
    """Log exception with traceback."""
    logger.exception(message)
