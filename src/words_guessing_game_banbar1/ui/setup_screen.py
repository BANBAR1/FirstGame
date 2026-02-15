"""
Setup Screen for Word Guessing Game
Allows player to select number of attempts and word length
"""

import pygame
from . import constants
from .constants import COLORS, SCREEN_WIDTH, BUTTON_WIDTH
from .ui_components import Button, NumberSelector


class SetupScreen:
    """Setup screen for configuring game parameters"""

    def __init__(self):
        """Initialize setup screen with default values"""
        self.selected_attempts = 6  # Default attempts
        self.selected_length = 5    # Default word length

        # Create number selectors
        self.attempts_selector = NumberSelector(
            min_val=1,
            max_val=10,
            default_val=self.selected_attempts,
            position=(SCREEN_WIDTH // 2, 200),
            label="Number of Attempts (1-10)"
        )

        self.length_selector = NumberSelector(
            min_val=3,
            max_val=11,
            default_val=self.selected_length,
            position=(SCREEN_WIDTH // 2, 350),
            label="Word Length (3-11)"
        )

        # Create start button
        start_btn_x = SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2
        start_btn_y = 500
        self.start_button = Button("START GAME", (start_btn_x, start_btn_y))

    def handle_event(self, event, game_manager):
        """
        Handle events for the setup screen

        Args:
            event: Pygame event
            game_manager: GameManager instance
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            # Check number selectors
            self.attempts_selector.handle_click(mouse_pos, mouse_pressed)
            self.length_selector.handle_click(mouse_pos, mouse_pressed)

            # Check start button
            if self.start_button.is_clicked(mouse_pos, mouse_pressed):
                # Update game manager with selected values
                self.selected_attempts = self.attempts_selector.selected
                self.selected_length = self.length_selector.selected

                # Start the game
                game_manager.start_game(self.selected_attempts, self.selected_length)

    def update(self, game_manager):
        """
        Update setup screen state

        Args:
            game_manager: GameManager instance
        """
        mouse_pos = pygame.mouse.get_pos()
        self.start_button.update(mouse_pos)

    def render(self, screen, game_manager):
        """
        Render the setup screen

        Args:
            screen: Pygame screen surface
            game_manager: GameManager instance
        """
        # Clear screen
        screen.fill(COLORS['background'])

        # Draw title
        title_surface = constants.FONTS['title'].render("WELCOME TO WORDLE!", True, COLORS['text_white'])
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 80))
        screen.blit(title_surface, title_rect)

        # Draw subtitle
        subtitle_surface = constants.FONTS['small'].render("Configure your game settings", True, COLORS['text_white'])
        subtitle_rect = subtitle_surface.get_rect(center=(SCREEN_WIDTH // 2, 120))
        screen.blit(subtitle_surface, subtitle_rect)

        # Render number selectors
        self.attempts_selector.render(screen)
        self.length_selector.render(screen)

        # Render start button
        self.start_button.render(screen)

        # Draw instructions at bottom
        instructions = [
            "Select the number of attempts and word length,",
            "then click START GAME to begin!"
        ]
        y_offset = 650
        for instruction in instructions:
            text_surface = constants.FONTS['small'].render(instruction, True, COLORS['text_white'])
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
            screen.blit(text_surface, text_rect)
            y_offset += 25
