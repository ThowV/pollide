import argparse
import discord

from pbot import get_pcommands
from pcommands.pcommand import PCommand
from pembeds import PArgumentError, PError


def generate_help() -> str:
    help_msg = '```'

    for pcommand in get_pcommands():
        help_msg += '\n{}{}'.format(pcommand.get_name().ljust(10), pcommand.get_info())

    help_msg += '```\nType p:help command_name for extra information.'

    return help_msg


def get_help_embed() -> discord.Embed:
    embed = discord.Embed(
        description="Pollide is a bot... If you haven't noticed yet",
        color=discord.Color.orange()
    )

    embed.set_author(name='PollideBot', url='https://github.com/ThowV/pollide-bot',
                     icon_url='https://i.imgur.com/RPrw70n.png')

    embed.add_field(name='Commands', value=generate_help())

    return embed


def generate_command_help(command: str) -> str:
    for pcommand in get_pcommands():
        if pcommand.get_name() == command:
            return '```' + pcommand.parser.format_help() + '```'

    return ''


def get_command_help_embed(command: str) -> discord.Embed:
    help = generate_command_help(command)
    embed = None

    if help:
        embed = discord.Embed(
            title=f'{command.capitalize()} information.',
            description=help,
            color=discord.Color.orange()
        )

    if not help:
        embed = PError.get_embed(PHelp.get_name(), f'{command} is not a valid command')

    return embed


class PHelp(PCommand):
    @staticmethod
    def get_name() -> str:
        return 'help'

    @staticmethod
    def get_info() -> str:
        return 'Shows this help message.'

    def __init__(self):
        self.parser = argparse.ArgumentParser(
            prog='help',
            description='Shows this help message'
        )

    async def run(self, context: discord.ext.commands.Context, input: str):
        if input:
            await context.send(embed=get_command_help_embed(input))
        else:
            await context.send(embed=get_help_embed())

    def get_command_help(self, command: str):
        pass
