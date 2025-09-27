import nltk
nltk.download('words')
from nltk.corpus import words
english_words = set(word.lower() for word in words.words())