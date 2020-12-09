from ppoll import PPoll

active_polls = {}


def store(poll: PPoll, pid: int):
    active_polls[pid] = poll


def get(pid: int) -> PPoll:
    global active_polls

    return active_polls.get(pid)
