"""
Reusable UI Components for Word Guessing Game
Contains LetterTile, Button, Grid, VirtualKeyboard, and NumberSelector
"""

import pygame
from . import constants
from .constants import (
    COLORS, TILE_SPACING, TILE_BORDER_WIDTH, SCREEN_WIDTH,
    BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_BORDER_RADIUS,
    NUMBER_BUTTON_SIZE, NUMBER_BUTTON_SPACING, GRID_TOP_MARGIN,
    KEYBOARD_ROWS, KEY_WIDTH, KEY_HEIGHT, KEY_SPACING, KEYBOARD_TOP_MARGIN,
    calculate_tile_size
)


class LetterTile:
    """Individual tile displaying a letter with color coding"""

    def __init__(self, letter, color_type, size, position):
        """
        Args:
            letter: The letter to display
            color_type: 'empty', 'absent', 'present', 'correct'
            size: Tile size in pixels
            position: (x, y) tuple for top-left corner
        """
        self.letter = letter.upper() if letter else None
        self.color_type = color_type
        self.size = size
        self.position = position

    def render(self, screen, scale_y=1.0, offset_x=0, offset_y=0, pop_scale=1.0):
        """Render the tile on the screen with optional animation transforms.

        Args:
            scale_y: Vertical scale 0.0-1.0 for flip animation
            offset_x: Horizontal pixel offset for shake animation
            offset_y: Vertical pixel offset for bounce animation
            pop_scale: Uniform scale factor for pop animation (e.g. 1.12)
        """
        x, y = self.position
        x += offset_x
        y += offset_y

        # Determine background color
        if self.color_type == 'correct':
            bg_color = COLORS['tile_correct']
        elif self.color_type == 'present':
            bg_color = COLORS['tile_present']
        elif self.color_type == 'absent':
            bg_color = COLORS['tile_absent']
        else:  # empty
            bg_color = COLORS['tile_empty']

        # Apply pop scale (uniform scale from center)
        size = self.size
        if pop_scale != 1.0:
            size = int(self.size * pop_scale)
            x -= (size - self.size) // 2
            y -= (size - self.size) // 2

        # Apply vertical scale for flip animation
        height = max(1, int(size * abs(scale_y)))
        y_center_offset = (size - height) // 2

        # Draw tile rectangle
        tile_rect = pygame.Rect(x, y + y_center_offset, size, height)
        pygame.draw.rect(screen, bg_color, tile_rect)
        pygame.draw.rect(screen, COLORS['border'], tile_rect, TILE_BORDER_WIDTH)

        # Draw letter if present and tile is tall enough to show text
        if self.letter and scale_y > 0.5:
            text_surface = constants.FONTS['tile'].render(self.letter, True, COLORS['text_white'])
            text_rect = text_surface.get_rect(center=(x + size // 2, y + size // 2))
            screen.blit(text_surface, text_rect)


class Button:
    """Interactive button with hover and click states"""

    def __init__(self, text, position, width=BUTTON_WIDTH, height=BUTTON_HEIGHT):
        """
        Args:
            text: Button label
            position: (x, y) tuple for top-left corner
            width: Button width
            height: Button height
        """
        self.text = text
        self.position = position
        self.width = width
        self.height = height
        self.rect = pygame.Rect(position[0], position[1], width, height)
        self.is_hovered = False

    def update(self, mouse_pos):
        """Update hover state based on mouse position"""
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, mouse_pos, mouse_pressed):
        """Check if button was clicked"""
        return self.rect.collidepoint(mouse_pos) and mouse_pressed[0]

    def render(self, screen):
        """Render the button"""
        # Determine color based on hover state
        color = COLORS['button_hover'] if self.is_hovered else COLORS['button_primary']

        # Draw button rectangle with rounded corners
        pygame.draw.rect(screen, color, self.rect, border_radius=BUTTON_BORDER_RADIUS)
        pygame.draw.rect(screen, COLORS['border'], self.rect, 2, border_radius=BUTTON_BORDER_RADIUS)

        # Draw text
        text_surface = constants.FONTS['normal'].render(self.text, True, COLORS['text_white'])
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)


