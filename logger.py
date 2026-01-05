# logger.py
"""Enhanced logging system for the File Organizer application."""

import logging
import os
from datetime import datetime
from typing import Optional
from PyQt6.QtCore import QObject, pyqtSignal

class FileOrganizerLogger(QObject):
    """Custom logger with GUI integration."""
    
    log_updated = pyqtSignal(str)
    
    def __init__(self, log_file: str = "file_organizer.log"):
        super().__init__()
        self.log_file = log_file
        self._setup_logger()
    
    def _setup_logger(self):
        """Setup file and console logging."""
        self.logger = logging.getLogger("FileOrganizer")
        self.logger.setLevel(logging.INFO)
        
        # Clear existing handlers
        self.logger.handlers.clear()
        
        # File handler
        file_handler = logging.FileHandler(self.log_file, encoding='utf-8')
        file_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter('%(levelname)s: %(message)s')
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
    
    def info(self, message: str, emit_signal: bool = True):
        """Log info message."""
        self.logger.info(message)
        if emit_signal:
            self.log_updated.emit(f"ℹ️ {message}")
    
    def success(self, message: str, emit_signal: bool = True):
        """Log success message."""
        self.logger.info(f"SUCCESS: {message}")
        if emit_signal:
            self.log_updated.emit(f"✅ {message}")
    
    def warning(self, message: str, emit_signal: bool = True):
        """Log warning message."""
        self.logger.warning(message)
        if emit_signal:
            self.log_updated.emit(f"⚠️ {message}")
    
    def error(self, message: str, emit_signal: bool = True):
        """Log error message."""
        self.logger.error(message)
        if emit_signal:
            self.log_updated.emit(f"❌ {message}")
    
    def clear_old_logs(self, days: int = 30):
        """Clear log entries older than specified days."""
        if not os.path.exists(self.log_file):
            return
        
        try:
            # This is a simple implementation - in production you might want
            # to use log rotation instead
            file_age = datetime.now().timestamp() - os.path.getmtime(self.log_file)
            if file_age > (days * 24 * 3600):  # Convert days to seconds
                os.remove(self.log_file)
                self._setup_logger()
        except OSError:
            pass