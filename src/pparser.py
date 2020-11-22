from typing import List

from pexceptions import InvalidArgumentException, OptionValueMissingException, MandatoryValueMissingException, \
    MandatoryValueUnnecessaryException


def parse(command: str, input: List[str], options: dict) -> dict:
    options_keys = list(options.keys())

    i = 0
    while i < len(input):
        word = input[i]

        # Validate formatting
        step_size = validate_formatting(command, input, options, i, word, options_keys)

        # Validate typing
        # ...

        # Build options
        if step_size == 2:
            options[word] = input[i + 1]
        else:
            options[options_keys[i]] = input[i]

        i += step_size

    return options


def validate_formatting(command: str, input: List[str], options: dict, index: int, word: str, options_keys: list) -> int:
    step_size = 1

    # Check if the word is an option identifier
    if word.startswith('-'):
        # Check if we actually passed all mandatory arguments
        if options[options_keys[index]][1]:
            raise MandatoryValueMissingException(command)
        else:
            step_size = 2

        # Check if current word is a valid option
        if word not in options_keys:
            raise InvalidArgumentException(command, word)

        # Check if there is a next word
        if index + 1 >= len(input):
            # Next word should be a value
            raise OptionValueMissingException(command, word)

        # Check if the next word is also an option identifier
        word_next = input[index + 1]
        if word_next.startswith('-'):
            # Next word should not be an option identifier but a value
            raise OptionValueMissingException(command, word)
    # The word is not an option identifier
    else:
        # Check if we are still assigning mandatory arguments
        if not options[options_keys[index]][1]:
            raise MandatoryValueUnnecessaryException(command)

    return step_size


def validate_typing():
    pass
