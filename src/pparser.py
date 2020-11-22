from typing import List

from pexceptions import InvalidArgumentException, OptionValueMissingException, MandatoryValueMissingException, \
    MandatoryValueUnnecessaryException


def check_formatting(command: str, input: List[str], options: dict):
    options_keys = list(options.keys())

    i = 0
    step_size = 1
    while i < len(input):
        word = input[i]

        # Check if the word is an option identifier
        if word.startswith('-'):
            # Check if we actually passed all mandatory arguments
            if options[options_keys[i]][1]:
                raise MandatoryValueMissingException(command)
            else:
                step_size = 2

            # Check if current word is a valid option
            if word not in options_keys:
                raise InvalidArgumentException(command, word)

            # Check if there is a next word
            if i + 1 >= len(input):
                # Next word should be a value
                raise OptionValueMissingException(command, word)

            # Check if the next word is also an option identifier
            word_next = input[i + 1]
            if word_next.startswith('-'):
                # Next word should not be an option identifier but a value
                raise OptionValueMissingException(command, word)
        # The word is not an option identifier
        else:
            # Check if we are still assigning mandatory arguments
            if not options[options_keys[i]][1]:
                raise MandatoryValueUnnecessaryException(command)

        i += step_size


def parse(input: List[str], options: dict) -> dict:
    mandatory_pointer = 0
    options_keys = list(options.keys())

    # Assign all arguments to the correct keys in the args dictionary
    i = 0
    while i < len(input):
        word = input[i]

        # Check if the word is an option identifier
        if word.startswith('-'):
            options[word] = input[i + 1]
            i += 1
        else:
            options[options_keys[mandatory_pointer]] = input[i]
            mandatory_pointer += 1

        i += 1

    return options
