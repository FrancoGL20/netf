"""
General helper functions for the application.
"""

def get_resource_path(relative_path: str) -> str:
    """
    Gets the absolute path of a resource.
    
    Args:
        relative_path (str): Relative path of the resource.
        
    Returns:
        str: Absolute path of the resource.
    """
    import os
    base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    return os.path.join(base_path, 'resources', relative_path)

def create_directory_if_not_exists(path: str) -> None:
    """
    Creates a directory if it doesn't exist.
    
    Args:
        path (str): Path of the directory to create.
    """
    import os
    if not os.path.exists(path):
        os.makedirs(path) 