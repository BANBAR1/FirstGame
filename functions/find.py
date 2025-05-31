import random
from functions.validation import are_symbols_same
from functions.nltk_functions import english_words
 
def find_random_word(lenght):
    target_words = []
    for word in english_words:
        if len(word) == lenght:
            target_words.append(word)
    return random.choice(target_words)


def find_right_letters(user_word, guess_word, match_letters: list):
    right_letters = []
    found_letters = []
    for i in range(len(user_word)):
        if i in match_letters:
            continue

        for j in range(len(guess_word)):
            if j not in match_letters and j not in found_letters:
                if are_symbols_same(guess_word[j], user_word[i]):
                    found_letters.append(j)
                    right_letters.append(i)
                    break
    return right_letters


def find_match_letters(user_word, guess_word):
    match_letters = []
    for i in range(len(user_word)):
        if are_symbols_same(user_word[i], guess_word[i]):
            match_letters.append(i)
    return match_letters
