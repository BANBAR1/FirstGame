"""
UI Constants for Word Guessing Game
Contains colors, dimensions, fonts, and layout configurations
"""

import pygame

# Screen dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
FPS = 60

# Colors (Wordle-inspired dark theme)
COLORS = {
    'background': (18, 18, 19),          # Dark background
    'tile_empty': (58, 58, 60),          # Empty tile
    'tile_absent': (58, 58, 60),         # Letter not in word (gray)
    'tile_present': (181, 159, 59),      # Letter in word, wrong position (yellow)
    'tile_correct': (83, 141, 78),       # Letter in correct position (green)
    'text_white': (255, 255, 255),
    'text_black': (0, 0, 0),
    'border': (86, 87, 88),
    'error': (220, 50, 50),
    'button_primary': (70, 130, 180),
    'button_hover': (100, 149, 237),
    'button_selected': (50, 100, 150),
    'key_unused': (129, 131, 132),       # Keyboard key not yet used
}

# Tile dimensions
TILE_SIZE_BASE = 70
TILE_SPACING = 8
TILE_BORDER_WIDTH = 2

# Grid positioning
GRID_TOP_MARGIN = 120
GRID_BOTTOM_MARGIN = 300

# Keyboard layout
KEYBOARD_ROWS = [
    'QWERTYUIOP',
    'ASDFGHJKL',
    'ZXCVBNM'
]
KEY_WIDTH = 45
KEY_HEIGHT = 58
KEY_SPACING = 6
KEYBOARD_TOP_MARGIN = 520

# Button dimensions
BUTTON_WIDTH = 150
BUTTON_HEIGHT = 50
BUTTON_BORDER_RADIUS = 8

# Number selector dimensions
NUMBER_BUTTON_SIZE = 50
NUMBER_BUTTON_SPACING = 10

# Fonts (will be initialized after pygame.init())
FONTS = None

def init_fonts():
    """Initialize pygame fonts after pygame.init() is called"""
    global FONTS
    pygame.font.init()
    FONTS = {
        'title': pygame.font.Font(None, 48),
        'header': pygame.font.Font(None, 36),
        'normal': pygame.font.Font(None, 28),
        'tile': pygame.font.Font(None, 36),
        'small': pygame.font.Font(None, 20),
        'key': pygame.font.Font(None, 24),
    }

def calculate_tile_size(word_length, max_attempts=6):
    """Calculate tile size based on word length and attempts to fit screen"""
    # Calculate max size based on width
    max_width = SCREEN_WIDTH - 100  # Leave margins
    tile_from_width = (max_width / word_length) - TILE_SPACING

    # Calculate max size based on height
    # Available height = keyboard start - grid top - input area
    available_height = KEYBOARD_TOP_MARGIN - GRID_TOP_MARGIN - 70  # 70px for input area
    tile_from_height = (available_height / max_attempts) - TILE_SPACING

    # Use the smaller of the two to ensure it fits both ways
    return min(TILE_SIZE_BASE, tile_from_width, tile_from_height)


# Animation timing constants (seconds)
FLIP_DURATION = 0.3
FLIP_STAGGER = 0.15
POP_DURATION = 0.1
POP_MAX_SCALE = 1.12
SHAKE_DURATION = 0.4
SHAKE_AMPLITUDE = 10
BOUNCE_DURATION = 0.5
BOUNCE_STAGGER = 0.1
BOUNCE_AMPLITUDE = 30
KEY_PRESS_DURATION = 0.1
FADE_DURATION = 0.25
