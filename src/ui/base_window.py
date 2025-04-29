import os
from PySide6.QtWidgets import QMainWindow, QMenuBar, QMessageBox, QWidget, QStackedLayout
from PySide6.QtGui import QIcon
from src.config.settings import (
    APP_NAME, APP_VERSION, APP_AUTHOR, APP_AUTHOR_GITHUB, PATH_ICONS
)

class BaseWindow(QMainWindow):
    """Base window with common configuration for all windows."""
    
    def __init__(self):
        super().__init__()
        self._setup_window()
        self._create_menu_bar()
        self._setup_central_widget()
        
        # Register pages
        self.pages = {}
        
    def _setup_window(self):
        """Configure basic window properties."""
        self.setWindowTitle(APP_NAME)
        # self.setMinimumSize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
        self.setWindowIcon(QIcon(os.path.join(PATH_ICONS, "Logo F.jpg")))
    
    def _create_menu_bar(self):
        """Create the main menu."""
        menubar = QMenuBar(None)
        self.setMenuBar(menubar)
        
        # File Menu
        file_menu = menubar.addMenu("&File")
        file_menu.addAction("&Exit", self.close)
        
        # Pages Menu
        self.pages_menu = menubar.addMenu("&Tools")
        # Actions will be added dynamically when registering pages
        
        # Help Menu
        help_menu = menubar.addMenu("&Help")
        help_menu.addAction("&About", self._show_about_dialog)
    
    def _setup_central_widget(self):
        """Configure the central widget and stacked widget."""
        # Central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Main layout
        # self.main_layout = QVBoxLayout()
        # self.central_widget.setLayout(self.main_layout)
        
        # Stacked Widget to handle multiple pages
        # self.stacked_widget = QStackedWidget()
        # self.main_layout.addWidget(self.stacked_widget)
        
        self.stacked_widget = QStackedLayout()
        self.central_widget.setLayout(self.stacked_widget)
    
    def _show_about_dialog(self):
        """Show the 'About' dialog."""
        QMessageBox.about(
            self,
            f"About {APP_NAME}",
            f"{APP_NAME} v{APP_VERSION}\n\n"
            f"Made by: {APP_AUTHOR}\n"
            f"Github: {APP_AUTHOR_GITHUB}\n"
        )
    
    def register_page(self, name: str, page_class, page_args=None):
        """
        Register a page in the application.
        
        Args:
            name: Page name to display in the menu
            page_class: Page class
            page_args: Arguments to initialize the page (optional)
        """
        if page_args is None:
            page_args = {}
            
        # Create page instance
        page_instance = page_class(**page_args)
        
        # Add to stacked widget
        page_index = self.stacked_widget.addWidget(page_instance)
        
        # Save reference and index
        self.pages[name] = {
            'instance': page_instance,
            'index': page_index
        }
        
        # Add to menu
        def switch_to_this_page():
            self.switch_to_page(name)
        
        self.pages_menu.addAction(f"&{name}", switch_to_this_page)
        
        return page_index
    
    def switch_to_page(self, page_name: str):
        """Switch to a specific page by its name.
        
        Args:
            page_name: Name of the page to switch to
        """
        if page_name in self.pages:
            page_instance = self.pages[page_name]['instance']
            self.stacked_widget.setCurrentIndex(self.pages[page_name]['index'])
            
            # Resize the window if the page provides a get_preferred_size method
            if hasattr(page_instance, 'get_preferred_size'):
                width, height = page_instance.get_preferred_size()
                self.resize(width, height)
                self.setMinimumSize(width, height)
        else:
            print(f"Error: Page '{page_name}' not found") 