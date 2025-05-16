"""
Global application settings.
"""

from pathlib import Path

# Application settings
APP_NAME = "NetF"
APP_VERSION = "1.0.0"
APP_AUTHOR = "Francisco Gutiérrez López"
APP_AUTHOR_GITHUB = "https://github.com/FrancoGL20"

# Main window settings
WINDOW_MIN_WIDTH = 800
WINDOW_MIN_HEIGHT = 600

# Paths
path_root = Path(__file__).parent.parent.parent
PATH_ROOT = path_root.as_posix()
PATH_SRC = path_root.joinpath('src').as_posix()
PATH_IMAGES = path_root.joinpath('assets', 'images').as_posix()
PATH_ICONS = path_root.joinpath('assets', 'icons').as_posix()

