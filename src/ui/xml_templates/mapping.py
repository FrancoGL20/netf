from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QGroupBox, QVBoxLayout, QFormLayout, QLineEdit, QGridLayout
from PySide6.QtCore import Qt
from src.config.settings import PATH_ROOT
import os, json

class MappingPage(QWidget):
    """Mapping xml templates function view."""
    
    def __init__(self):
        self.PREFERRED_WIDTH = 1000
        self.PREFERRED_HEIGHT = 450
        self.MEMORY_FILE = os.path.join(PATH_ROOT,'.memory','mapping.json')

        super().__init__()
        self._setup_ui()

    
    def _setup_ui(self):
        """Configure the user interface."""
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        
        group_box = self._create_group_box()
        self.main_layout.addWidget(group_box)
        
        self._update_ui_with_memory()
    
    
    def _update_ui_with_memory(self):
        """Update the UI with the memory file data."""
        if os.path.exists(self.MEMORY_FILE):
            with open(self.MEMORY_FILE, 'r') as file:
                data = json.load(file)

                # Update UI elements with data from the memory file
                self.input_directory_line_edit.setText(data.get('input_directory', ''))
                self.output_directory_line_edit.setText(data.get('output_directory', ''))
                self.mapping_file_line_edit.setText(data.get('mapping_file', ''))
    
    
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
        formulary_grid.setVerticalSpacing(15)
        formulary_grid.addWidget(QLabel("Input directory:"), 0, 0)
        self.input_directory_line_edit = QLineEdit()
        formulary_grid.addWidget(self.input_directory_line_edit, 0, 1)
        formulary_grid.addWidget(QPushButton("Browse"), 0, 2)
        formulary_grid.addWidget(QLabel("Output directory:"), 1, 0)
        self.output_directory_line_edit = QLineEdit()
        formulary_grid.addWidget(self.output_directory_line_edit, 1, 1)
        formulary_grid.addWidget(QLabel("Mapping file:"), 2, 0)
        self.mapping_file_line_edit = QLineEdit()
        formulary_grid.addWidget(self.mapping_file_line_edit, 2, 1)
        formulary_grid_widget.setLayout(formulary_grid)
        layout.addWidget(formulary_grid_widget)
        
        # Buttons
        self.button_map_file = QPushButton("Map file")
        self.button_map_file.setToolTip("Click to map the selected file.")
        self.button_map_file.clicked.connect(self._on_map_file)
        layout.addWidget(self.button_map_file)
        # self.button_map_file.setStyleSheet("background-color: #4CAF50; color: white; font-size: 15px; font-weight: bold; padding: 10px;")
        
        group_box.setLayout(layout)
        return group_box
    
    def _on_map_file(self):
        """Handle file mapping."""
        
        # Create the memory file if it doesn't exist and write the current state to it
        if not os.path.exists(self.MEMORY_FILE):
            os.makedirs(os.path.dirname(self.MEMORY_FILE), exist_ok=True)
        with open(self.MEMORY_FILE, 'w') as file:
            json_data = {
                'input_directory': self.input_directory_line_edit.text(),
                'output_directory': self.output_directory_line_edit.text(),
                'mapping_file': self.mapping_file_line_edit.text()
            }
            json.dump(json_data, file, indent=4)
        
        # TODO: Implement the mapping logic here.
        print("Mapping file...")
    
    
    def get_preferred_size(self) -> tuple[int, int]:
        """Returns the preferred size for this page.
        
        Returns:
            tuple: (width, height) in pixels
        """
        return self.PREFERRED_WIDTH, self.PREFERRED_HEIGHT
