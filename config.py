# config.py
"""Configuration management for the File Organizer application."""

import json
import os
from typing import Dict, List, Optional

class Config:
    """Manages application configuration and file categories."""
    
    DEFAULT_CONFIG = {
        "file_categories": {
            "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"],
            "Documents": [".pdf", ".docx", ".txt", ".doc", ".rtf", ".odt"],
            "Videos": [".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm"],
            "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma"],
            "Executables": [".exe", ".msi", ".deb", ".dmg"],
            "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"],
            "Code": [".py", ".js", ".html", ".css", ".cpp", ".java", ".c"],
            "Spreadsheets": [".xlsx", ".xls", ".csv", ".ods"]
        },
        "ui_settings": {
            "window_width": 600,
            "window_height": 700,
            "animation_duration": 300,
            "log_max_lines": 1000
        }
    }
    
    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self.config = self._load_config()
    
    def _load_config(self) -> Dict:
        """Load configuration from file or create default."""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        return self.DEFAULT_CONFIG.copy()
    
    def save_config(self) -> None:
        """Save current configuration to file."""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except IOError as e:
            print(f"Failed to save config: {e}")
    
    @property
    def file_categories(self) -> Dict[str, List[str]]:
        return self.config.get("file_categories", self.DEFAULT_CONFIG["file_categories"])
    
    @property
    def ui_settings(self) -> Dict:
        return self.config.get("ui_settings", self.DEFAULT_CONFIG["ui_settings"])
    
    def add_category(self, name: str, extensions: List[str]) -> None:
        """Add a new file category."""
        self.config["file_categories"][name] = extensions
        self.save_config()
    
    def remove_category(self, name: str) -> None:
        """Remove a file category."""
        if name in self.config["file_categories"]:
            del self.config["file_categories"][name]
            self.save_config()