from functions.find import find_random_word, find_right_indexes, find_match_indexes
from functions.print import print_result
from functions.validation import ask_and_check_user_word
from functions.UserInputIntReader import AttemptsReader, LengthReader

attempts_reader = AttemptsReader(
    "How many attempts do you want? ", "The number must be in range from 1 to 10")
length_reader = LengthReader(
    "What length do you want for your word? ", "The length must be in range from 3 to 11")

number_of_attempts = attempts_reader.read()
length = length_reader.read()

guess_word = str(find_random_word(length))

while number_of_attempts > 0:
    user_word = ask_and_check_user_word(length)

    match_letters = find_match_indexes(user_word, guess_word)
    right_letters = find_right_indexes(user_word, guess_word, match_letters)

    print_result(user_word, match_letters, right_letters)
    
    if guess_word.lower() == user_word.lower():
        print("You won!")
        input("Press Enter to exit...")
        exit()
    number_of_attempts -= 1

print(f"You lose! The guess word is: {guess_word}")
input("Press Any key to exit...")