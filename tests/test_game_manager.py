"""
Tests for GameManager class
Run with: pytest tests/ -v
"""

import pytest
import sys
import os

# Add src directory to path for package imports (words_guessing_game_banbar1.*)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))
# Add inner package directory for bare imports (main_game_func, etc.)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src", "words_guessing_game_banbar1"))

# Initialize pygame before importing game modules
import pygame
pygame.init()

from main_game_func import GameManager, GameState


class TestGameManager:
    """Tests for GameManager class"""

    def setup_method(self):
        """Set up test fixtures"""
        self.manager = GameManager()

    def test_initial_state(self):
        """GameManager should start in SETUP state"""
        assert self.manager.state == GameState.SETUP
        assert self.manager.attempts_total == 0
        assert self.manager.word_length == 0
        assert self.manager.guesses == []
        assert self.manager.current_input == ""

    def test_start_game(self):
        """start_game should initialize game properly"""
        self.manager.start_game(attempts=6, length=5)

        assert self.manager.state == GameState.PLAYING
        assert self.manager.attempts_total == 6
        assert self.manager.attempts_remaining == 6
        assert self.manager.word_length == 5
        assert len(self.manager.guess_word) == 5
        assert self.manager.guesses == []
        assert self.manager.current_input == ""

    def test_start_game_different_settings(self):
        """start_game should work with various settings"""
        for attempts in [1, 5, 10]:
            for length in [3, 7, 11]:
                self.manager.start_game(attempts=attempts, length=length)
                assert self.manager.attempts_total == attempts
                assert self.manager.word_length == length
                assert len(self.manager.guess_word) == length

    def test_reset_game(self):
        """reset_game should return to SETUP state"""
        self.manager.start_game(attempts=6, length=5)
        self.manager.current_input = "test"
        self.manager.guesses.append({'word': 'test', 'match_indexes': [], 'right_indexes': []})

        self.manager.reset_game()

        assert self.manager.state == GameState.SETUP
        assert self.manager.attempts_total == 0
        assert self.manager.word_length == 0
        assert self.manager.guess_word == ""
        assert self.manager.guesses == []
        assert self.manager.current_input == ""

    def test_submit_guess_wrong_length(self):
        """submit_guess should reject wrong length words"""
        self.manager.start_game(attempts=6, length=5)

        success, error = self.manager.submit_guess("cat")  # 3 letters, need 5

        assert success == False
        assert "5 characters" in error

    def test_submit_guess_non_letters(self):
        """submit_guess should reject words with non-letters"""
        self.manager.start_game(attempts=6, length=5)

        success, error = self.manager.submit_guess("hel1o")

        assert success == False
        assert "English letters" in error

    def test_submit_guess_not_in_dictionary(self):
        """submit_guess should reject words not in dictionary"""
        self.manager.start_game(attempts=6, length=5)

        success, error = self.manager.submit_guess("xxxxx")

        assert success == False
        assert "dictionary" in error

    def test_submit_guess_valid(self):
        """submit_guess should accept valid words"""
        self.manager.start_game(attempts=6, length=5)

        success, error = self.manager.submit_guess("hello")

        assert success == True
        assert error == ""
        assert len(self.manager.guesses) == 1
        assert self.manager.attempts_remaining == 5

    def test_submit_guess_decrements_attempts(self):
        """Each guess should decrement attempts"""
        self.manager.start_game(attempts=6, length=5)

        self.manager.submit_guess("hello")
        assert self.manager.attempts_remaining == 5

        self.manager.submit_guess("world")
        assert self.manager.attempts_remaining == 4

    def test_win_condition(self):
        """Correct guess should trigger WIN state"""
        self.manager.start_game(attempts=6, length=5)
        correct_word = self.manager.guess_word

        self.manager.submit_guess(correct_word)

        assert self.manager.state == GameState.WIN

    def test_lose_condition(self):
        """Running out of attempts should trigger LOSE state"""
        self.manager.start_game(attempts=1, length=5)

        # Make sure we don't accidentally guess correctly
        self.manager.guess_word = "zzzzz"  # Unlikely to be guessed

        self.manager.submit_guess("hello")

        assert self.manager.state == GameState.LOSE

    def test_check_win_condition_true(self):
        """check_win_condition should return True after winning"""
        self.manager.start_game(attempts=6, length=5)
        correct_word = self.manager.guess_word
        self.manager.submit_guess(correct_word)

        assert self.manager.check_win_condition() == True

    def test_check_win_condition_false(self):
        """check_win_condition should return False when not won"""
        self.manager.start_game(attempts=6, length=5)
        self.manager.guess_word = "zzzzz"  # Set to something we won't guess
        self.manager.submit_guess("hello")

        assert self.manager.check_win_condition() == False

    def test_guess_stores_match_data(self):
        """Submitted guess should store match and right indexes"""
        self.manager.start_game(attempts=6, length=5)
        self.manager.guess_word = "hello"

        self.manager.submit_guess("world")

        guess_data = self.manager.guesses[0]
        assert 'word' in guess_data
        assert 'match_indexes' in guess_data
        assert 'right_indexes' in guess_data
        assert guess_data['word'] == "WORLD"


