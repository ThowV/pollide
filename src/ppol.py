import os
from typing import List

import discord
import requests


class PPoll:
    id: int
    title: str
    description: str
    options: List[str]
    max_responses: List[int]
    anonymous: bool
    roles: List[str]
    dest_channel: str
    closing_time: str
    closing_date: str

    curr_y_responses: int
    curr_n_responses: int
    curr_m_responses: int

    logo_url: str

    def __init__(self):
        self.curr_y_responses = 0
        self.curr_n_responses = 0
        self.curr_m_responses = 0

    def clean(self):
        self.title = ' '.join(self.title)
        self.description = ' '.join(self.description) if self.description else None

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
        game = {}
        url = ''

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
            title=f"Poll #{self.id}: {self.title}",
            description=self.description,
            #url=f"https://www.google.com/search?q={'+'.join(self.title.split())}",
            color=discord.Color.blue()
        )

        embed.set_thumbnail(url=self.get_logo_url())

        return embed

    def get_responses(self):
        return f'{self.curr_y_responses} - {self.curr_m_responses} - {self.curr_n_responses}'

    def set_id(self, pid):
        self.id = pid
