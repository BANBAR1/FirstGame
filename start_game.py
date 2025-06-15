from functions.find import find_random_word, find_right_letters, find_match_letters
from functions.print import print_result
from functions.validation import ask_and_check_user_word
from functions.UserInputIntReader import AttemptsReader, LengthReader

attempts_reader = AttemptsReader(
    "How many attempts do you want? ", "The number must be in range from 1 to 10")
lenght_reader = LengthReader(
    "What lenght do you want for your word? ", "The lenght must be in range from 3 to 11")

number_of_attempts = attempts_reader.read()
lenght = lenght_reader.read()

guess_word = str(find_random_word(lenght))

while number_of_attempts > 0:
    user_word = ask_and_check_user_word(lenght)

    match_letters = find_match_letters(user_word, guess_word)
    right_letters = find_right_letters(user_word, guess_word, match_letters)

    print_result(user_word, match_letters, right_letters)

    if guess_word.lower() == user_word.lower():
        print("You won!")
        input("Press Enter to exit...")
        exit()
    number_of_attempts -= 1

print(f"You lose! The guess word is: {guess_word}")
input("Press Enter to exit...")