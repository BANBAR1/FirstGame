"""
Animation classes for Word Guessing Game
Provides tile flip, pop, shake, bounce, key press, and screen fade animations.
"""

import math
import time

from .constants import (
    FLIP_DURATION, FLIP_STAGGER,
    POP_DURATION, POP_MAX_SCALE,
    SHAKE_DURATION, SHAKE_AMPLITUDE,
    BOUNCE_DURATION, BOUNCE_STAGGER, BOUNCE_AMPLITUDE,
    KEY_PRESS_DURATION,
    FADE_DURATION,
)


class TileFlipAnimation:
    """Tiles flip one-by-one to reveal their colors after a guess."""

    def __init__(self, num_tiles):
        self.num_tiles = num_tiles
        self.start_time = time.time()

    def get_tile_state(self, tile_index):
        """Return (scale_y, show_color) for a given tile.

        scale_y: 1.0 → 0.0 → 1.0 (vertical squash for flip effect)
        show_color: False during first half, True during second half
        """
        elapsed = time.time() - self.start_time
        tile_start = tile_index * FLIP_STAGGER
        tile_elapsed = elapsed - tile_start

        if tile_elapsed < 0:
            return 1.0, False  # Not started yet
        if tile_elapsed >= FLIP_DURATION:
            return 1.0, True   # Finished

        progress = tile_elapsed / FLIP_DURATION
        if progress < 0.5:
            # First half: shrinking (shows uncolored tile)
            scale = 1.0 - progress * 2
            return scale, False
        else:
            # Second half: growing (shows colored tile)
            scale = (progress - 0.5) * 2
            return scale, True

    @property
    def is_complete(self):
        elapsed = time.time() - self.start_time
        return elapsed >= (self.num_tiles - 1) * FLIP_STAGGER + FLIP_DURATION


class TilePopAnimation:
    """Brief scale-up pulse when a letter is typed."""

    def __init__(self):
        self.start_time = time.time()

    def get_scale(self):
        elapsed = time.time() - self.start_time
        if elapsed >= POP_DURATION:
            return None  # Animation finished
        progress = elapsed / POP_DURATION
        return 1.0 + (POP_MAX_SCALE - 1.0) * math.sin(progress * math.pi)


class RowShakeAnimation:
    """Horizontal shake for invalid input — decaying oscillation."""

    def __init__(self):
        self.start_time = time.time()

    def get_offset_x(self):
        elapsed = time.time() - self.start_time
        if elapsed >= SHAKE_DURATION:
            return None  # Animation finished
        progress = elapsed / SHAKE_DURATION
        decay = 1.0 - progress
        return int(SHAKE_AMPLITUDE * decay * math.sin(progress * math.pi * 6))


class WinBounceAnimation:
    """Winning row tiles bounce up in sequence."""

    def __init__(self, num_tiles):
        self.num_tiles = num_tiles
        self.start_time = time.time()

    def get_tile_offset_y(self, tile_index):
        elapsed = time.time() - self.start_time
        tile_start = tile_index * BOUNCE_STAGGER
        tile_elapsed = elapsed - tile_start

        if tile_elapsed < 0:
            return 0
        if tile_elapsed >= BOUNCE_DURATION:
            return 0

        progress = tile_elapsed / BOUNCE_DURATION
        # Damped bounce: two peaks that decrease in height
        return int(-BOUNCE_AMPLITUDE * abs(math.sin(progress * math.pi * 2)) * (1.0 - progress))

    @property
    def is_complete(self):
        elapsed = time.time() - self.start_time
        return elapsed >= (self.num_tiles - 1) * BOUNCE_STAGGER + BOUNCE_DURATION


class KeyPressAnimation:
    """Brief darkening of a virtual keyboard key when pressed."""

    def __init__(self, key):
        self.key = key.upper()
        self.start_time = time.time()

    def get_darken_amount(self):
        elapsed = time.time() - self.start_time
        if elapsed >= KEY_PRESS_DURATION:
            return None  # Animation finished
        progress = elapsed / KEY_PRESS_DURATION
        return int(50 * (1.0 - progress))


class ScreenFadeTransition:
    """Two-phase fade: out to black, then in from black."""

    def __init__(self):
        self.start_time = time.time()
        self.phase = 'out'  # 'out' fading to black, 'in' fading from black
        self.midpoint_reached = False
        self.active = True

    def get_alpha(self):
        elapsed = time.time() - self.start_time

        if self.phase == 'out':
            if elapsed >= FADE_DURATION:
                self.phase = 'in'
                self.start_time = time.time()
                self.midpoint_reached = True
                return 255
            return int(255 * (elapsed / FADE_DURATION))
        else:
            if elapsed >= FADE_DURATION:
                self.active = False
                return 0
            return int(255 * (1.0 - elapsed / FADE_DURATION))
