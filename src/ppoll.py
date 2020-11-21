class Poll:
    name:                   str
    max_responses:          int
    destination_channel:    str
    closing_time:           str
    closing_date:           str

    def __init__(self, name: str, max_responses: int, destination_channel: str, closing_time: str, closing_date: str):
        self.name = name
        self.max_responses = max_responses
        self.destination_channel = destination_channel
        self.closing_time = closing_time
        self.closing_date = closing_date
