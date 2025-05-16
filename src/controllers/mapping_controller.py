import json
from pathlib import Path
from src.config.settings import PATH_ROOT
from src.utils.xml_files_processing import map_ids
from PySide6.QtCore import QThread


class MappingController:
    """Controller for mapping XML templates."""
    

    def __init__(self):
        self._MEMORY_FILE = Path(PATH_ROOT,'.memory','mapping.json')


    def get_memory_content(self):
        """Get the memory content from the App memory file."""
        
        # Get the memory content from the App memory file
        if self._MEMORY_FILE.exists():
            with open(self._MEMORY_FILE, 'r') as file:
                data = json.load(file)
                return data
        
        return None
    

    def save_memory_content(self, data):
        """Save the memory content to the App memory file."""
        
        # Create the memory file directory if it doesn't exist
        MEMORY_FILE_DIR = Path(self._MEMORY_FILE).parent
        if not MEMORY_FILE_DIR.exists():
            MEMORY_FILE_DIR.mkdir(parents=True, exist_ok=True)
        
        # Save the memory content to the App memory file
        with open(self._MEMORY_FILE, 'w') as file:
            json.dump(data, file)
    

    def map_ids(self, file_with_mapping: str, file_to_map: str, dir_output: str, columns_to_map: str|list[str] = ["TM Tariff ID", "Tariff ID", "TariffCode"], unmap: bool = False, has_details: bool = False):
        """Map IDs of and xml excel spreadsheet 2003 file."""
        
        # Map IDs
        result = map_ids(
            file_with_mapping=file_with_mapping,
            file_to_map=file_to_map,
            dir_output=dir_output,
            columns_to_map=columns_to_map,
            unmap=unmap,
            has_details=has_details
        )
        
        return result