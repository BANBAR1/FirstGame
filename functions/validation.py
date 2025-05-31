import re
from functions.nltk_functions import english_words

def all_english_letters(s):
    return bool(re.fullmatch(r'[a-zA-Z]+', s))


def is_word_lenght_valid(user_word: str, lenght: int):
    return len(user_word) == lenght


def are_symbols_same(symbol1: str, symbol2: str):
    return symbol1.lower() == symbol2.lower()


def validate_word(user_word, lenght):
    check1 = is_word_lenght_valid(user_word, lenght)
    if not check1:
        print("Your word must be", lenght, "characters long")

    check2 = all_english_letters(user_word)
    if not check2:
        print("Your word must have only English letters")
    
    check3 = user_word in english_words
    if not check3:
        print("Your word must be in the English dictionary")
    return check1 and check2 and check3


def ask_and_check_user_word(lenght: int):
    is_valid = False
    while not is_valid == True:
        user_word = input("Enter your word:")
        is_valid = validate_word(user_word, lenght)

    return user_word
