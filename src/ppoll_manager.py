from ppoll import Poll

active_polls = {}


def create_poll(name: str, optional_args: []) -> str:
    max_responses = optional_args['-m']
    destination_channel = optional_args['-c']
    closing_time = optional_args['-ct']
    closing_date = optional_args['-cd']

    # Create a new poll and store it
    poll = Poll(name, max_responses, destination_channel, closing_time, closing_date)
    active_polls[id(poll)] = poll

    print(active_polls)

    return (
        f"@everyone, A poll named {name} has been opened for a maximum of {max_responses} people.\n"
        f"To respond type p:respond ID VALUE"
    )
