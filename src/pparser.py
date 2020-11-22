from pexceptions import InvalidArgumentException, ValueArgumentMissingException


def check_formatting(command: str, input: list, options: dict):
    past_arg_identifier = ''

    for word in input:
        # Check if the argument is an option identifier
        if word.startswith('-'):
            if past_arg_identifier:
                raise ValueArgumentMissingException(command, past_arg_identifier)
            elif word not in options.keys():
                raise InvalidArgumentException(command, word)
            else:
                past_arg_identifier = word  # Next loop iteration should encounter a value
        else:
            past_arg_identifier = ''


def parse(input: list, options: dict) -> dict:
    mandatory_pointer = 0
    args_keys = list(options.keys())

    # Assign all arguments to the correct keys in the args dictionary
    i = 0
    while i < len(input):
        arg: str = input[i]

        # Check if the argument is an identifier
        if arg.startswith('-'):
            options[arg] = input[i + 1]
            i += 1
        else:
            options[args_keys[mandatory_pointer]] = input[i]

        i += 1

    return options
