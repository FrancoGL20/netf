import os
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt

class MappingPage(QWidget):
    """Mapping xml templates function."""
    
    def __init__(self):
        super().__init__()
        self._setup_ui()
        self.preferred_width = 400
        self.preferred_height = 500

    def _setup_ui(self):
        """Configure the user interface of the mapping page."""
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Add specific widgets for your main page here
        welcome_label = QLabel("Mapping xml templates function.")
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(welcome_label)
    
    def get_preferred_size(self) -> tuple[int, int]:
        """Returns the preferred size for this page.
        
        Returns:
            tuple: (width, height) in pixels
        """
        return self.preferred_width, self.preferred_height
