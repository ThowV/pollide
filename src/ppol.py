import os
from typing import List

import discord
import requests


class PPoll:
    title: str
    description: str
    options: dict[str: int]
    responses: dict[int: int]  # User id: Option id
    max_responses: List[int]
    anonymous: bool
    roles: List[str]
    dest_channel: str
    closing_time: str
    closing_date: str

    emojis: List[str]

    curr_y_responses: int
    curr_n_responses: int
    curr_m_responses: int

    logo_url: str

    def __init__(self):
        self.responses = {}
        self.curr_y_responses = 0
        self.curr_n_responses = 0
        self.curr_m_responses = 0

    def clean(self):
        self.title = ' '.join(self.title)
        self.description = ' '.join(self.description) if self.description else None

        if not self.options:
            self.emojis = ['\U00002705', '\U00002796', '\U0001F1FD']
            self.options = {'Yes': 0, 'Maybe': 0, 'No': 0}
        else:
            self.options = {option: 0 for option in self.options}

    def add_response(self, user_id, emoji_idx):
        # Add response
        self.responses[user_id] = emoji_idx

        # Add response to response amount of option
        option = list(self.options.keys())[emoji_idx]
        response_amount = self.options.get(option)
        self.options[option] = response_amount + 1

    def respond(self, option_id: int):
        if option_id == 1:
            self.curr_y_responses += 1
        elif option_id == 2:
            self.curr_m_responses += 1
        elif option_id == 3:
            self.curr_n_responses += 1

        return f"Poll {id(self)} standings: {self.curr_y_responses} - {self.curr_n_responses} - {self.curr_m_responses}"

    def get_logo_url(self) -> str:
        game_search_result = requests.get(
            f"https://www.steamgriddb.com/api/v2/search/autocomplete/{self.title.lower().strip().capitalize()}",
            headers={'Authorization': f"Bearer {os.getenv('STEAMGRIDDB_API_KEY')}"})

        # Get game
        if not game_search_result.status_code == 200:
            return ''

        json = game_search_result.json()

        if not json['data']:
            return ''

        game = json['data'][0]

        # Get logo
        if not game:
            return ''

        logos_search_result = requests.get(f"https://www.steamgriddb.com/api/v2/logos/game/{game['id']}",
                                           headers={'Authorization': f"Bearer {os.getenv('STEAMGRIDDB_API_KEY')}"})

        if not logos_search_result.status_code == 200:
            return ''

        json = logos_search_result.json()

        if not json['data']:
            return ''

        return json['data'][0]['url']

    def get_as_embed(self):
        embed = discord.Embed(
            title=f"Poll: {self.title}",
            description=self.description,
            #url=f"https://www.google.com/search?q={'+'.join(self.title.split())}",
            color=discord.Color.blue()
        )

        # Generate options info
        options_info = ''
        for idx in range(len(self.options)):
            option = list(self.options.keys())[idx]
            response_amount = self.options.get(option)
            options_info += f'{self.emojis[idx]} {option} - {response_amount}\n'

        embed.add_field(name='Votes', value=options_info)

        embed.set_thumbnail(url=self.get_logo_url())

        return embed

    def get_emojis(self) -> List[str]:
        return self.emojis

    def get_responses(self):
        return f'{self.curr_y_responses} - {self.curr_m_responses} - {self.curr_n_responses}'
