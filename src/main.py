import sys
from src.ui.base_window import BaseWindow
from src.ui.main_page import MainPage
from src.ui.xml_templates.mapping import MappingPage
from src.ui.files_processing.drop_duplicates import DropDuplicatesPage
from PySide6.QtWidgets import QApplication

def main():
    """Main entry point of the application."""
    app = QApplication(sys.argv)
    
    # Create main window
    window = BaseWindow()
    
    # Register pages
    window.register_page("Main", MainPage)
    window.register_page("Mapping", MappingPage)
    window.register_page("Drop duplicated file lines", DropDuplicatesPage)
    
    # Switch to main page
    window.switch_to_page("Drop duplicated file lines")
    
    # Show the window
    window.show()
    
    return app.exec()

if __name__ == "__main__":
    sys.exit(main())