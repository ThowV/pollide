class Poll:
    name: str
    description: str
    options: [str]
    max_responses: int
    destination_channel: str
    closing_time: str
    closing_date: str

    curr_y_responses: int
    curr_n_responses: int
    curr_m_responses: int

    def __init__(self, name: str, description: str, options: list, max_responses: int, destination_channel: str,
                 closing_time: str, closing_date: str):
        self.name = name
        self.description = description
        self.options = options
        self.max_responses = max_responses
        self.destination_channel = destination_channel
        self.closing_time = closing_time
        self.closing_date = closing_date

        self.curr_y_responses = 0
        self.curr_n_responses = 0
        self.curr_m_responses = 0

    def respond(self, response: str):
        response = response.lower()

        if response == 'y':
            self.curr_y_responses += 1
        elif response == 'n':
            self.curr_n_responses += 1
        elif response == 'm':
            self.curr_m_responses += 1

        return f"Poll {id(self)} standings: {self.curr_y_responses} - {self.curr_n_responses} - {self.curr_m_responses}"
