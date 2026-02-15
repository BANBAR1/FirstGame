def print_result(user_word, match_letters, right_letters):
    color_green = "\033[32m"
    color_orange = "\033[38;5;208m"
    reset = "\033[0m"

    colored_word = "".join(
        (color_green if i in match_letters else color_orange if i in right_letters else reset) + letter
        for i, letter in enumerate(user_word)
    )
    print(colored_word + reset)
