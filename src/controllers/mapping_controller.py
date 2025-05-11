import os
import json
from pathlib import Path
from src.config.settings import PATH_ROOT

class MappingController:
    """Controller for mapping XML templates."""
    
    def __init__(self):
        self._MEMORY_FILE = os.path.join(PATH_ROOT,'.memory','mapping.json')

    def get_memory_content(self):
        """Get the memory content from the App memory file."""
        
        # Get the memory content from the App memory file
        if Path(self._MEMORY_FILE).exists():
            with open(self._MEMORY_FILE, 'r') as file:
                data = json.load(file)
                return data
        
        return None
    
    def save_memory_content(self, data):
        """Save the memory content to the App memory file."""
        
        # Create the memory file directory if it doesn't exist
        MEMORY_FILE_DIR = os.path.dirname(self._MEMORY_FILE)
        if not Path(MEMORY_FILE_DIR).exists():
            Path(MEMORY_FILE_DIR).mkdir(parents=True, exist_ok=True)
        
        # Save the memory content to the App memory file
        with open(self._MEMORY_FILE, 'w') as file:
            json.dump(data, file)