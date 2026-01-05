# Smart File Organizer

A Python-based desktop automation tool with a PyQt6 GUI that monitors a selected folder in real time and automatically organizes files into categorized directories based on file extensions.

## Features
- Real-time folder monitoring using watchdog
- Automatic file organization by file type
- Desktop GUI built with PyQt6
- Background processing to keep the UI responsive
- Logging of file operations and errors
- Light and dark theme support

## Tech Stack
- Python
- PyQt6
- watchdog

## Project Structure
- `automation.py` – main application and UI logic  
- `config.py` – file category configuration  
- `logger.py` – logging system  
- `styles.py` – application styling and themes  

## How to Run
1. Clone the repository:
   git clone https://github.com/veershah1008/python-automation-system.git

2. Install dependencies:
    pip install -r requirements.txt

3. Run the application:
    python run.py
