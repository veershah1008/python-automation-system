#!/usr/bin/env python3
"""
Simple launcher script for the Smart File Organizer.
This script ensures proper error handling and dependency checking.
"""

import sys
import os

def check_dependencies():
    """Check if all required dependencies are installed."""
    required_packages = ['PyQt6', 'watchdog']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("Missing required packages:")
        for package in missing_packages:
            print(f"  - {package}")
        print("\nPlease install them using:")
        print("pip install -r requirements.txt")
        return False
    
    return True

def main():
    """Main launcher function."""
    print("Smart File Organizer v2.0")
    print("=" * 30)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check if icons directory exists
    if not os.path.exists("icons"):
        print("Warning: Icons directory not found. Some UI elements may not display correctly.")
    
    # Import and run the application
    try:
        from automation import FileOrganizerApp
        from PyQt6.QtWidgets import QApplication
        
        app = QApplication(sys.argv)
        window = FileOrganizerApp()
        window.show()
        
        print("Application started successfully!")
        sys.exit(app.exec())
        
    except Exception as e:
        print(f"Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()