class NumberSelector:
    """Row of number buttons for selecting attempts or length"""

    def __init__(self, min_val, max_val, default_val, position, label):
        """
        Args:
            min_val: Minimum value
            max_val: Maximum value
            default_val: Default selected value
            position: (x, y) tuple for top-left corner of the selector
            label: Label text to display above buttons
        """
        self.min_val = min_val
        self.max_val = max_val
        self.selected = default_val
        self.position = position
        self.label = label
        self.buttons = []

        # Create buttons for each number
        total_width = (max_val - min_val + 1) * (NUMBER_BUTTON_SIZE + NUMBER_BUTTON_SPACING) - NUMBER_BUTTON_SPACING
        start_x = position[0] - total_width // 2

        for i, num in enumerate(range(min_val, max_val + 1)):
            btn_x = start_x + i * (NUMBER_BUTTON_SIZE + NUMBER_BUTTON_SPACING)
            btn_y = position[1] + 40  # Below label
            self.buttons.append({
                'value': num,
                'rect': pygame.Rect(btn_x, btn_y, NUMBER_BUTTON_SIZE, NUMBER_BUTTON_SIZE)
            })

    def handle_click(self, mouse_pos, mouse_pressed):
        """Handle click events on number buttons"""
        if mouse_pressed[0]:
            for btn in self.buttons:
                if btn['rect'].collidepoint(mouse_pos):
                    self.selected = btn['value']
                    return True
        return False

    def render(self, screen):
        """Render the number selector"""
        # Draw label
        label_surface = constants.FONTS['normal'].render(self.label, True, COLORS['text_white'])
        label_rect = label_surface.get_rect(center=(self.position[0], self.position[1]))
        screen.blit(label_surface, label_rect)

        # Draw number buttons
        mouse_pos = pygame.mouse.get_pos()
        for btn in self.buttons:
            # Determine color
            if btn['value'] == self.selected:
                color = COLORS['button_selected']
            elif btn['rect'].collidepoint(mouse_pos):
                color = COLORS['button_hover']
            else:
                color = COLORS['button_primary']

            # Draw button
            pygame.draw.rect(screen, color, btn['rect'], border_radius=5)
            pygame.draw.rect(screen, COLORS['border'], btn['rect'], 2, border_radius=5)

            # Draw number
            text_surface = constants.FONTS['normal'].render(str(btn['value']), True, COLORS['text_white'])
            text_rect = text_surface.get_rect(center=btn['rect'].center)
            screen.blit(text_surface, text_rect)


class Grid:
    """Grid displaying all guess rows with color-coded tiles"""

    def __init__(self, max_attempts, word_length):
        """
        Args:
            max_attempts: Maximum number of attempts (rows)
            word_length: Length of the word (columns)
        """
        self.max_attempts = max_attempts
        self.word_length = word_length
        self.tile_size = calculate_tile_size(word_length, max_attempts)

        # Calculate grid position (centered)
        grid_width = word_length * (self.tile_size + TILE_SPACING) - TILE_SPACING
        self.start_x = (SCREEN_WIDTH - grid_width) // 2
        self.start_y = GRID_TOP_MARGIN

    def render(self, screen, guesses, current_input, anim_state=None):
        """
        Render the grid with all guesses and current input

        Args:
            guesses: List of dicts with 'word', 'match_indexes', 'right_indexes'
            current_input: Current input string being typed
            anim_state: Optional dict with active animation data
        """
        if anim_state is None:
            anim_state = {}

        for row in range(self.max_attempts):
            for col in range(self.word_length):
                x = self.start_x + col * (self.tile_size + TILE_SPACING)
                y = self.start_y + row * (self.tile_size + TILE_SPACING)

                # Determine letter and color for this tile
                letter = ''
                color_type = 'empty'

                if row < len(guesses):
                    # Previous guess
                    guess_data = guesses[row]
                    letter = guess_data['word'][col]

                    if col in guess_data['match_indexes']:
                        color_type = 'correct'
                    elif col in guess_data['right_indexes']:
                        color_type = 'present'
                    else:
                        color_type = 'absent'

                elif row == len(guesses) and col < len(current_input):
                    # Current input being typed
                    letter = current_input[col]
                    color_type = 'empty'

                # Compute animation transforms for this tile
                scale_y = 1.0
                offset_x = 0
                offset_y = 0
                pop_scale = 1.0

                # Flip animation (applies to the row that just flipped)
                flip_anim = anim_state.get('flip')
                if flip_anim and row == anim_state.get('flip_row'):
                    sy, show_color = flip_anim.get_tile_state(col)
                    scale_y = sy
                    if not show_color:
                        color_type = 'empty'  # Hide color during first half

                # Shake animation (applies to the current input row)
                shake_anim = anim_state.get('shake')
                if shake_anim and row == anim_state.get('shake_row'):
                    ox = shake_anim.get_offset_x()
                    if ox is not None:
                        offset_x = ox

                # Pop animation (applies to a single tile)
                pop_anim = anim_state.get('pop')
                if (pop_anim
                        and row == anim_state.get('pop_row')
                        and col == anim_state.get('pop_col')):
                    ps = pop_anim.get_scale()
                    if ps is not None:
                        pop_scale = ps

                # Bounce animation (applies to a row on win)
                bounce_anim = anim_state.get('bounce')
                if bounce_anim and row == anim_state.get('bounce_row'):
                    offset_y = bounce_anim.get_tile_offset_y(col)

                # Render tile with transforms
                tile = LetterTile(letter, color_type, self.tile_size, (x, y))
                tile.render(screen, scale_y=scale_y, offset_x=offset_x,
                            offset_y=offset_y, pop_scale=pop_scale)


