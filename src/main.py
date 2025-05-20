import os
import sys
from src.ui.base_window import BaseWindow
from src.ui.main_page import MainPage
from src.ui.xml_templates.mapping import MappingPage
from src.ui.files_processing.drop_duplicates import DropDuplicatesPage
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from src.config.settings import APP_NAME, PATH_ICONS
from pathlib import Path

try:
    from ctypes import windll  # Only exists on Windows.
    myappid = 'FCompany.NetF.1.0'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass

def main():
    """Main entry point of the application."""
    app = QApplication(sys.argv)
    # app.setStyle("Fusion")
    app.setApplicationName(APP_NAME)
    app.setWindowIcon(QIcon(Path(PATH_ICONS, "Logo_F.ico").as_posix()))
    
    # Create main main_window
    main_window = BaseWindow()
    
    # Register pages
    main_window.register_page("Main", "menu_tools", MainPage)
    main_window.register_page("Mapping", "menu_templates", MappingPage)
    main_window.register_page("Drop duplicated file lines", "menu_tools", DropDuplicatesPage)
    
    # Switch to main page
    main_window.switch_to_page("Mapping")
    
    # Show the main_window
    main_window.show()
    
    return app.exec()

if __name__ == "__main__":
    sys.exit(main())