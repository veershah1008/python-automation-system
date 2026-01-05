# Smart File Organizer v2.0

A modern, intelligent file organization tool built with PyQt6 that automatically sorts files into categories based on their extensions.

## Features

- **Automatic File Organization**: Monitors folders and automatically sorts files into categories
- **Real-time Monitoring**: Uses watchdog for efficient file system monitoring
- **Dark/Light Theme**: Toggle between modern dark and light themes
- **Configurable Categories**: Easily customize file categories and extensions
- **Enhanced Logging**: Comprehensive logging with both file and GUI display
- **Duplicate Handling**: Automatically handles duplicate files with smart renaming
- **Existing File Organization**: Organizes files already present in the folder
- **Modern UI**: Clean, responsive interface with smooth animations

## Supported File Categories

- **Images**: jpg, jpeg, png, gif, bmp, tiff, webp
- **Documents**: pdf, docx, txt, doc, rtf, odt
- **Videos**: mp4, mkv, avi, mov, wmv, flv, webm
- **Audio**: mp3, wav, flac, aac, ogg, wma
- **Executables**: exe, msi, deb, dmg
- **Archives**: zip, rar, 7z, tar, gz, bz2
- **Code**: py, js, html, css, cpp, java, c
- **Spreadsheets**: xlsx, xls, csv, ods

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd file-organizer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python automation.py
```

## Usage

1. **Select Folder**: Click "Select Folder" to choose the directory you want to organize
2. **Start Monitoring**: Click "Start Monitoring" to begin automatic file organization
3. **View Progress**: Monitor the log output to see files being organized in real-time
4. **Stop When Done**: Click "Stop Monitoring" when you're finished

## Configuration

The application uses a `config.json` file for customization:

- **File Categories**: Add or modify file extensions for each category
- **UI Settings**: Adjust window size, animation duration, and log limits

## Logging

- **GUI Logging**: Real-time log display in the application
- **File Logging**: Detailed logs saved to `file_organizer.log`
- **Log Rotation**: Automatic cleanup of old log entries

## Architecture

The application follows a clean, modular architecture:

- `automation.py`: Main application and UI logic
- `config.py`: Configuration management
- `logger.py`: Enhanced logging system
- `styles.py`: Theme and styling system

## Requirements

- Python 3.7+
- PyQt6
- watchdog
- pathlib (built-in for Python 3.4+)

## License

This project is open source and available under the MIT License.