class TestGameStateTransitions:
    """Tests for game state transitions"""

    def setup_method(self):
        """Set up test fixtures"""
        self.manager = GameManager()

    def test_setup_to_playing(self):
        """SETUP -> PLAYING when game starts"""
        assert self.manager.state == GameState.SETUP
        self.manager.start_game(6, 5)
        assert self.manager.state == GameState.PLAYING

    def test_playing_to_win(self):
        """PLAYING -> WIN when correct guess"""
        self.manager.start_game(6, 5)
        self.manager.submit_guess(self.manager.guess_word)
        assert self.manager.state == GameState.WIN

    def test_playing_to_lose(self):
        """PLAYING -> LOSE when out of attempts"""
        self.manager.start_game(1, 5)
        self.manager.guess_word = "zzzzz"
        self.manager.submit_guess("hello")
        assert self.manager.state == GameState.LOSE

    def test_win_to_setup(self):
        """WIN -> SETUP when reset"""
        self.manager.start_game(6, 5)
        self.manager.submit_guess(self.manager.guess_word)
        assert self.manager.state == GameState.WIN
        self.manager.reset_game()
        assert self.manager.state == GameState.SETUP

    def test_lose_to_setup(self):
        """LOSE -> SETUP when reset"""
        self.manager.start_game(1, 5)
        self.manager.guess_word = "zzzzz"
        self.manager.submit_guess("hello")
        assert self.manager.state == GameState.LOSE
        self.manager.reset_game()
        assert self.manager.state == GameState.SETUP


class TestMixedCaseGameManager:
    """Tests for mixed case input in GameManager"""

    def setup_method(self):
        """Set up test fixtures"""
        self.manager = GameManager()

    def test_submit_mixed_case_valid(self):
        """Mixed case input should be accepted as valid"""
        self.manager.start_game(attempts=6, length=5)

        success, error = self.manager.submit_guess("HeLLo")

        assert success == True
        assert error == ""

    def test_win_with_mixed_case(self):
        """Should win with mixed case matching guess word"""
        self.manager.start_game(attempts=6, length=5)
        self.manager.guess_word = "hello"

        self.manager.submit_guess("HELLO")  # All uppercase

        assert self.manager.state == GameState.WIN

    def test_win_with_random_mixed_case(self):
        """Should win with random mixed case"""
        self.manager.start_game(attempts=6, length=5)
        self.manager.guess_word = "world"

        self.manager.submit_guess("WoRlD")  # Random mixed case

        assert self.manager.state == GameState.WIN

    def test_mixed_case_stored_uppercase(self):
        """Guess should be stored as uppercase"""
        self.manager.start_game(attempts=6, length=5)
        self.manager.guess_word = "zzzzz"  # Won't match

        self.manager.submit_guess("hElLo")

        assert self.manager.guesses[0]['word'] == "HELLO"

    def test_mixed_case_match_indexes(self):
        """Match indexes should be correct with mixed case"""
        self.manager.start_game(attempts=6, length=5)
        self.manager.guess_word = "hello"

        self.manager.submit_guess("HeLLo")

        # All letters should match
        assert self.manager.guesses[0]['match_indexes'] == [0, 1, 2, 3, 4]

    def test_mixed_case_partial_match(self):
        """Partial match should work with mixed case"""
        self.manager.start_game(attempts=6, length=5)
        self.manager.guess_word = "hello"

        self.manager.submit_guess("HeArT")

        guess_data = self.manager.guesses[0]
        # 'H' and 'e' should be in match_indexes (positions 0, 1)
        assert 0 in guess_data['match_indexes']  # H
        assert 1 in guess_data['match_indexes']  # e

    def test_mixed_case_dictionary_check(self):
        """Dictionary check should be case insensitive"""
        self.manager.start_game(attempts=6, length=5)

        # "HELLO" should be found in dictionary (stored as lowercase)
        success1, _ = self.manager.submit_guess("HELLO")
        self.manager.start_game(attempts=6, length=5)
        success2, _ = self.manager.submit_guess("hello")
        self.manager.start_game(attempts=6, length=5)
        success3, _ = self.manager.submit_guess("HeLLo")

        assert success1 == True
        assert success2 == True
        assert success3 == True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
