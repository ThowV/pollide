import shlex


def parse_optional_args(optional_args: [], optional_dict: dict) -> dict:
    for i in range(0, len(optional_args), 2):
        # Check if the argument is an identifier by checking if it starts with the '-' prefix
        if optional_args[i].startswith('-'):
            # Check if the identifier is present in the optional dictionary
            if optional_args[i] in optional_dict.keys():
                optional_dict[optional_args[i]] = optional_args[i + 1]
            else:
                pass  # ERROR: Identifier does not exist for this command
        else:
            pass  # ERROR: Not an identifier

    return optional_dict


def parse(msg: str) -> []:
    args = shlex.split(msg)
    args_parsed = []

    i = 0
    while i < len(args):
        # Check if the argument is an identifier by checking if it starts with the '-' prefix
        if args[i].startswith('-'):
            arg = args[i].split('-')

            # Add a parsed argument: Identifier = Value
            args_parsed.append([arg[1], args[i + 1]])

            # Next item is the value so we skip it
            i += 1
        else:
            args_parsed.append(args[i])

        i += 1

    return args_parsed
