import random
from words_guessing_game_banbar1.functions.validation import are_symbols_same
from words_guessing_game_banbar1.functions.word_loader import english_words
 
def find_random_word(lenght):
    target_words = []
    for word in english_words:
        if len(word) == lenght:
            target_words.append(word)
    return random.choice(target_words)


def find_right_indexes(user_word, guess_word, match_indexes: list):
    right_indexes = []
    found_indexes = []
    for i in range(len(user_word)):
        if i in match_indexes:
            continue

        for j in range(len(guess_word)):
            if j not in match_indexes and j not in found_indexes:
                if are_symbols_same(guess_word[j], user_word[i]):
                    found_indexes.append(j)
                    right_indexes.append(i)
                    break
    return right_indexes


def find_match_indexes(user_word, guess_word):
    match_indexes = []
    for i in range(len(user_word)):
        if are_symbols_same(user_word[i], guess_word[i]):
            match_indexes.append(i)
    return match_indexes
