"""
Game Screen for Word Guessing Game
Main gameplay interface with grid, input, and virtual keyboard
"""

import pygame
from . import constants
from .constants import COLORS, SCREEN_WIDTH, SCREEN_HEIGHT, GRID_TOP_MARGIN, TILE_SPACING
from .ui_components import Grid, VirtualKeyboard
from .animations import TileFlipAnimation, TilePopAnimation, RowShakeAnimation, KeyPressAnimation


class GameScreen:
    """Main game screen with word grid and keyboard"""

    def __init__(self):
        """Initialize game screen"""
        self.grid = None
        self.virtual_keyboard = VirtualKeyboard()
        self.error_message = ""
        self.error_timer = 0  # Timer to fade out error message

        # Animation state
        self.flip_animation = None
        self.flip_row = -1
        self.pop_animation = None
        self.pop_row = -1
        self.pop_col = -1
        self.shake_animation = None
        self.shake_row = -1
        self.key_press_animation = None
        self.pending_state = None   # Deferred WIN/LOSE during flip
        self.animating = False      # Block input during flip

    def initialize_grid(self, max_attempts, word_length):
        """
        Initialize grid with game parameters

        Args:
            max_attempts: Maximum number of attempts
            word_length: Length of the word
        """
        self.grid = Grid(max_attempts, word_length)
        self.virtual_keyboard.reset()
        self.error_message = ""
        self._clear_animations()

    def _clear_animations(self):
        """Reset all animation state"""
        self.flip_animation = None
        self.pop_animation = None
        self.shake_animation = None
        self.key_press_animation = None
        self.pending_state = None
        self.animating = False

    def _start_pop(self, game_manager, col):
        """Start a pop animation on the tile that just received a letter."""
        self.pop_animation = TilePopAnimation()
        self.pop_row = len(game_manager.guesses)
        self.pop_col = col

    def handle_event(self, event, game_manager):
        """
        Handle events for the game screen

        Args:
            event: Pygame event
            game_manager: GameManager instance
        """
        # Block input during flip animation
        if self.animating:
            return

        # Handle physical keyboard input
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                self._submit_guess(game_manager)

            elif event.key == pygame.K_BACKSPACE:
                if game_manager.current_input:
                    game_manager.current_input = game_manager.current_input[:-1]
                    self.error_message = ""

            elif event.key == pygame.K_ESCAPE:
                game_manager.reset_game()

            else:
                if event.unicode.isalpha() and len(game_manager.current_input) < game_manager.word_length:
                    letter = event.unicode.upper()
                    game_manager.current_input += letter
                    self.error_message = ""
                    # Start pop and key press animations
                    self._start_pop(game_manager, len(game_manager.current_input) - 1)
                    self.key_press_animation = KeyPressAnimation(letter)

        # Handle virtual keyboard clicks
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            action_type, value = self.virtual_keyboard.handle_click(mouse_pos, mouse_pressed)

            if action_type == 'letter':
                if len(game_manager.current_input) < game_manager.word_length:
                    game_manager.current_input += value
                    self.error_message = ""
                    self._start_pop(game_manager, len(game_manager.current_input) - 1)
                    self.key_press_animation = KeyPressAnimation(value)

            elif action_type == 'backspace':
                if game_manager.current_input:
                    game_manager.current_input = game_manager.current_input[:-1]
                    self.error_message = ""

            elif action_type == 'submit':
                self._submit_guess(game_manager)

    def _submit_guess(self, game_manager):
        """
        Submit the current guess and process it

        Args:
            game_manager: GameManager instance
        """
        if not game_manager.current_input:
            return

        # Remember which row this guess will land on
        guess_row = len(game_manager.guesses)

        success, error = game_manager.submit_guess(game_manager.current_input)

        if not success:
            # Show error and start shake animation on the current input row
            self.error_message = error
            self.error_timer = 180
            self.shake_animation = RowShakeAnimation()
            self.shake_row = guess_row
        else:
            self.error_message = ""
            game_manager.current_input = ""

            # Start flip animation on the just-submitted row
            self.flip_animation = TileFlipAnimation(game_manager.word_length)
            self.flip_row = guess_row
            self.animating = True

            # Defer state transition until flip animation finishes
            from words_guessing_game_banbar1.main_game_func import GameState
            if game_manager.state in (GameState.WIN, GameState.LOSE):
                self.pending_state = game_manager.state
                game_manager.state = GameState.PLAYING

            # Update virtual keyboard states
            self.virtual_keyboard.update_letter_states(game_manager.guesses, game_manager.guess_word)

    def update(self, game_manager):
        """
        Update game screen state

        Args:
            game_manager: GameManager instance
        """
        # Fade out error message
        if self.error_timer > 0:
            self.error_timer -= 1
            if self.error_timer == 0:
                self.error_message = ""

        # Check if flip animation completed
        if self.flip_animation and self.flip_animation.is_complete:
            self.flip_animation = None
            self.animating = False
            # Apply deferred state transition
            if self.pending_state is not None:
                game_manager.state = self.pending_state
                self.pending_state = None

        # Clean up finished pop animation
        if self.pop_animation and self.pop_animation.get_scale() is None:
            self.pop_animation = None

        # Clean up finished shake animation
        if self.shake_animation and self.shake_animation.get_offset_x() is None:
            self.shake_animation = None

        # Clean up finished key press animation
        if self.key_press_animation and self.key_press_animation.get_darken_amount() is None:
            self.key_press_animation = None

    def render(self, screen, game_manager):
        """
        Render the game screen

        Args:
            screen: Pygame screen surface
            game_manager: GameManager instance
        """
        # Clear screen
        screen.fill(COLORS['background'])

        # Draw title
        title_surface = constants.FONTS['header'].render("WORD GUESSING GAME", True, COLORS['text_white'])
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 40))
        screen.blit(title_surface, title_rect)

        # Draw info bar (attempts remaining)
        info_text = f"Attempts: {game_manager.attempts_remaining}/{game_manager.attempts_total}  |  Length: {game_manager.word_length}"
        info_surface = constants.FONTS['small'].render(info_text, True, COLORS['text_white'])
        info_rect = info_surface.get_rect(center=(SCREEN_WIDTH // 2, 80))
        screen.blit(info_surface, info_rect)

        # Build animation state for the grid
        anim_state = {}
        if self.flip_animation:
            anim_state['flip'] = self.flip_animation
            anim_state['flip_row'] = self.flip_row
        if self.shake_animation:
            anim_state['shake'] = self.shake_animation
            anim_state['shake_row'] = self.shake_row
        if self.pop_animation:
            anim_state['pop'] = self.pop_animation
            anim_state['pop_row'] = self.pop_row
            anim_state['pop_col'] = self.pop_col

        # Render grid if initialized
        if self.grid:
            self.grid.render(screen, game_manager.guesses, game_manager.current_input, anim_state)

        # Render current input display (below grid)
        input_y = GRID_TOP_MARGIN + game_manager.attempts_total * (self.grid.tile_size + TILE_SPACING) + 10
        input_text = f"Current: {game_manager.current_input}{'_' * (game_manager.word_length - len(game_manager.current_input))}"
        input_surface = constants.FONTS['normal'].render(input_text, True, COLORS['text_white'])
        input_rect = input_surface.get_rect(center=(SCREEN_WIDTH // 2, input_y))
        screen.blit(input_surface, input_rect)

        # Render error message if present
        if self.error_message:
            error_surface = constants.FONTS['small'].render(self.error_message, True, COLORS['error'])
            error_rect = error_surface.get_rect(center=(SCREEN_WIDTH // 2, input_y + 30))
            screen.blit(error_surface, error_rect)

        # Render virtual keyboard with key press animation
        self.virtual_keyboard.render(screen, key_press_anim=self.key_press_animation)

        # Draw instructions at bottom
        instructions = "Type or click letters | ENTER/SUBMIT to guess | ESC to restart"
        instructions_surface = constants.FONTS['small'].render(instructions, True, COLORS['text_white'])
        instructions_rect = instructions_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20))
        screen.blit(instructions_surface, instructions_rect)
