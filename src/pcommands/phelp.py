import argparse
import discord

from pbot import get_pcommands
from pcommands.pcommand import PCommand


def generate_help():
    help_msg = '```'

    for pcommand in get_pcommands():
        help_msg += '\n{}{}'.format(pcommand.get_name().ljust(10), pcommand.get_info())

    help_msg += '```'

    return help_msg


class PHelp(PCommand):
    @staticmethod
    def get_name() -> str:
        return 'help'

    @staticmethod
    def get_info() -> str:
        return 'Shows this help message.'

    def __init__(self):
        self.parser = argparse.ArgumentParser()

    async def run(self, context: discord.ext.commands.Context, input: str):
        embed = discord.Embed(
            description="Pollide is a bot... If you haven't noticed yet",
            color=discord.Color.orange()
        )

        embed.set_author(name='PollideBot', url='https://github.com/ThowV/pollide-bot',
                         icon_url='https://i.imgur.com/RPrw70n.png')

        embed.add_field(name='Commands', value=generate_help())
        await context.send(embed=embed)

    def get_command_help(self, command=str):
        pass
