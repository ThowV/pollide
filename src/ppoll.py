import os
import discord
import requests
import pvars

from typing import List, Union

from perrors import OptionOverflowError


class PPoll:
    # Poll data
    logo_url: str
    title: str
    description: Union[str, None]
    options: {str: [str, int]}  # Emoji code: [Option description, Response amount]
    responses: {int: [str, [str]]}  # User id: [User name, [Emoji codes]]
    response_amount: int
    multi_options: bool
    anonymous: bool
    roles: [str]
    dest_channel: str
    closing_time: str
    closing_date: str

    # Parsed destination data, will be modified inside clean
    max_responses: Union[List[int], int, None]
    option_descriptions: [str]

    def __init__(self):
        self.options = {
            '\U00002705': ['Yes', 0],
            '\U00002754': ['Maybe', 0],
            '\U0001F1FD': ['No', 0]
        }
        self.responses = {}
        self.response_amount = 0

        self.max_responses = []
        self.option_descriptions = []

    def clean(self):
        # Set title, description and response amount
        self.title = ' '.join(self.title)
        self.description = ' '.join(self.description) if self.description else None

        # Set option descriptions and options
        if self.option_descriptions:
            self.options = {}

            in_option = False
            option_emoji = ''
            option_pointer = 0
            for option_part in self.option_descriptions:
                add_part_to_option = in_option

                # Check if the string holds the quotation mark
                if '"' in option_part:
                    option_part = option_part.replace('"', '')
                    # Flip the in option boolean
                    in_option = not in_option

                    # If we are about to build an option create an entry in the options dictionary
                    if in_option:
                        add_part_to_option = True
                        option_emoji = pvars.get_alphabet_emoji(option_pointer)
                        self.options[option_emoji] = ['', 0]
                        option_pointer += 1

                # Add the option part to the option it belongs to
                if add_part_to_option:
                    self.options[option_emoji][0] += ' ' + option_part

            # Check if too many options were provided
            if len(self.options) > 20:
                raise OptionOverflowError(
                    20, len(self.options), 'Discord only supports 20 emojis.'
                )

        # Set the max response amount for each option
        if len(self.max_responses) == 0:
            self.max_responses = None
        elif len(self.max_responses) == 1 and self.max_responses[0] > 0:
            self.max_responses = self.max_responses[0]

        for i, (option, info) in enumerate(self.options.items()):
            if type(self.max_responses) is list and i < len(self.max_responses) and self.max_responses[i] >= 0:
                info.append(self.max_responses[i])
            else:
                info.append(0)

        # Set the logo
        self.logo_url = self.get_logo_url()

    def add_response(self, user_id: int, user_name: str, emoji_code: str) -> Union[str, None]:
        """Return the the emoji code that was removed"""

        emoji_code_removed = None

        # Check if the maximum of responses has been reached
        if type(self.max_responses) is int and self.max_responses <= self.response_amount:
            return emoji_code

        if self.options[emoji_code][2] != 0 and self.options[emoji_code][1] >= self.options[emoji_code][2]:
            return emoji_code

        # Check if multiple responses are allowed, if not, remove last response
        if not self.multi_options:
            emoji_code_removed = self.remove_response(user_id)

        # Add response
        if user_id not in self.responses:
            self.responses[user_id] = [user_name, []]

        self.responses[user_id][1].append(emoji_code)

        # Add one to response amount of option and general response amount
        self.options[emoji_code][1] += 1
        self.response_amount += 1

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
                emoji_code = self.responses[user_id][1][0]
            except KeyError or ValueError:
                # User id did not respond yet
                return None

        try:
            # Remove the emoji code from the user responses
            self.responses[user_id][1].remove(emoji_code)

            # Remove response from option amounts and general response amount
            self.options[emoji_code][1] -= 1
            self.response_amount -= 1
        except ValueError or KeyError:
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
        for emoji_code, option in self.options.items():
            # Get the emoji_code and amount of responses
            options_info += f'{emoji_code} {option[0]} - '

            if option[2] > 0:
                options_info += f'({option[1]}/{option[2]})'
            else:
                options_info += f'{option[1]}'

            options_info += f'\n'

            # Get the users that responded to each option
            user_responses = ''
            for response in self.responses.values():
                if emoji_code in response[1]:
                    user_responses += '\n' + response[0]

            if user_responses:
                options_info += '```' + user_responses + '```'

        # Generate field name
        field_name = f'Votes ({self.response_amount}'
        if type(self.max_responses) is int and self.max_responses > 0:
            field_name += f'/{self.max_responses}'
        field_name += ')'

        # Finalize the embed
        embed.add_field(name=field_name, value=options_info)
        embed.set_thumbnail(url=self.logo_url)

        return embed

    def get_emojis(self) -> [str]:
        return list(self.options.keys())

    def get_user_reactions(self, user_id) -> [str]:
        emojis = list(self.options.keys())
        return [emojis[emoji_idx] for emoji_idx in [self.responses[user_id][1]]]
