class UserInputIntReader:
    def __init__(self, message: str, error_message: str):
        self.message = message
        self.error_message = error_message

    def is_number_valid(self, input_number: int) -> bool:
        return True

    def read(self) -> int:
        while True:
            try:
                input_number = int(input(self.message))
                if self.is_number_valid(input_number):
                    return input_number
                else:
                    print(self.error_message)
                    continue
            except ValueError as _:
                print("The number is invalid")


class AttemptsReader(UserInputIntReader):
    def is_number_valid(self, input_number: int) -> bool:
        return input_number > 0 and input_number <= 10


class LengthReader(UserInputIntReader):
    def is_number_valid(self, input_number: int) -> bool:
        return input_number > 2 and input_number <= 11
