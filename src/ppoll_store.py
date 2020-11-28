from ppol import PPoll

active_polls = {}
pid_pointer = 1


def store(poll: PPoll):
    global pid_pointer

    poll.clean()
    poll.set_id(pid_pointer)
    active_polls[poll.id] = poll
    pid_pointer += 1


def get(pid: int) -> PPoll:
    global active_polls

    return active_polls.get(pid)
