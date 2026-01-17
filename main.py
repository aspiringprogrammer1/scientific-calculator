import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow

def main():
    """
    Main function to initialize and run the PyQt6 application.
    """
    # Create the application object
    app = QApplication(sys.argv)
    
    # Create the main window
    window = MainWindow()
    
    # Show the window
    window.show()
    
    # Start the application's event loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()