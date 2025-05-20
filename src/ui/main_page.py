import os
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt

class MainPage(QWidget):
    """Main page of the application."""
    
    def __init__(self, main_window=None):
        self.PREFERRED_WIDTH = 350
        self.PREFERRED_HEIGHT = 350
        self.main_window = main_window
        
        super().__init__()
        self._setup_ui()
    
    def _setup_ui(self):
        """Configure the user interface of the main page."""
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Adding a title widget to the page
        title_widget = QLabel("Main Page")
        title_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_widget)
        font = title_widget.font()
        font.setPointSize(24)  # Increase font size to 24 points
        title_widget.setFont(font)
        
        # Add specific widgets for your main page here
        welcome_label = QLabel("Welcome to the application!")
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(welcome_label)
    
    def get_preferred_size(self) -> tuple[int, int]:
        """Returns the preferred size for this page.
        
        Returns:
            tuple: (width, height) in pixels
        """
        return self.PREFERRED_WIDTH, self.PREFERRED_HEIGHT
