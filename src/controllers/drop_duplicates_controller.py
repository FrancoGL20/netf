import os
from src.utils.drop_duplicates import drop_duplicates
from PySide6.QtWidgets import QWidget, QFileDialog

class DropDuplicatesController:
    """Controller to process the removal of duplicate lines."""

    def __init__(self):
        self.selected_file = None
        self.output_dir = "./Processed_Files/Drop_Duplicates"

    
    def select_file(self, parent: QWidget) -> str:
        """
        Handle file selection dialog.
        
        Args:
            parent: Parent widget for the dialog
            
        Returns:
            str: Selected file path or empty string if cancelled
        """
        file_path, _ = QFileDialog.getOpenFileName(
            parent, 
            "Open File",
            "", 
            "All Files (*)"
        )
        
        if file_path:
            self.selected_file = file_path
            print(f"Selected file: {file_path}")
            
        return file_path


    def get_file_name(self, file_path: str) -> str:
        """Extract file name from path."""
        return os.path.basename(file_path)


    def process_selected_file(self) -> tuple[int, int]:
        """
        Process the currently selected file.
        
        Returns:
            tuple[int, int]: Original and new line counts
            
        Raises:
            ValueError: If no file is selected
        """
        if not self.selected_file:
            raise ValueError("No file selected")

        file_name = self.get_file_name(self.selected_file)
        output_filename = f"processed_{file_name}"
        
        return drop_duplicates(self.selected_file, output_filename, self.output_dir)