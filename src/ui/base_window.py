from PySide6.QtWidgets import (
    QMainWindow,
    QMenuBar,
    QMessageBox,
    QWidget,
    QStackedLayout,
)
from src.config.settings import APP_NAME, APP_VERSION, APP_AUTHOR, APP_AUTHOR_GITHUB


class BaseWindow(QMainWindow):
    """Base window with common configuration for all windows."""

    def __init__(self):
        super().__init__()
        self._setup_window()
        self._create_menu_bar()
        self._setup_central_widget()

        # Register pages
        self._pages = {}

        self._menus = {
            "menu_tools": self.pages_menu,
            "menu_templates": self.templates_menu,
        }


    def _setup_window(self):
        """Configure basic window properties."""
        self.setWindowTitle(APP_NAME)


    def _create_menu_bar(self):
        """Create the main menu."""
        menubar = QMenuBar(self)
        self.setMenuBar(menubar)

        # File Menu
        file_menu = menubar.addMenu("&File")
        file_menu.addAction("&Exit", self.close)

        # Files tools menu
        self.pages_menu = menubar.addMenu("&Tools")
        
        # Templates tools menu
        self.templates_menu = menubar.addMenu("&Templates")

        # Help Menu
        help_menu = menubar.addMenu("&Help")
        help_menu.addAction("&About", self._show_about_dialog)


    def _setup_central_widget(self):
        """Configure the central widget and stacked widget."""

        # The central widget is a QWidget with a QStackedLayout as its layout
        self.central_widget = QWidget()
        self.stacked_widget = QStackedLayout()
        self.central_widget.setLayout(self.stacked_widget)
        self.setCentralWidget(self.central_widget)


    def register_page(self, name: str, page_menu: str, page_class: type, page_args: dict = None):
        """
        Register a page in the application.

        Args:
            name: Page name to display in the menu
            page_menu: Menu to add the page to
            page_class: Page class
            page_args: Arguments to initialize the page (optional)
        """
        if page_args is None:
            page_args = {}

        # Create page instance with parent window reference
        page_args["main_window"] = self
        page_instance = page_class(**page_args)

        # Add to stacked widget
        page_index = self.stacked_widget.addWidget(page_instance)

        # Save reference and index
        self._pages[name] = {"instance": page_instance, "index": page_index}

        # Add to menu
        def switch_to_this_page():
            self.switch_to_page(name)

        self._menus[page_menu].addAction(f"&{name}", switch_to_this_page)

        return page_index

    def switch_to_page(self, page_name: str):
        """Switch to a specific page by its name.

        Args:
            page_name: Name of the page to switch to
        """
        if page_name in self._pages:
            page_instance = self._pages[page_name]["instance"]
            self.stacked_widget.setCurrentIndex(self._pages[page_name]["index"])

            # Set the window title to the page name
            self.setWindowTitle(f"{APP_NAME} - {page_name}")

            # Resize the window if the page provides a get_preferred_size method
            if hasattr(page_instance, "get_preferred_size"):
                width, height = page_instance.get_preferred_size()
                self.resize_window(width, height)
        else:
            print(f"Error: Page '{page_name}' not found")

    def resize_window(self, width: int, height: int, fixed: bool = False):
        """
        Resize the window with optional fixed size.

        Args:
            width: New window width
            height: New window height
            fixed: If True, window size will be fixed
        """
        if fixed:
            self.setFixedSize(width, height)
        else:
            self.setMinimumSize(width, height)
            self.resize(width, height)

    # 4. Métodos auxiliares privados
    def _show_about_dialog(self):
        """Show the 'About' dialog."""
        QMessageBox.about(
            self,
            f"About {APP_NAME}",
            f"{APP_NAME} v{APP_VERSION}\n\n"
            f"Made by: {APP_AUTHOR}\n"
            f"Github: {APP_AUTHOR_GITHUB}\n",
        )
