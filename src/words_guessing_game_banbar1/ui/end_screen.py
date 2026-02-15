"""
End Screen for Word Guessing Game
Displays win or loss message with replay option
"""

import pygame
from . import constants
from .constants import COLORS, SCREEN_WIDTH, BUTTON_WIDTH
from .ui_components import Button, Grid
from .animations import WinBounceAnimation


class EndScreen:
    """End screen showing win/loss result"""

    def __init__(self):
        """Initialize end screen"""
        # Create buttons
        play_again_x = SCREEN_WIDTH // 2 - BUTTON_WIDTH - 10
        exit_x = SCREEN_WIDTH // 2 + 10
        button_y = 550

        self.play_again_button = Button("PLAY AGAIN", (play_again_x, button_y))
        self.exit_button = Button("EXIT", (exit_x, button_y))

        self.grid = None
        self.bounce_animation = None
        self.bounce_row = -1
        self.bounce_started = False

    def initialize_grid(self, max_attempts, word_length):
        """
        Initialize grid to display final game state

        Args:
            max_attempts: Maximum number of attempts
            word_length: Length of the word
        """
        self.grid = Grid(max_attempts, word_length)
        self.bounce_started = False
        self.bounce_animation = None

    def start_win_bounce(self, game_manager):
        """Start the win bounce animation on the winning row."""
        if not self.bounce_started:
            self.bounce_started = True
            self.bounce_row = len(game_manager.guesses) - 1
            self.bounce_animation = WinBounceAnimation(game_manager.word_length)

    def handle_event(self, event, game_manager):
        """
        Handle events for the end screen

        Args:
            event: Pygame event
            game_manager: GameManager instance
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            # Check play again button
            if self.play_again_button.is_clicked(mouse_pos, mouse_pressed):
                game_manager.reset_game()

            # Check exit button
            if self.exit_button.is_clicked(mouse_pos, mouse_pressed):
                pygame.quit()
                exit()

    def update(self, game_manager):
        """
        Update end screen state

        Args:
            game_manager: GameManager instance
        """
        mouse_pos = pygame.mouse.get_pos()
        self.play_again_button.update(mouse_pos)
        self.exit_button.update(mouse_pos)

        # Clean up finished bounce animation
        if self.bounce_animation and self.bounce_animation.is_complete:
            self.bounce_animation = None

    def render(self, screen, game_manager):
        """
        Render the end screen

        Args:
            screen: Pygame screen surface
            game_manager: GameManager instance
        """
        # Clear screen
        screen.fill(COLORS['background'])

        # Determine if win or loss
        is_win = game_manager.check_win_condition()

        # Start win bounce on first render if player won
        if is_win:
            self.start_win_bounce(game_manager)

        # Draw result message
        if is_win:
            message = "YOU WON!"
            message_color = COLORS['tile_correct']
        else:
            message = "GAME OVER"
            message_color = COLORS['error']

        message_surface = constants.FONTS['title'].render(message, True, message_color)
        message_rect = message_surface.get_rect(center=(SCREEN_WIDTH // 2, 80))
        screen.blit(message_surface, message_rect)

        # Draw attempts info
        if is_win:
            info_text = f"You guessed the word in {game_manager.attempts_total - game_manager.attempts_remaining} attempt(s)!"
        else:
            info_text = "Better luck next time!"

        info_surface = constants.FONTS['normal'].render(info_text, True, COLORS['text_white'])
        info_rect = info_surface.get_rect(center=(SCREEN_WIDTH // 2, 130))
        screen.blit(info_surface, info_rect)

        # Draw the answer
        answer_text = f"The word was: {game_manager.guess_word.upper()}"
        answer_surface = constants.FONTS['normal'].render(answer_text, True, COLORS['text_white'])
        answer_rect = answer_surface.get_rect(center=(SCREEN_WIDTH // 2, 170))
        screen.blit(answer_surface, answer_rect)

        # Build animation state for the grid
        anim_state = {}
        if self.bounce_animation:
            anim_state['bounce'] = self.bounce_animation
            anim_state['bounce_row'] = self.bounce_row

        # Render final grid state
        if self.grid:
            original_start_y = self.grid.start_y
            self.grid.start_y = 220
            self.grid.render(screen, game_manager.guesses, "", anim_state)
            self.grid.start_y = original_start_y

        # Render buttons
        self.play_again_button.render(screen)
        self.exit_button.render(screen)

        # Draw additional info
        footer_text = "Click PLAY AGAIN to start a new game or EXIT to quit"
        footer_surface = constants.FONTS['small'].render(footer_text, True, COLORS['text_white'])
        footer_rect = footer_surface.get_rect(center=(SCREEN_WIDTH // 2, 630))
        screen.blit(footer_surface, footer_rect)
