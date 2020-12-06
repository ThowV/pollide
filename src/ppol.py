import os
from typing import List, Union

import discord
import requests


class PPoll:
    # Poll data
    logo_url: str
    title: str
    description: str
    options: dict[str: [str, int]]  # Emoji code: [Option description, Response amount]
    responses: dict[int: List[str]]  # User id: Emoji code
    multi_options: bool
    anonymous: bool
    roles: List[str]
    dest_channel: str
    closing_time: str
    closing_date: str

    # Parsed destination data
    max_responses: List[int]
    option_descriptions: List[str]

    def __init__(self):
        self.responses = {}

        self.max_responses = [0]
        self.option_descriptions = []

    def clean(self):
        # Set description and title
        self.title = ' '.join(self.title)
        self.description = ' '.join(self.description) if self.description else None

        # Set option descriptions and options
        if not self.option_descriptions:
            self.options = {
                '\U00002705': ['yes',   0],
                '\U00002796': ['maybe', 0],
                '\U0001F1FD': ['no',    0]
            }
        #else:
        #    self.options = {option: [0] for option in self.options}

        # Set the logo
        self.logo_url = self.get_logo_url()

    def add_response(self, user_id: int, emoji_code: str) -> Union[str, None]:
        """Return the the emoji code that was removed"""

        emoji_code_removed = None

        # Check if multiple responses are allowed, if not, remove last response
        if not self.multi_options:
            emoji_code_removed = self.remove_response(user_id)

        # Add response
        if user_id not in self.responses:
            self.responses[user_id] = []

        self.responses[user_id].append(emoji_code)

        # Add one to response amount of option
        self.options[emoji_code][1] = self.options[emoji_code][1] + 1

        return emoji_code_removed

    def remove_response(self, user_id: int, emoji: Union[str, int] = None) -> Union[str, None]:
        """Return the the emoji code that was removed"""

        emoji_code = emoji

        # Get the emoji code and emoji index in different scenarios
        if isinstance(emoji, int):
            # Emoji index was provided, get the emoji code
            try:
                emoji_code = self.get_emojis()[emoji]
            except KeyError:
                # Wrong emoji index provided.
                return None
        elif emoji is None:
            # Nothing was provided, get the emoji code and index
            try:
                # We get the first emoji code because this block only triggers when one poll option is available
                emoji_code = self.responses[user_id][0]
            except KeyError or ValueError:
                # User id did not respond yet
                return None

        try:
            # Remove the emoji code from the user responses
            self.responses[user_id].remove(emoji_code)

            # Remove response from option amounts
            self.options[emoji_code][1] = self.options[emoji_code][1] - 1
        except ValueError:
            return None

        # Return the removed emoji
        return emoji_code

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
            url=f"https://www.google.com/search?q={'+'.join(self.title.split())}",
            color=discord.Color.blue()
        )

        # Generate options info
        options_info = ''
        for option, info in self.options.items():
            options_info += f'{option} {info[0]} - {info[1]}\n'

        embed.add_field(name='Votes', value=options_info)

        embed.set_thumbnail(url=self.logo_url)

        return embed

    def get_emojis(self) -> List[str]:
        return list(self.options.keys())

    def get_user_reactions(self, user_id) -> List[str]:
        emojis = list(self.options.keys())
        return [emojis[emoji_idx] for emoji_idx in [self.responses[user_id]]]
