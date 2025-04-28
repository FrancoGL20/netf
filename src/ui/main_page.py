import os
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt

class MainPage(QWidget):
    """Main page of the application."""
    
    def __init__(self):
        super().__init__()
        self._setup_ui()
        self.preferred_width = 500
        self.preferred_height = 400
    
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
        # Set a larger font size for the welcome label
        layout.addWidget(welcome_label)
    
    def get_preferred_size(self) -> tuple[int, int]:
        """Returns the preferred size for this page.
        
        Returns:
            tuple: (width, height) in pixels
        """
        return self.preferred_width, self.preferred_height
