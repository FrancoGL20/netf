from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QGridLayout, QMessageBox, QGroupBox, QVBoxLayout
from PySide6.QtCore import Qt
from src.controllers.drop_duplicates_controller import DropDuplicatesController

class DropDuplicatesPage(QWidget):
    """Drop duplicated lines view"""
    
    def __init__(self):
        self.preferred_width = 400
        self.preferred_height = 300

        super().__init__()
        self.controller = DropDuplicatesController()
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
        layout = QGridLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setVerticalSpacing(20)
        
        # Title
        welcome_label = QLabel("Drop duplicated file lines.")
        welcome_label.setStyleSheet("font-size: 15px; font-weight: bold;")
        layout.addWidget(welcome_label, 0, 1)
        
        # File selection
        button_open_file = QPushButton("Open File")
        button_open_file.clicked.connect(self._on_file_select)
        button_open_file.setToolTip("Click to open a file dialog to select a file.")
        layout.addWidget(button_open_file, 1, 1)
        
        # File name display
        self.filename_label = QLabel("Selected file: None")
        self.filename_label.setMaximumWidth(self.preferred_width-20)
        layout.addWidget(self.filename_label, 2, 1)
        
        # Process button
        self.button_drop_duplicates = QPushButton("Process File")
        self.button_drop_duplicates.setEnabled(False)
        self.button_drop_duplicates.setToolTip("Click to process the selected file.")
        self.button_drop_duplicates.clicked.connect(self._on_process)
        layout.addWidget(self.button_drop_duplicates, 3, 1)

        group_box.setLayout(layout)
        return group_box
    
    
    def _on_file_select(self):
        """Handle file selection."""
        file_path = self.controller.select_file(self)
        if file_path:
            file_name = self.controller.get_file_name(file_path)
            self.filename_label.setText(f"Selected file: {file_name}")
            self.button_drop_duplicates.setEnabled(True)


    def _on_process(self):
        """Handle file processing."""
        try:
            result = self.controller.process_selected_file()
            self._show_success_message(result)
        except Exception as e:
            self._show_error_message(str(e))


    def _show_success_message(self, result):
        """Display success message with results."""
        original_lines, new_lines = result
        QMessageBox.information(
            self, 
            "Process Result",
            f"Original lines: {original_lines}\nNew lines: {new_lines}"
        )
    
    
    def _show_error_message(self, error):
        """Display error message."""
        QMessageBox.critical(self, "Error", f"Error processing file: {error}")
    
    
    def get_preferred_size(self) -> tuple[int, int]:
        """Returns the preferred size for this page.
        
        Returns:
            tuple: (width, height) in pixels
        """
        return self.preferred_width, self.preferred_height
