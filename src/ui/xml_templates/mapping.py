from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QGroupBox, QVBoxLayout, QFormLayout, QLineEdit
from PySide6.QtCore import Qt

class MappingPage(QWidget):
    """Mapping xml templates function view."""
    
    def __init__(self):
        super().__init__()
        self._setup_ui()
        self.PREFERRED_WIDTH = 600
        self.PREFERRED_HEIGHT = 450

    
    def _setup_ui(self):
        """Configure the user interface."""
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        
        group_box = self._create_group_box()
        self.main_layout.addWidget(group_box)
    
    
    def _create_group_box(self):
        """Create and configure the main group box."""
        group_box = QGroupBox()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Title
        welcome_label = QLabel("Mapping xml templates function.")
        welcome_label.setStyleSheet("font-size: 15px; font-weight: bold; margin-left: 20px; margin-bottom: 20px;")
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(welcome_label)
        
        # Files and directory
        form_layout_widget = QWidget()
        form_layout = QFormLayout()
        form_layout.setVerticalSpacing(15)
        form_layout.addRow(QLabel("Input directory:"), QLineEdit())
        form_layout.addRow(QLabel("Output directory:"), QLineEdit())
        form_layout.addRow(QLabel("Mapping file:"), QLineEdit())
        form_layout_widget.setLayout(form_layout)
        layout.addWidget(form_layout_widget)
        
        group_box.setLayout(layout)
        return group_box
    
    
    def get_preferred_size(self) -> tuple[int, int]:
        """Returns the preferred size for this page.
        
        Returns:
            tuple: (width, height) in pixels
        """
        return self.PREFERRED_WIDTH, self.PREFERRED_HEIGHT
