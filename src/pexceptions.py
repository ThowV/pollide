class InvalidArgumentException(Exception):
    def __init__(self, command: str, argument: str):
        self.message = f"'{argument}' is not a valid argument for the {command} command.\n" \
                       f"You can type 'p:help {command}' for more info on this command and its arguments."
        super().__init__()

    def __str__(self):
        return self.message


class OptionValueMissingException(Exception):
    def __init__(self, command: str, option: str):
        self.message = f"The '{option}' option expects a value but it was not provided.\n" \
                       f"You can type 'p:help {command}' for more info on this command and its arguments."
        super().__init__()

    def __str__(self):
        return self.message


class MandatoryValueMissingException(Exception):
    def __init__(self, command: str):
        self.message = f"The '{command}' command is being called with missing mandatory arguments.\n" \
                       f"You can type 'p:help {command}' for more info on this command and its arguments."
        super().__init__()

    def __str__(self):
        return self.message
