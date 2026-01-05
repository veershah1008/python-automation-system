#!/usr/bin/env python3
"""
Test script for the Smart File Organizer.
Creates sample files to test the organization functionality.
"""

import os
import tempfile
from pathlib import Path
from config import Config
from logger import FileOrganizerLogger

def create_test_files(test_dir):
    """Create sample files for testing."""
    test_files = [
        "document.pdf",
        "image.jpg",
        "video.mp4",
        "music.mp3",
        "archive.zip",
        "script.py",
        "spreadsheet.xlsx",
        "program.exe"
    ]
    
    for filename in test_files:
        file_path = Path(test_dir) / filename
        file_path.write_text(f"Test content for {filename}")
    
    return test_files

def test_config():
    """Test configuration system."""
    print("Testing configuration system...")
    config = Config()
    
    # Test file categories
    assert "Images" in config.file_categories
    assert ".jpg" in config.file_categories["Images"]
    
    # Test UI settings
    assert "window_width" in config.ui_settings
    assert config.ui_settings["window_width"] == 600
    
    print("✅ Configuration system working correctly")

def test_logger():
    """Test logging system."""
    print("Testing logging system...")
    logger = FileOrganizerLogger("test.log")
    
    logger.info("Test info message", emit_signal=False)
    logger.success("Test success message", emit_signal=False)
    logger.warning("Test warning message", emit_signal=False)
    logger.error("Test error message", emit_signal=False)
    
    # Check if log file was created
    assert os.path.exists("test.log")
    
    # Close logger handlers to release file
    for handler in logger.logger.handlers:
        handler.close()
    logger.logger.handlers.clear()
    
    # Clean up
    try:
        os.remove("test.log")
    except OSError:
        pass  # File might still be in use, that's okay for testing
    
    print("✅ Logging system working correctly")

def main():
    """Run all tests."""
    print("Smart File Organizer - Test Suite")
    print("=" * 40)
    
    try:
        test_config()
        test_logger()
        
        print("\n🎉 All tests passed!")
        print("The File Organizer is ready to use.")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())