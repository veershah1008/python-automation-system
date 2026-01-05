from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, 
                             QLabel, QFileDialog, QTextEdit, QHBoxLayout, QFrame,
                             QMessageBox, QProgressBar, QSplitter)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QPropertyAnimation, QEasingCurve, QEvent, QSize, QTimer, QObject
from PyQt6.QtGui import QPalette, QColor, QIcon
import shutil
import os
import time
import sys
from pathlib import Path
from typing import Optional, Dict, List
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from styles import apply_stylesheet
from config import Config
from logger import FileOrganizerLogger

class FileHandler(QObject, FileSystemEventHandler):
    """Enhanced file system event handler with better error handling."""
    
    file_moved = pyqtSignal(str, str)
    file_error = pyqtSignal(str, str)

    def __init__(self, source_folder: str, config: Config, logger: FileOrganizerLogger):
        super().__init__()
        self.source_folder = Path(source_folder)
        self.config = config
        self.logger = logger

    def on_created(self, event):
        """Handle file creation events."""
        if event.is_directory:
            return
            
        file_path = Path(event.src_path)
        
        # Wait a bit to ensure file is fully written
        time.sleep(0.1)
        
        if not file_path.exists():
            return
            
        self._organize_file(file_path)

    def _organize_file(self, file_path: Path) -> bool:
        """Organize a single file into appropriate category."""
        try:
            file_ext = file_path.suffix.lower()
            file_name = file_path.name
            
            # Skip hidden files and system files
            if file_name.startswith('.') or file_name.startswith('~'):
                return False
            
            category = self._get_file_category(file_ext)
            if not category:
                return False
                
            dest_folder = self.source_folder / category
            dest_folder.mkdir(exist_ok=True)
            
            # Handle duplicate files
            dest_path = self._get_unique_path(dest_folder / file_name)
            
            shutil.move(str(file_path), str(dest_path))
            self.file_moved.emit(file_name, category)
            self.logger.success(f"Moved: {file_name} → {category}", emit_signal=False)
            return True
            
        except Exception as e:
            error_msg = f"Error moving {file_path.name}: {str(e)}"
            self.file_error.emit(file_path.name, error_msg)
            self.logger.error(error_msg, emit_signal=False)
            return False
    
    def _get_file_category(self, file_ext: str) -> Optional[str]:
        """Get the category for a file extension."""
        for category, extensions in self.config.file_categories.items():
            if file_ext in extensions:
                return category
        return None
    
    def _get_unique_path(self, path: Path) -> Path:
        """Get a unique file path to avoid overwrites."""
        if not path.exists():
            return path
            
        stem = path.stem
        suffix = path.suffix
        counter = 1
        
        while path.exists():
            path = path.parent / f"{stem}_{counter}{suffix}"
            counter += 1
            
        return path

class FolderMonitor(QThread):
    """Enhanced folder monitoring thread with better error handling."""
    
    file_moved = pyqtSignal(str, str)
    file_error = pyqtSignal(str, str)
    monitoring_started = pyqtSignal()
    monitoring_stopped = pyqtSignal()

    def __init__(self, source_folder: str, config: Config, logger: FileOrganizerLogger):
        super().__init__()
        self.source_folder = source_folder
        self.config = config
        self.logger = logger
        self.stop_event = False
        self.observer = None

    def run(self):
        """Main monitoring loop."""
        try:
            self.logger.info(f"Starting monitor for {self.source_folder}", emit_signal=False)
            
            event_handler = FileHandler(self.source_folder, self.config, self.logger)
            event_handler.file_moved.connect(self.file_moved)
            event_handler.file_error.connect(self.file_error)
            
            self.observer = Observer()
            self.observer.schedule(event_handler, self.source_folder, recursive=False)
            self.observer.start()
            
            self.monitoring_started.emit()
            
            while not self.stop_event:
                time.sleep(0.5)  # More responsive stopping
                
        except Exception as e:
            self.logger.error(f"Monitor error: {str(e)}", emit_signal=False)
        finally:
            if self.observer:
                self.observer.stop()
                self.observer.join()
            self.monitoring_stopped.emit()
            self.logger.info("Monitor stopped", emit_signal=False)

    def stop(self):
        """Stop the monitoring thread gracefully."""
        self.logger.info("Stopping monitor...", emit_signal=False)
        self.stop_event = True
        if self.observer:
            self.observer.stop()

