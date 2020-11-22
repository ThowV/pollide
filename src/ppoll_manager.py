from ppoll import Poll

active_polls = {}


def create_poll(input: dict) -> Poll:
    # Create a new poll and store it
    poll = Poll(input['-n'], input['-d'], input['-o'], input['-m'], input['-c'], input['-ct'], input['-cd'])
    active_polls[id(poll)] = poll

    return poll


def respond_to_poll(pid: int, response: str) -> str:
    return active_polls.get(pid).respond(response)
