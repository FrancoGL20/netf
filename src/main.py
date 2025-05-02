import os
import sys
from src.ui.base_window import BaseWindow
from src.ui.main_page import MainPage
from src.ui.xml_templates.mapping import MappingPage
from src.ui.files_processing.drop_duplicates import DropDuplicatesPage
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from src.config.settings import APP_NAME, PATH_ICONS

def main():
    """Main entry point of the application."""
    app = QApplication(sys.argv)
    # app.setStyle("Fusion")
    app.setApplicationName(APP_NAME)
    app.setWindowIcon(QIcon(os.path.join(PATH_ICONS, "Logo_F.ico")))
    
    # Create main main_window
    main_window = BaseWindow()
    
    # Register pages
    main_window.register_page("Main", MainPage)
    main_window.register_page("Mapping", MappingPage)
    main_window.register_page("Drop duplicated file lines", DropDuplicatesPage)
    
    # Switch to main page
    main_window.switch_to_page("Mapping")
    
    # Show the main_window
    main_window.show()
    
    return app.exec()

if __name__ == "__main__":
    sys.exit(main())