class FileOrganizerApp(QWidget):
    """Enhanced File Organizer application with improved architecture."""
    
    def __init__(self):
        super().__init__()
        
        # Initialize configuration and logging
        self.config = Config()
        self.logger = FileOrganizerLogger()
        self.logger.log_updated.connect(self._update_log_display)
        
        # Application state
        self.source_folder = None
        self.worker = None
        self.is_dark_mode = False
        
        self._setup_ui()
        self._setup_connections()
        self._setup_animations()
        
        # Apply initial styling
        apply_stylesheet(self, self.is_dark_mode)
        
        # Start fade-in animation
        QTimer.singleShot(100, self.start_fade_in)

    def _setup_ui(self):
        """Initialize the user interface."""
        ui_settings = self.config.ui_settings
        
        self.setWindowTitle("Smart File Organizer v2.0")
        self.setGeometry(400, 200, ui_settings["window_width"], ui_settings["window_height"])
        
        # Main layout
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(10)

        # Top layout for header and toggle button
        self.top_layout = QHBoxLayout()
        self.header_label = QLabel("Smart File Organizer v2.0")
        self.header_label.setObjectName("header")
        self.top_layout.addWidget(self.header_label)
        self.top_layout.addStretch()
        
        self.toggle_dark_mode_button = QPushButton()
        self.toggle_dark_mode_button.setObjectName("toggleDarkModeButton")
        self.toggle_dark_mode_button.setIcon(QIcon("icons/sun-line.png"))
        self.toggle_dark_mode_button.setIconSize(QSize(24, 24))
        self.top_layout.addWidget(self.toggle_dark_mode_button)
        self.layout.addLayout(self.top_layout)

        # Log Output with max lines limit
        self.log_output = QTextEdit()
        self.log_output.setObjectName("logOutput")
        self.log_output.setReadOnly(True)
        self.log_output.document().setMaximumBlockCount(ui_settings["log_max_lines"])
        self.layout.addWidget(self.log_output)

        # Button Container
        self.button_container = QFrame()
        self.button_container.setObjectName("buttonContainer")
        self.button_layout = QHBoxLayout()
        self.button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.button_layout.setSpacing(8)

        self.select_button = QPushButton("Select Folder")
        self.start_button = QPushButton("Start Monitoring")
        self.stop_button = QPushButton("Stop Monitoring")
        self.view_logs_button = QPushButton("View Logs")

        self.buttons = [self.select_button, self.start_button, self.stop_button, self.view_logs_button]
        for button in self.buttons:
            self.button_layout.addWidget(button)
        self.button_container.setLayout(self.button_layout)
        self.layout.addWidget(self.button_container)

        self.setLayout(self.layout)

    def _setup_connections(self):
        """Setup signal connections."""
        self.select_button.clicked.connect(self.select_folder)
        self.start_button.clicked.connect(self.start_monitoring)
        self.stop_button.clicked.connect(self.stop_monitoring)
        self.view_logs_button.clicked.connect(self.view_logs)
        self.toggle_dark_mode_button.clicked.connect(self.toggle_dark_mode)

    def _setup_animations(self):
        """Setup UI animations."""
        ui_settings = self.config.ui_settings
        duration = ui_settings["animation_duration"]
        
        self.fade_in_animation = QPropertyAnimation(self.button_container, b"windowOpacity")
        self.fade_in_animation.setDuration(500)
        self.fade_in_animation.setStartValue(0)
        self.fade_in_animation.setEndValue(1)
        self.fade_in_animation.setEasingCurve(QEasingCurve.Type.OutQuad)

        self.log_fade_in_animation = QPropertyAnimation(self.log_output, b"windowOpacity")
        self.log_fade_in_animation.setDuration(500)
        self.log_fade_in_animation.setStartValue(0)
        self.log_fade_in_animation.setEndValue(1)
        self.log_fade_in_animation.setEasingCurve(QEasingCurve.Type.OutQuad)

        self.log_animation = QPropertyAnimation(self.log_output, b"maximumHeight")
        self.log_animation.setDuration(duration)
        self.log_animation.setEasingCurve(QEasingCurve.Type.OutQuad)

        # Install event filters for hover animations
        for button in self.buttons + [self.toggle_dark_mode_button]:
            button.installEventFilter(self)

    def start_fade_in(self):
        self.fade_in_animation.start()
        self.log_fade_in_animation.start()

    def apply_stylesheet(self):
        current_opacity = self.windowOpacity()
        apply_stylesheet(self, self.is_dark_mode)
        self.setWindowOpacity(current_opacity)
        mode_transition = QPropertyAnimation(self, b"windowOpacity")
        mode_transition.setDuration(500)
        mode_transition.setStartValue(current_opacity)
        mode_transition.setEndValue(1)
        mode_transition.setEasingCurve(QEasingCurve.Type.OutQuad)
        mode_transition.start()

    def eventFilter(self, obj, event):
        if obj in [self.select_button, self.start_button, self.stop_button, self.view_logs_button, self.toggle_dark_mode_button]:
            if event.type() == QEvent.Type.Enter:
                anim = QPropertyAnimation(obj, b"geometry")
                anim.setDuration(200)
                anim.setStartValue(obj.geometry())
                anim.setEndValue(obj.geometry().adjusted(0, 0, 0, -5))
                anim.setEasingCurve(QEasingCurve.Type.OutQuad)
                anim.start()

                scale_anim = QPropertyAnimation(obj, b"minimumWidth")
                scale_anim.setDuration(200)
                scale_anim.setStartValue(obj.minimumWidth())
                scale_anim.setEndValue(obj.minimumWidth() * 1.05)
                scale_anim.setEasingCurve(QEasingCurve.Type.OutQuad)
                scale_anim.start()
            elif event.type() == QEvent.Type.Leave:
                anim = QPropertyAnimation(obj, b"geometry")
                anim.setDuration(200)
                anim.setStartValue(obj.geometry())
                anim.setEndValue(obj.geometry().adjusted(0, 0, 0, 5))
                anim.setEasingCurve(QEasingCurve.Type.OutQuad)
                anim.start()

                scale_anim = QPropertyAnimation(obj, b"minimumWidth")
                scale_anim.setDuration(200)
                scale_anim.setStartValue(obj.minimumWidth())
                scale_anim.setEndValue(obj.minimumWidth() / 1.05)
                scale_anim.start()
        return super().eventFilter(obj, event)

    def select_folder(self):
        """Select folder to monitor with validation."""
        folder = QFileDialog.getExistingDirectory(self, "Select Folder to Monitor")
        if folder:
            if not os.access(folder, os.R_OK | os.W_OK):
                self.logger.error("Selected folder is not accessible!")
                return
                
            self.source_folder = folder
            self.logger.info(f"📁 Folder Selected: {self.source_folder}")
            
            # Show folder statistics
            try:
                files_count = len([f for f in Path(folder).iterdir() if f.is_file()])
                self.logger.info(f"Found {files_count} files to organize")
            except Exception as e:
                self.logger.error(f"Error reading folder: {str(e)}")

    def organize_existing_files(self):
        """Organize existing files in the selected folder using the new system."""
        if not self.source_folder:
            return
            
        self.logger.info("🗂️ Organizing existing files...")
        source_path = Path(self.source_folder)
        
        # Create a temporary file handler for organizing existing files
        file_handler = FileHandler(self.source_folder, self.config, self.logger)
        
        organized_count = 0
        for file_path in source_path.iterdir():
            if file_path.is_file():
                if file_handler._organize_file(file_path):
                    organized_count += 1
        
        self.logger.info(f"Organized {organized_count} existing files")

    def start_monitoring(self):
        """Start monitoring the selected folder."""
        if not self.source_folder:
            self.logger.warning("Please select a folder first!")
            return
            
        if self.worker and self.worker.isRunning():
            self.logger.warning("Monitoring is already running!")
            return
            
        try:
            # Organize existing files first
            self.organize_existing_files()
            
            # Then start monitoring for new files
            if self.worker:
                self.worker.stop()
                self.worker.wait()
                
            self.worker = FolderMonitor(self.source_folder, self.config, self.logger)
            self.worker.file_moved.connect(self._on_file_moved)
            self.worker.file_error.connect(self._on_file_error)
            self.worker.monitoring_started.connect(lambda: self.logger.info("▶️ Monitoring Started..."))
            self.worker.monitoring_stopped.connect(lambda: self.logger.info("⏹️ Monitoring Stopped"))
            self.worker.start()
            
        except Exception as e:
            self.logger.error(f"Error starting monitoring: {str(e)}")

    def stop_monitoring(self):
        """Stop monitoring the folder."""
        if self.worker and self.worker.isRunning():
            try:
                self.worker.stop()
                self.worker.wait()
                self.worker = None
            except Exception as e:
                self.logger.error(f"Error stopping monitoring: {str(e)}")
        else:
            self.logger.warning("No monitoring to stop!")

    def view_logs(self):
        """Open the log file in the default text editor."""
        log_file = self.logger.log_file
        if os.path.exists(log_file):
            try:
                os.startfile(log_file)  # Windows
            except AttributeError:
                os.system(f"open {log_file}")  # macOS
            except:
                os.system(f"xdg-open {log_file}")  # Linux
        else:
            self.logger.warning("No log file found!")

    def toggle_dark_mode(self):
        """Toggle between dark and light mode."""
        self.is_dark_mode = not self.is_dark_mode
        self.apply_stylesheet()

    def _update_log_display(self, message: str):
        """Update the log display with new messages."""
        self.log_output.append(message)
        self.animate_log_with_fade()

    def _on_file_moved(self, file_name: str, category: str):
        """Handle file moved signal."""
        # The logger already handles the display update
        pass

    def _on_file_error(self, file_name: str, error_msg: str):
        """Handle file error signal."""
        # The logger already handles the display update
        pass

    def animate_log_with_fade(self):
        """Animate log updates with fade effect."""
        self.log_animation.setStartValue(self.log_output.height())
        self.log_animation.setEndValue(self.log_output.height() + 20)
        self.log_animation.start()

        log_fade = QPropertyAnimation(self.log_output, b"windowOpacity")
        log_fade.setDuration(300)
        log_fade.setStartValue(0.5)
        log_fade.setEndValue(1)
        log_fade.setEasingCurve(QEasingCurve.Type.OutQuad)
        log_fade.start()

    def closeEvent(self, event):
        """Handle application close event."""
        if self.worker and self.worker.isRunning():
            self.worker.stop()
            self.worker.wait()
        event.accept()

if __name__ == "__main__":
    app = QApplication([])
    window = FileOrganizerApp()
    window.show()
    app.exec()