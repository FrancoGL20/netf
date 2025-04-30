from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QGroupBox, QVBoxLayout, QFormLayout, QLineEdit, QGridLayout
from PySide6.QtCore import Qt

class MappingPage(QWidget):
    """Mapping xml templates function view."""
    
    def __init__(self):
        self.preferred_width = 600
        self.preferred_height = 450

        super().__init__()
        self._setup_ui()

    
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
        welcome_label.setStyleSheet("font-size: 15px; font-weight: bold; margin-bottom: 20px;")
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(welcome_label)
        
        # Files and directory
        formulary_grid_widget = QWidget()
        formulary_grid = QGridLayout()
        # formulary_grid.setVerticalSpacing(15)
        # formulary_grid.addRow(QLabel("Input directory:"), QLineEdit())
        # formulary_grid.addRow(QLabel("Output directory:"), QLineEdit())
        # formulary_grid.addRow(QLabel("Mapping file:"), QLineEdit())
        # formulary_grid_widget.setLayout(formulary_grid)
        formulary_grid.setVerticalSpacing(15)
        formulary_grid.addWidget(QLabel("Input directory:"), 0, 0)
        formulary_grid.addWidget(QLineEdit(), 0, 1)
        formulary_grid.addWidget(QPushButton("Browse"), 0, 2)
        formulary_grid.addWidget(QLabel("Output directory:"), 1, 0)
        formulary_grid.addWidget(QLineEdit(), 1, 1)
        formulary_grid.addWidget(QLabel("Mapping file:"), 2, 0)
        formulary_grid.addWidget(QLineEdit(), 2, 1)
        formulary_grid_widget.setLayout(formulary_grid)
        layout.addWidget(formulary_grid_widget)
        
        group_box.setLayout(layout)
        return group_box
    
    
    def get_preferred_size(self) -> tuple[int, int]:
        """Returns the preferred size for this page.
        
        Returns:
            tuple: (width, height) in pixels
        """
        return self.preferred_width, self.preferred_height
