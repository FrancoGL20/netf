from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QGroupBox, QVBoxLayout, QFormLayout, QLineEdit, QGridLayout, QFileDialog
from PySide6.QtCore import Qt
from src.config.settings import PATH_ROOT
import os, json

class MappingPage(QWidget):
    """Mapping xml templates function view."""
    
    def __init__(self, main_window=None):
        self.PREFERRED_WIDTH = 1000
        self.PREFERRED_HEIGHT = 450
        self._MEMORY_FILE = os.path.join(PATH_ROOT,'.memory','mapping.json')
        self.main_window = main_window

        super().__init__()
        self._setup_ui()

    def resize_main_window(self, width: int, height: int, fixed: bool = False):
        """Resize the parent window if available."""
        
        if self.main_window:
            self.main_window.resize_window(width, height, fixed)
    
    def _setup_ui(self):
        """Configure the user interface."""
        
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        
        group_box = self._create_group_box()
        self.main_layout.addWidget(group_box)
        
        self._update_ui_with_memory()
    
    
    def _update_ui_with_memory(self):
        """Update the UI with the memory file data."""
        
        if os.path.exists(self._MEMORY_FILE):
            with open(self._MEMORY_FILE, 'r') as file:
                data = json.load(file)

                # Update UI elements with data from the memory file
                self.input_directory_line_edit.setText(data.get('input_directory', ''))
                self.output_directory_line_edit.setText(data.get('output_directory', ''))
                self.mapping_file_line_edit.setText(data.get('mapping_file', ''))
                self.file_to_map_line_edit.setText(data.get('file_to_map', ''))
    
    
    def _create_group_box(self):
        """Create and configure the main group box."""
        
        # Window widget and layout
        group_box = QGroupBox()
        page_layout = QVBoxLayout()
        page_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Title
        label_welcome = QLabel("Mapping xml templates function.")
        label_welcome.setStyleSheet("font-size: 15px; font-weight: bold; margin-bottom: 20px;")
        label_welcome.setAlignment(Qt.AlignmentFlag.AlignCenter)
        page_layout.addWidget(label_welcome)
        
        # Formulary widget - Start
        formulary_widget = QWidget()
        formulary_grid_layout = QGridLayout()
        formulary_grid_layout.setVerticalSpacing(15)
        
        # Input directory
        formulary_grid_layout.addWidget(QLabel("Input directory:"), 0, 0)
        self.input_directory_line_edit = QLineEdit()
        formulary_grid_layout.addWidget(self.input_directory_line_edit, 0, 1)
        button_browse_input_dir = QPushButton("Browse")
        button_browse_input_dir.clicked.connect(lambda: self._on_browse(0))
        button_browse_input_dir.setToolTip("Click to select the input directory.")
        formulary_grid_layout.addWidget(button_browse_input_dir, 0, 2)
        
        # Output directory
        formulary_grid_layout.addWidget(QLabel("Output directory:"), 1, 0)
        self.output_directory_line_edit = QLineEdit()
        formulary_grid_layout.addWidget(self.output_directory_line_edit, 1, 1)
        button_browse_output_dir = QPushButton("Browse")
        button_browse_output_dir.clicked.connect(lambda: self._on_browse(1))
        button_browse_output_dir.setToolTip("Click to select the output directory.")
        formulary_grid_layout.addWidget(button_browse_output_dir, 1, 2)
        
        # Mapping file
        formulary_grid_layout.addWidget(QLabel("Mapping file:"), 2, 0)
        self.mapping_file_line_edit = QLineEdit()
        formulary_grid_layout.addWidget(self.mapping_file_line_edit, 2, 1)
        button_browse_mapping_file = QPushButton("Browse")
        button_browse_mapping_file.clicked.connect(lambda: self._on_browse(2))
        button_browse_mapping_file.setToolTip("Click to select the mapping file.")
        formulary_grid_layout.addWidget(button_browse_mapping_file, 2, 2)
        
        # File to map
        formulary_grid_layout.addWidget(QLabel("File to map:"), 3, 0)
        self.file_to_map_line_edit = QLineEdit()
        formulary_grid_layout.addWidget(self.file_to_map_line_edit, 3, 1)
        button_browse_file_to_map = QPushButton("Browse")
        button_browse_file_to_map.clicked.connect(lambda: self._on_browse(3))
        button_browse_file_to_map.setToolTip("Click to select the file to map.")
        formulary_grid_layout.addWidget(button_browse_file_to_map, 3, 2)

        # Formulary widget - End
        formulary_widget.setLayout(formulary_grid_layout)
        page_layout.addWidget(formulary_widget)
        
        # Buttons
        self.button_map_file = QPushButton("Map file")
        self.button_map_file.setStyleSheet("font-size: 12px; font-weight: bold; padding-top: 8px; padding-bottom: 8px; margin-top: 20px; margin-left: 15px; margin-right: 15px;")
        self.button_map_file.clicked.connect(self._on_map_file)
        page_layout.addWidget(self.button_map_file)
        
        group_box.setLayout(page_layout)
        return group_box
    
    
    def _on_browse(self, line_edit_index: int):
        """Handle the browse button click for the input, output, and mapping file."""
        
        if line_edit_index == 0:
            # Browse for input directory
            directory = QFileDialog.getExistingDirectory(self, "Select Input Directory")
            if directory:
                self.input_directory_line_edit.setText(directory)
        elif line_edit_index == 1:
            # Browse for output directory
            directory = QFileDialog.getExistingDirectory(self, "Select Output Directory")
            if directory:
                self.output_directory_line_edit.setText(directory)
        elif line_edit_index == 2:
            # Browse for mapping file
            file_name, _ = QFileDialog.getOpenFileName(self, "Select Mapping File", "", "Excel Files (*.xlsx)")
            if file_name:
                self.mapping_file_line_edit.setText(file_name)
        elif line_edit_index == 3:
            # Browse for file to map
            file_name, _ = QFileDialog.getOpenFileName(self, "Select File to Map", "", "XML Files (*.xml)")
            # Extract the file name from the path
            file_name = os.path.basename(file_name)
            if file_name:
                self.file_to_map_line_edit.setText(file_name)
    
    
    def _on_map_file(self):
        """Handle file mapping."""
        
        # Create the memory file if it doesn't exist and write the current state to it
        if not os.path.exists(self._MEMORY_FILE):
            os.makedirs(os.path.dirname(self._MEMORY_FILE), exist_ok=True)
        with open(self._MEMORY_FILE, 'w') as file:
            json_data = {
                'input_directory': self.input_directory_line_edit.text(),
                'output_directory': self.output_directory_line_edit.text(),
                'mapping_file': self.mapping_file_line_edit.text(),
                'file_to_map': self.file_to_map_line_edit.text()
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
