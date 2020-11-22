import os

import requests


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

    logo_url: str

    def __init__(self, name: str, description: str, options: list, max_responses: int, destination_channel: str,
                 closing_time: str, closing_date: str):
        self.name = name.lower().strip().capitalize()
        self.description = description
        self.options = options
        self.max_responses = max_responses
        self.destination_channel = destination_channel
        self.closing_time = closing_time
        self.closing_date = closing_date

        self.curr_y_responses = 0
        self.curr_n_responses = 0
        self.curr_m_responses = 0

        self.logo_url = self.get_logo_url()

    def respond(self, response: str):
        response = response.lower()

        if response == 'y':
            self.curr_y_responses += 1
        elif response == 'n':
            self.curr_n_responses += 1
        elif response == 'm':
            self.curr_m_responses += 1

        return f"Poll {id(self)} standings: {self.curr_y_responses} - {self.curr_n_responses} - {self.curr_m_responses}"

    def get_logo_url(self) -> str:
        game_search_result = requests.get(f"https://www.steamgriddb.com/api/v2/search/autocomplete/{self.name}",
                                          headers={'Authorization': f"Bearer {os.getenv('STEAMGRIDDB_API_KEY')}"})
        game = {}
        url = ''

        # Get game
        if game_search_result.status_code == 200:
            game = game_search_result.json()['data'][0]

        # Get logo
        if game:
            logos_search_result = requests.get(f"https://www.steamgriddb.com/api/v2/logos/game/{game['id']}",
                                               headers={'Authorization': f"Bearer {os.getenv('STEAMGRIDDB_API_KEY')}"})

            if logos_search_result.status_code == 200:
                json = logos_search_result.json()

                url = json['data'][0]['url']

        return url
