"""
Pytest configuration and fixtures for Word Guessing Game tests
"""

import pytest
import sys
import os

# Add src directory to path for package imports (words_guessing_game_banbar1.*)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))
# Add inner package directory for bare imports (main_game_func, etc.)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src", "words_guessing_game_banbar1"))


@pytest.fixture(scope="session", autouse=True)
def setup_pygame():
    """Initialize pygame once for all tests"""
    import pygame
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def sample_words():
    """Provide sample words for testing"""
    return {
        'five_letter': ['hello', 'world', 'apple', 'house', 'water'],
        'three_letter': ['cat', 'dog', 'run', 'sun', 'hat'],
        'invalid': ['123', 'ab cd', 'hello!', ''],
    }
