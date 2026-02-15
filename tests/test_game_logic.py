"""
Tests for Word Guessing Game logic functions
Run with: pytest tests/ -v
"""

import pytest
import sys
import os

# Add src directory to path for package imports (words_guessing_game_banbar1.*)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))
# Add inner package directory for bare imports (functions.find, etc.)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src", "words_guessing_game_banbar1"))

from functions.find import find_random_word, find_match_indexes, find_right_indexes
from functions.validation import all_english_letters, is_word_lenght_valid, are_symbols_same


class TestFindRandomWord:
    """Tests for find_random_word function"""

    def test_returns_word_of_correct_length(self):
        """Word should match requested length"""
        for length in [3, 5, 7, 10]:
            word = find_random_word(length)
            assert len(word) == length, f"Expected length {length}, got {len(word)}"

    def test_returns_lowercase_word(self):
        """Word should be lowercase"""
        word = find_random_word(5)
        assert word == word.lower(), "Word should be lowercase"

    def test_returns_string(self):
        """Should return a string"""
        word = find_random_word(5)
        assert isinstance(word, str), "Should return a string"

    def test_different_lengths(self):
        """Should work for various lengths"""
        for length in range(3, 12):
            word = find_random_word(length)
            assert len(word) == length


class TestFindMatchIndexes:
    """Tests for find_match_indexes function (correct position matches)"""

    def test_all_letters_match(self):
        """All letters in correct position"""
        result = find_match_indexes("hello", "hello")
        assert result == [0, 1, 2, 3, 4]

    def test_no_letters_match(self):
        """No letters in correct position"""
        result = find_match_indexes("abcde", "fghij")
        assert result == []

    def test_some_letters_match(self):
        """Some letters in correct position"""
        result = find_match_indexes("hello", "helps")
        assert result == [0, 1, 2]

    def test_case_insensitive(self):
        """Should be case insensitive"""
        result = find_match_indexes("HELLO", "hello")
        assert result == [0, 1, 2, 3, 4]

    def test_first_letter_match(self):
        """Only first letter matches"""
        result = find_match_indexes("apple", "arrow")
        assert 0 in result

    def test_last_letter_match(self):
        """Only last letter matches"""
        result = find_match_indexes("tests", "words")
        assert 4 in result


class TestFindRightIndexes:
    """Tests for find_right_indexes function (wrong position matches)"""

    def test_no_right_letters(self):
        """No letters in wrong position"""
        result = find_right_indexes("hello", "hello", [0, 1, 2, 3, 4])
        assert result == []

    def test_all_wrong_position(self):
        """All letters exist but in wrong positions"""
        # "olleh" vs "hello" - all letters exist but wrong positions
        match_indexes = find_match_indexes("olleh", "hello")
        result = find_right_indexes("olleh", "hello", match_indexes)
        # Should find o, l, l, e in wrong positions
        assert len(result) > 0

    def test_some_wrong_position(self):
        """Some letters in wrong position"""
        # "heart" vs "earth" - e,a,r,t are in wrong positions, h might match
        match_indexes = find_match_indexes("heart", "earth")
        result = find_right_indexes("heart", "earth", match_indexes)
        assert len(result) > 0

    def test_letter_not_in_word(self):
        """Letters not in word should not be marked"""
        match_indexes = find_match_indexes("xxxxx", "hello")
        result = find_right_indexes("xxxxx", "hello", match_indexes)
        assert result == []

    def test_duplicate_letters_handling(self):
        """Should handle duplicate letters correctly"""
        # "speed" has two e's, "eeeee" guess
        match_indexes = find_match_indexes("eeeee", "speed")
        result = find_right_indexes("eeeee", "speed", match_indexes)
        # Should not mark more e's than exist in "speed"
        total_marked = len(match_indexes) + len(result)
        assert total_marked <= 2  # "speed" only has 2 e's


class TestAllEnglishLetters:
    """Tests for all_english_letters function"""

    def test_valid_lowercase(self):
        """Lowercase letters should be valid"""
        assert all_english_letters("hello") == True

    def test_valid_uppercase(self):
        """Uppercase letters should be valid"""
        assert all_english_letters("HELLO") == True

    def test_valid_mixed_case(self):
        """Mixed case letters should be valid"""
        assert all_english_letters("HeLLo") == True

    def test_invalid_with_numbers(self):
        """Numbers should be invalid"""
        assert all_english_letters("hello123") == False

    def test_invalid_with_spaces(self):
        """Spaces should be invalid"""
        assert all_english_letters("hello world") == False

    def test_invalid_with_special_chars(self):
        """Special characters should be invalid"""
        assert all_english_letters("hello!") == False

    def test_empty_string(self):
        """Empty string should be invalid"""
        assert all_english_letters("") == False


