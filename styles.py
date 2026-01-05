# styles.py
"""Enhanced styling system for the File Organizer application."""

from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import QSize

def apply_stylesheet(main_window, is_dark_mode):
    # Stripe-inspired dark theme
    dark_stylesheet = """
        QWidget {
            background: #1A1A3A;  /* Stripe's dark background */
            color: #FFFFFF;  /* White text */
            font-family: 'Inter', 'Segoe UI', Arial, sans-serif;
            font-size: 14px;
        }
        #header {
            font-size: 28px;
            font-weight: bold;
            color: #FFFFFF;
            padding: 20px;
            text-align: center;
            background: linear-gradient(145deg, #1A1A3A, #242450);  /* Gradient like Stripe */
            border-radius: 15px;
            margin: 10px;
        }
        #toggleDarkModeButton {
            background-color: transparent;
            border: 1px solid #585B70;
            border-radius: 12px;
            padding: 2px;
            width: 40px;
            height: 40px;
        }
        #toggleDarkModeButton:hover {
            background-color: #585B70;
        }
        #logOutput {
            background-color: #242450;  /* Slightly lighter dark shade */
            border-radius: 15px;
            padding: 15px;
            border: 1px solid #585B70;
            color: #FFFFFF;
            margin: 10px;
            font-family: 'Consolas', 'Courier New', monospace;
        }
        #buttonContainer {
            background-color: #2E2E5A;  /* Slightly darker than buttons for contrast */
            border-radius: 30px;
            padding: 10px;
            margin: 10px;
            border: 1px solid #585B70;  /* Subtle border for separation */
        }
        QPushButton {
            background: linear-gradient(145deg, #635BFF, #4A47FF);  /* Gradient for depth */
            color: #FFFFFF;
            border: 1px solid #4A47FF;  /* Subtle border to separate buttons */
            border-radius: 30px;
            padding: 8px 16px;
            font-weight: bold;
            font-size: 14px;
            min-width: 120px;
            margin: 5px;
        }
        QPushButton:hover {
            background: linear-gradient(145deg, #7B72FF, #635BFF);  /* Lighter gradient on hover */
        }
        QPushButton:pressed {
            background: linear-gradient(145deg, #4A47FF, #3A37FF);  /* Darker gradient when pressed */
        }
        QLabel {
            color: #FFFFFF;
            font-size: 16px;
            padding: 5px;
        }
        QTextEdit {
            background-color: #242450;
            border-radius: 15px;
            padding: 15px;
            border: 1px solid #585B70;
            color: #FFFFFF;
            margin: 10px;
            font-family: 'Consolas', 'Courier New', monospace;
        }
    """
    # Light theme (Stripe-inspired but lighter)
    light_stylesheet = """
        QWidget {
            background: #F5F5F5;
            color: #1A1A3A;
            font-family: 'Inter', 'Segoe UI', Arial, sans-serif;
            font-size: 14px;
        }
        #header {
            font-size: 28px;
            font-weight: bold;
            color: #1A1A3A;
            padding: 20px;
            text-align: center;
            background: linear-gradient(145deg, #E5E9F0, #F5F5F5);
            border-radius: 15px;
            margin: 10px;
        }
        #toggleDarkModeButton {
            background-color: transparent;
            border: 1px solid #D8DEE9;
            border-radius: 12px;
            padding: 2px;
            width: 40px;
            height: 40px;
        }
        #toggleDarkModeButton:hover {
            background-color: #D8DEE9;
        }
        #logOutput {
            background-color: #E5E9F0;
            border-radius: 15px;
            padding: 15px;
            border: 1px solid #D8DEE9;
            color: #1A1A3A;
            margin: 10px;
            font-family: 'Consolas', 'Courier New', monospace;
        }
        #buttonContainer {
            background-color: #D8DEE9;  /* Lighter background for contrast */
            border-radius: 30px;
            padding: 10px;
            margin: 10px;
            border: 1px solid #B0B7C4;  /* Subtle border for separation */
        }
        QPushButton {
            background: linear-gradient(145deg, #635BFF, #4A47FF);
            color: #1453FF;
            border: 1px solid #4A47FF;
            border-radius: 30px;
            padding: 8px 16px;
            font-weight: bold;
            font-size: 14px;
            min-width: 120px;
            margin: 5px;
        }
        QPushButton:hover {
            background: linear-gradient(145deg, #7B72FF, #635BFF);
        }
        QPushButton:pressed {
            background: linear-gradient(145deg, #4A47FF, #3A37FF);
        }
        QLabel {
            color: #1A1A3A;
            font-size: 16px;
            padding: 5px;
        }
        QTextEdit {
            background-color: #E5E9F0;
            border-radius: 15px;
            padding: 15px;
            border: 1px solid #D8DEE9;
            color: #1A1A3A;
            margin: 10px;
            font-family: 'Consolas', 'Courier New', monospace;
        }
    """

    # Apply the appropriate stylesheet
    main_window.setStyleSheet(dark_stylesheet if is_dark_mode else light_stylesheet)

    # Set the icon for the toggle button
    if hasattr(main_window, "toggle_dark_mode_button"):
        main_window.toggle_dark_mode_button.setIcon(
            QIcon("icons/moon-line.png") if is_dark_mode else QIcon("icons/sun-line.png")
        )
        main_window.toggle_dark_mode_button.setIconSize(QSize(24, 24))