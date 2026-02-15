import os

_words_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "words.txt")
with open(_words_path) as f:
    english_words = set(word.strip().lower() for word in f)