class VirtualKeyboard:
    """On-screen keyboard with letter status tracking"""

    def __init__(self):
        """Initialize keyboard with default letter states"""
        self.letter_states = {letter: 'unused' for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'}
        self.keys = []
        self._create_keys()

    def _create_keys(self):
        """Create key rectangles based on keyboard layout"""
        self.keys = []
        y_offset = KEYBOARD_TOP_MARGIN

        for row_idx, row in enumerate(KEYBOARD_ROWS):
            # Calculate row width and starting x position
            row_width = len(row) * (KEY_WIDTH + KEY_SPACING) - KEY_SPACING
            x_offset = (SCREEN_WIDTH - row_width) // 2

            for col_idx, letter in enumerate(row):
                x = x_offset + col_idx * (KEY_WIDTH + KEY_SPACING)
                y = y_offset + row_idx * (KEY_HEIGHT + KEY_SPACING)

                self.keys.append({
                    'letter': letter,
                    'rect': pygame.Rect(x, y, KEY_WIDTH, KEY_HEIGHT)
                })

        # Add backspace and submit buttons on the same row as ZXCVBNM
        last_letter_row = KEYBOARD_ROWS[-1]  # ZXCVBNM
        last_row_y = y_offset + (len(KEYBOARD_ROWS) - 1) * (KEY_HEIGHT + KEY_SPACING)

        # Calculate the width of the letter keys in the last row
        last_row_width = len(last_letter_row) * (KEY_WIDTH + KEY_SPACING) - KEY_SPACING
        last_row_start_x = (SCREEN_WIDTH - last_row_width) // 2
        last_row_end_x = last_row_start_x + last_row_width

        # Submit button (left side of last row)
        submit_width = 65
        submit_x = last_row_start_x - submit_width - KEY_SPACING
        self.submit_button = Button("OK", (submit_x, last_row_y), width=submit_width, height=KEY_HEIGHT)

        # Backspace button (right side of last row) - custom rect, no text
        backspace_width = 65
        backspace_x = last_row_end_x + KEY_SPACING
        self.backspace_rect = pygame.Rect(backspace_x, last_row_y, backspace_width, KEY_HEIGHT)
        self.backspace_hovered = False

    def reset(self):
        """Reset all letter states for a new game"""
        self.letter_states = {letter: 'unused' for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'}

    def update_letter_states(self, guesses, guess_word):
        """
        Update letter states based on all guesses
        Priority: correct > present > absent > unused

        Args:
            guesses: List of guess data dicts
            guess_word: The target word
        """
        for guess_data in guesses:
            word = guess_data['word'].upper()
            match_indexes = guess_data['match_indexes']
            right_indexes = guess_data['right_indexes']

            for i, letter in enumerate(word):
                current_state = self.letter_states.get(letter, 'unused')

                # Determine new state with priority
                if i in match_indexes:
                    new_state = 'correct'
                elif i in right_indexes:
                    new_state = 'present'
                else:
                    new_state = 'absent'

                # Apply with priority: correct > present > absent > unused
                if current_state == 'unused':
                    self.letter_states[letter] = new_state
                elif current_state == 'absent' and new_state in ['present', 'correct']:
                    self.letter_states[letter] = new_state
                elif current_state == 'present' and new_state == 'correct':
                    self.letter_states[letter] = new_state

    def handle_click(self, mouse_pos, mouse_pressed):
        """
        Handle click events on keyboard keys
        Returns: Tuple (action_type, value) where action_type is 'letter', 'backspace', or 'submit'
        """
        if mouse_pressed[0]:
            # Check letter keys
            for key in self.keys:
                if key['rect'].collidepoint(mouse_pos):
                    return ('letter', key['letter'])

            # Check backspace
            if self.backspace_rect.collidepoint(mouse_pos):
                return ('backspace', None)

            # Check submit
            if self.submit_button.rect.collidepoint(mouse_pos):
                return ('submit', None)

        return (None, None)

    def render(self, screen, key_press_anim=None):
        """Render the virtual keyboard

        Args:
            key_press_anim: Optional KeyPressAnimation for visual feedback
        """
        mouse_pos = pygame.mouse.get_pos()

        # Render letter keys
        for key in self.keys:
            letter = key['letter']
            state = self.letter_states.get(letter, 'unused')

            # Determine color based on state
            if state == 'correct':
                color = COLORS['tile_correct']
            elif state == 'present':
                color = COLORS['tile_present']
            elif state == 'absent':
                color = COLORS['tile_absent']
            else:  # unused
                color = COLORS['key_unused']

            # Key press darkening effect
            if key_press_anim and letter == key_press_anim.key:
                darken = key_press_anim.get_darken_amount()
                if darken is not None:
                    color = tuple(max(c - darken, 0) for c in color)

            # Highlight on hover
            if key['rect'].collidepoint(mouse_pos):
                # Brighten the color
                color = tuple(min(c + 30, 255) for c in color)

            # Draw key
            pygame.draw.rect(screen, color, key['rect'], border_radius=4)
            pygame.draw.rect(screen, COLORS['border'], key['rect'], 2, border_radius=4)

            # Draw letter
            text_surface = constants.FONTS['key'].render(letter, True, COLORS['text_white'])
            text_rect = text_surface.get_rect(center=key['rect'].center)
            screen.blit(text_surface, text_rect)

        # Render backspace button with arrow icon
        self.backspace_hovered = self.backspace_rect.collidepoint(mouse_pos)
        backspace_color = COLORS['button_hover'] if  self.backspace_hovered else COLORS['button_primary']
        pygame.draw.rect(screen, backspace_color, self.backspace_rect, border_radius=4)
        pygame.draw.rect(screen, COLORS['border'], self.backspace_rect, 2, border_radius=4)

        # Draw backspace arrow icon (← with X)
        cx, cy = self.backspace_rect.center
        arrow_size = 12
        # Draw arrow pointing left with tail
        arrow_points = [
            (cx - arrow_size, cy),           # Arrow tip (left)
            (cx - arrow_size + 8, cy - 8),   # Top of arrow head
            (cx - arrow_size + 8, cy - 4),   # Top inner
            (cx + arrow_size - 4, cy - 4),   # Top right
            (cx + arrow_size - 4, cy + 4),   # Bottom right
            (cx - arrow_size + 8, cy + 4),   # Bottom inner
            (cx - arrow_size + 8, cy + 8),   # Bottom of arrow head
        ]
        pygame.draw.polygon(screen, COLORS['text_white'], arrow_points)
        # Draw small X on the arrow body
        x_offset = 6
        x_size = 4
        pygame.draw.line(screen, backspace_color, ((cx + x_offset - x_size)-5, cy - x_size), ((cx + x_offset + x_size)-5, cy + x_size), 2)
        pygame.draw.line(screen, backspace_color, ((cx + x_offset + x_size)-5, cy - x_size), ((cx + x_offset - x_size)-5, cy + x_size), 2)

        # Update and render submit button
        self.submit_button.update(mouse_pos)
        self.submit_button.render(screen)