class TestIsWordLengthValid:
    """Tests for is_word_lenght_valid function"""

    def test_correct_length(self):
        """Word with correct length should be valid"""
        assert is_word_lenght_valid("hello", 5) == True

    def test_too_short(self):
        """Word too short should be invalid"""
        assert is_word_lenght_valid("hi", 5) == False

    def test_too_long(self):
        """Word too long should be invalid"""
        assert is_word_lenght_valid("hello", 3) == False

    def test_various_lengths(self):
        """Test various word lengths"""
        assert is_word_lenght_valid("cat", 3) == True
        assert is_word_lenght_valid("elephant", 8) == True
        assert is_word_lenght_valid("a", 1) == True


class TestAreSymbolsSame:
    """Tests for are_symbols_same function"""

    def test_same_lowercase(self):
        """Same lowercase letters should match"""
        assert are_symbols_same("a", "a") == True

    def test_same_uppercase(self):
        """Same uppercase letters should match"""
        assert are_symbols_same("A", "A") == True

    def test_case_insensitive(self):
        """Should be case insensitive"""
        assert are_symbols_same("a", "A") == True
        assert are_symbols_same("A", "a") == True

    def test_different_letters(self):
        """Different letters should not match"""
        assert are_symbols_same("a", "b") == False


class TestGameScenarios:
    """Integration tests for game scenarios"""

    def test_winning_scenario(self):
        """Test a winning game scenario"""
        guess_word = "apple"
        user_word = "apple"

        match_indexes = find_match_indexes(user_word, guess_word)
        right_indexes = find_right_indexes(user_word, guess_word, match_indexes)

        assert match_indexes == [0, 1, 2, 3, 4]
        assert right_indexes == []
        assert user_word.lower() == guess_word.lower()

    def test_partial_match_scenario(self):
        """Test a partial match scenario"""
        guess_word = "apple"
        user_word = "apply"

        match_indexes = find_match_indexes(user_word, guess_word)
        right_indexes = find_right_indexes(user_word, guess_word, match_indexes)

        # a, p, p, l should match at positions 0, 1, 2, 3
        assert 0 in match_indexes  # 'a'
        assert 1 in match_indexes  # 'p'
        assert 2 in match_indexes  # 'p'
        assert 3 in match_indexes  # 'l'
        assert 4 not in match_indexes  # 'y' vs 'e'

    def test_no_match_scenario(self):
        """Test a no match scenario"""
        guess_word = "apple"
        user_word = "drink"

        match_indexes = find_match_indexes(user_word, guess_word)
        right_indexes = find_right_indexes(user_word, guess_word, match_indexes)

        assert len(match_indexes) == 0
        assert len(right_indexes) == 0

    def test_wrong_position_scenario(self):
        """Test letters in wrong positions"""
        guess_word = "alert"
        user_word = "later"

        match_indexes = find_match_indexes(user_word, guess_word)
        right_indexes = find_right_indexes(user_word, guess_word, match_indexes)

        # Some letters should be in wrong positions
        assert len(right_indexes) > 0


class TestMixedCaseInput:
    """Tests for mixed case user input handling"""

    def test_mixed_case_match_indexes(self):
        """Mixed case input should match correctly"""
        # User types "HeLLo", guess word is "hello"
        result = find_match_indexes("HeLLo", "hello")
        assert result == [0, 1, 2, 3, 4]

    def test_mixed_case_vs_uppercase_guess(self):
        """Mixed case should work against uppercase guess word"""
        result = find_match_indexes("hElLo", "HELLO")
        assert result == [0, 1, 2, 3, 4]

    def test_mixed_case_partial_match(self):
        """Mixed case partial matches should work"""
        result = find_match_indexes("HeLPs", "hello")
        # H, e, l should match at positions 0, 1, 2
        assert 0 in result  # H vs h
        assert 1 in result  # e vs e
        assert 2 in result  # l vs l

    def test_mixed_case_right_indexes(self):
        """Mixed case should work for wrong position matches"""
        match_indexes = find_match_indexes("oLLeh", "hello")
        right_indexes = find_right_indexes("oLLeh", "hello", match_indexes)
        # Should find letters in wrong positions
        assert len(right_indexes) > 0

    def test_all_english_letters_mixed_case(self):
        """Mixed case should be valid English letters"""
        assert all_english_letters("HeLLo") == True
        assert all_english_letters("wOrLd") == True
        assert all_english_letters("PyThOn") == True

    def test_symbols_same_mixed_variations(self):
        """Various mixed case comparisons should work"""
        assert are_symbols_same("H", "h") == True
        assert are_symbols_same("h", "H") == True
        assert are_symbols_same("Z", "z") == True
        assert are_symbols_same("a", "A") == True

    def test_winning_with_mixed_case(self):
        """Should be able to win with mixed case input"""
        guess_word = "apple"
        user_word = "ApPlE"  # Mixed case

        match_indexes = find_match_indexes(user_word, guess_word)

        # All 5 letters should match
        assert match_indexes == [0, 1, 2, 3, 4]
        # Win condition check (case insensitive)
        assert user_word.lower() == guess_word.lower()

    def test_mixed_case_no_match(self):
        """Mixed case with no matches should return empty"""
        result = find_match_indexes("XyZaB", "hello")
        assert result == []


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
