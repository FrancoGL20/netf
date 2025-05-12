from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QGroupBox, QVBoxLayout, QLineEdit, QGridLayout, QFileDialog, QCheckBox, QHBoxLayout
from PySide6.QtCore import Qt
from src.config.settings import PATH_ROOT
from src.controllers.mapping_controller import MappingController
from pathlib import Path

class MappingPage(QWidget):
    """Mapping xml templates function view."""
    
    def __init__(self, main_window=None):
        self.PREFERRED_WIDTH = 1000
        self.PREFERRED_HEIGHT = 450
        self.COLUMNS_TO_MAP=["TM Tariff ID","Tariff ID","TariffCode"]
        self.JSON_DIR_OUTPUT = 'directory_output'
        self.JSON_FILE_MAPPING = 'file_mapping'
        self.JSON_FILE_TO_MAP = 'file_to_map'
        self.JSON_CHECKBOX_DETAILS = 'checkbox_details'
        self.JSON_CHECKBOX_UNMAP = 'checkbox_unmap'
        self.JSON_CHECKBOX_CUSTOM_COLUMN_TO_MAP = 'checkbox_custom_column_to_map'
        
        self.main_window = main_window
        self.controller = MappingController()

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

        memory_content=self.controller.get_memory_content()

        # Update UI elements with data from the memory file
        if memory_content:
            data = memory_content

            # Update UI elements with data from the memory file
            self.output_directory_line_edit.setText(data.get(self.JSON_DIR_OUTPUT, ''))
            self.mapping_file_line_edit.setText(data.get(self.JSON_FILE_MAPPING, ''))
            self.file_to_map_line_edit.setText(data.get(self.JSON_FILE_TO_MAP, ''))
            self.checkbox_details.setChecked(data.get(self.JSON_CHECKBOX_DETAILS, False))
            self.checkbox_unmap.setChecked(data.get(self.JSON_CHECKBOX_UNMAP, False))
            self.checkbox_custom_column_to_map.setChecked(data.get(self.JSON_CHECKBOX_CUSTOM_COLUMN_TO_MAP, False))
    
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
        
        # File to map
        formulary_grid_layout.addWidget(QLabel("File to map:"), 1, 0)
        self.file_to_map_line_edit = QLineEdit()
        formulary_grid_layout.addWidget(self.file_to_map_line_edit, 1, 1)
        button_browse_file_to_map = QPushButton("Browse")
        button_browse_file_to_map.clicked.connect(lambda: self._on_browse(1))
        button_browse_file_to_map.setToolTip("Click to select the file to map.")
        formulary_grid_layout.addWidget(button_browse_file_to_map, 1, 2)
        
        # Output directory
        formulary_grid_layout.addWidget(QLabel("Output directory:"), 2, 0)
        self.output_directory_line_edit = QLineEdit()
        formulary_grid_layout.addWidget(self.output_directory_line_edit, 2, 1)
        button_browse_output_dir = QPushButton("Browse")
        button_browse_output_dir.clicked.connect(lambda: self._on_browse(2))
        button_browse_output_dir.setToolTip("Click to select the output directory.")
        formulary_grid_layout.addWidget(button_browse_output_dir, 2, 2)
        
        # Mapping file
        formulary_grid_layout.addWidget(QLabel("Mapping file:"), 3, 0)
        self.mapping_file_line_edit = QLineEdit()
        formulary_grid_layout.addWidget(self.mapping_file_line_edit, 3, 1)
        button_browse_mapping_file = QPushButton("Browse")
        button_browse_mapping_file.clicked.connect(lambda: self._on_browse(3))
        button_browse_mapping_file.setToolTip("Click to select the mapping file.")
        formulary_grid_layout.addWidget(button_browse_mapping_file, 3, 2)
        
        # Formulary widget - End
        formulary_widget.setLayout(formulary_grid_layout)
        page_layout.addWidget(formulary_widget)

        # Group of checkboxes
        checkbox_group=QWidget()
        checkbox_layout=QHBoxLayout()
        checkbox_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        checkbox_layout.setSpacing(50)
        checkbox_group.setLayout(checkbox_layout)
        # Checkbox for details
        self.checkbox_details = QCheckBox("Has details")
        self.checkbox_details.setToolTip("Check if the file to map has details.")
        checkbox_layout.addWidget(self.checkbox_details)
        # Checkbox for unmap
        self.checkbox_unmap = QCheckBox("Unmap")
        self.checkbox_unmap.setToolTip("Check if you want to unmap the file.")
        checkbox_layout.addWidget(self.checkbox_unmap)
        # Checkbox for custom column to map
        self.checkbox_custom_column_to_map = QCheckBox("Custom column to map")
        self.checkbox_custom_column_to_map.setToolTip("Check if you want to map a custom column (other than \"TM Tariff ID\",\"Tariff ID\",\"TariffCode\").")
        self.checkbox_custom_column_to_map.checkStateChanged.connect(self._on_custom_column_to_map)
        checkbox_layout.addWidget(self.checkbox_custom_column_to_map)
        # Line edit for custom column to map
        self.line_edit_custom_column_to_map = QLineEdit()
        self.line_edit_custom_column_to_map.setPlaceholderText("Custom column to map")
        self.line_edit_custom_column_to_map.setToolTip("Disabled")
        self.line_edit_custom_column_to_map.setEnabled(False)
        checkbox_layout.addWidget(self.line_edit_custom_column_to_map)
        # Group of checkboxes - End
        page_layout.addWidget(checkbox_group)
        
        # Buttons
        self.button_map_file = QPushButton("Map file")
        self.button_map_file.setStyleSheet("font-size: 12px; font-weight: bold; padding-top: 8px; padding-bottom: 8px; margin-top: 20px; margin-left: 15px; margin-right: 15px;")
        self.button_map_file.clicked.connect(self._on_map_file)
        page_layout.addWidget(self.button_map_file)
        
        group_box.setLayout(page_layout)
        return group_box
    
    
    def _on_browse(self, line_edit_index: int):
        """Handle the browse button click for the output and mapping file."""
        
        if line_edit_index == 1:
            # Browse for file to map
            file_name, _ = QFileDialog.getOpenFileName(self, "Select File to Map", "", "XML Files (*.xml)")
            file_name = Path(file_name)
            if file_name:
                self.file_to_map_line_edit.setText(file_name.as_posix())
        elif line_edit_index == 2:
            # Browse for output directory
            directory = Path(QFileDialog.getExistingDirectory(self, "Select Output Directory"))
            if directory:
                self.output_directory_line_edit.setText(directory.as_posix())
        elif line_edit_index == 3:
            # Browse for mapping file
            file_name, _ = QFileDialog.getOpenFileName(self, "Select Mapping File", "", "Excel Files (*.xlsx)")
            file_name = Path(file_name)
            if file_name:
                self.mapping_file_line_edit.setText(file_name.as_posix())
    
    
    def _on_map_file(self):
        """Handle file mapping."""
        
        # Save memory content
        JSON_DATA = {
            self.JSON_DIR_OUTPUT: self.output_directory_line_edit.text(),
            self.JSON_FILE_MAPPING: self.mapping_file_line_edit.text(),
            self.JSON_FILE_TO_MAP: self.file_to_map_line_edit.text(),
            self.JSON_CHECKBOX_DETAILS: self.checkbox_details.isChecked(),
            self.JSON_CHECKBOX_UNMAP: self.checkbox_unmap.isChecked(),
            self.JSON_CHECKBOX_CUSTOM_COLUMN_TO_MAP: self.checkbox_custom_column_to_map.isChecked()
        }
        self.controller.save_memory_content(JSON_DATA)
        
        # TODO: Implement the mapping logic here.
        print("Mapping file...")
    
    def _on_custom_column_to_map(self):
        """Handle custom column to map checkbox state change."""
        
        self.line_edit_custom_column_to_map.setEnabled(self.checkbox_custom_column_to_map.isChecked())
        self.line_edit_custom_column_to_map.setToolTip("Disabled" if not self.checkbox_custom_column_to_map.isChecked() else "Specify the column name to map")

    def get_preferred_size(self) -> tuple[int, int]:
        """Returns the preferred size for this page.
        
        Returns:
            tuple: (width, height) in pixels
        """
        return self.PREFERRED_WIDTH, self.PREFERRED_HEIGHT
