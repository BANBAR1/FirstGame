"""
Word Guessing Game with Pygame UI
A Wordle-style word guessing game with graphical interface
"""

import pygame
from enum import Enum

# Import UI components
from words_guessing_game_banbar1.ui.constants import *
from words_guessing_game_banbar1.ui.setup_screen import SetupScreen
from words_guessing_game_banbar1.ui.game_screen import GameScreen
from words_guessing_game_banbar1.ui.end_screen import EndScreen
from words_guessing_game_banbar1.ui.animations import ScreenFadeTransition

# Import game logic functions
from words_guessing_game_banbar1.functions.find import find_random_word, find_match_indexes, find_right_indexes
from words_guessing_game_banbar1.functions.validation import all_english_letters, is_word_lenght_valid
from words_guessing_game_banbar1.functions.word_loader import english_words


class GameState(Enum):
    """Enum for game states"""
    SETUP = 1
    PLAYING = 2
    WIN = 3
    LOSE = 4


class GameManager:
    """Manages game state and logic"""

    def __init__(self):
        """Initialize game manager"""
        self.state = GameState.SETUP
        self.attempts_total = 0
        self.attempts_remaining = 0
        self.word_length = 0
        self.guess_word = ""
        self.guesses = []  # List of dicts: {'word', 'match_indexes', 'right_indexes'}
        self.current_input = ""

    def start_game(self, attempts, length):
        """
        Start a new game with specified parameters

        Args:
            attempts: Number of attempts allowed
            length: Length of the word to guess
        """
        self.attempts_total = attempts
        self.attempts_remaining = attempts
        self.word_length = length
        self.guess_word = find_random_word(length)
        self.guesses = []
        self.current_input = ""
        self.state = GameState.PLAYING

    def submit_guess(self, user_word):
        """
        Process a guess submission

        Args:
            user_word: The word guessed by the user

        Returns:
            Tuple (success: bool, error_message: str)
        """
        # Validate word length
        if not is_word_lenght_valid(user_word, self.word_length):
            return False, f"Word must be {self.word_length} characters long"

        # Validate only English letters
        if not all_english_letters(user_word):
            return False, "Word must contain only English letters"

        # Validate word is in dictionary
        if user_word.lower() not in english_words:
            return False, "Word not in English dictionary"

        # Word is valid, process it
        match_indexes = find_match_indexes(user_word, self.guess_word)
        right_indexes = find_right_indexes(user_word, self.guess_word, match_indexes)

        # Store guess data
        self.guesses.append({
            'word': user_word.upper(),
            'match_indexes': match_indexes,
            'right_indexes': right_indexes
        })

        # Decrease attempts
        self.attempts_remaining -= 1

        # Check win condition
        if user_word.lower() == self.guess_word.lower():
            self.state = GameState.WIN
        # Check lose condition
        elif self.attempts_remaining <= 0:
            self.state = GameState.LOSE

        return True, ""

    def check_win_condition(self):
        """
        Check if player won

        Returns:
            bool: True if won, False otherwise
        """
        if not self.guesses:
            return False
        last_guess = self.guesses[-1]['word']
        return last_guess.lower() == self.guess_word.lower()

    def reset_game(self):
        """Reset game to setup screen"""
        self.state = GameState.SETUP
        self.attempts_total = 0
        self.attempts_remaining = 0
        self.word_length = 0
        self.guess_word = ""
        self.guesses = []
        self.current_input = ""


def main():
    """Main game loop"""
    # Initialize pygame
    pygame.init()
    init_fonts()

    # Create screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Word Guessing Game")
    clock = pygame.time.Clock()

    # Create game manager
    game_manager = GameManager()

    # Create screens
    setup_screen = SetupScreen()
    game_screen = GameScreen()
    end_screen = EndScreen()

    screens = {
        GameState.SETUP: setup_screen,
        GameState.PLAYING: game_screen,
        GameState.WIN: end_screen,
        GameState.LOSE: end_screen
    }

    # Track previous state to detect transitions
    previous_state = None
    fade_transition = None
    fade_pending_state = None  # State to apply at fade midpoint
    fade_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    fade_overlay.fill((0, 0, 0))

    # Main game loop
    running = True
    while running:
        current_state = game_manager.state
        current_screen = screens[current_state]

        # Handle state transitions
        if current_state != previous_state:
            if previous_state is not None:
                # Start fade transition (skip for the initial SETUP)
                fade_transition = ScreenFadeTransition()
                fade_pending_state = current_state
                # Revert to old state during fade-out phase
                game_manager.state = previous_state
                current_state = previous_state
                current_screen = screens[current_state]
            else:
                # First state (SETUP) — initialize without fade
                previous_state = current_state

        # Handle fade midpoint: switch screens when fully black
        if fade_transition and fade_transition.midpoint_reached:
            fade_transition.midpoint_reached = False  # Consume the flag
            game_manager.state = fade_pending_state
            current_state = fade_pending_state
            current_screen = screens[current_state]
            previous_state = current_state

            # Initialize the new screen
            if current_state == GameState.PLAYING:
                game_screen.initialize_grid(game_manager.attempts_total, game_manager.word_length)
            elif current_state in [GameState.WIN, GameState.LOSE]:
                end_screen.initialize_grid(game_manager.attempts_total, game_manager.word_length)

            fade_pending_state = None

        # Clear fade when done
        if fade_transition and not fade_transition.active:
            fade_transition = None

        # Event handling (block input during fade)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif not fade_transition:
                current_screen.handle_event(event, game_manager)

        # Update
        current_screen.update(game_manager)

        # Render
        screen.fill(COLORS['background'])
        current_screen.render(screen, game_manager)

        # Draw fade overlay on top
        if fade_transition and fade_transition.active:
            alpha = fade_transition.get_alpha()
            fade_overlay.set_alpha(alpha)
            screen.blit(fade_overlay, (0, 0))

        pygame.display.flip()

        # Cap framerate
        clock.tick(FPS)

    # Quit
    pygame.quit()

