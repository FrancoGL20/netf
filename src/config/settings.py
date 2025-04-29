"""
Global application settings.
"""

import os

# Application settings
APP_NAME = "NetF"
APP_VERSION = "1.0.0"
APP_AUTHOR = "Francisco Gutiérrez López"
APP_AUTHOR_GITHUB = "https://github.com/FrancoGL20"

# Main window settings
WINDOW_MIN_WIDTH = 800
WINDOW_MIN_HEIGHT = 600

# Paths
PATH_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PATH_SRC = os.path.join(PATH_ROOT, 'src')
PATH_IMAGES = os.path.join(PATH_SRC, 'assets', 'images')
PATH_ICONS = os.path.join(PATH_SRC, 'assets', 'icons')
