import argparse
import discord
import ppoll_store

from pcommands.pcommand import PCommand
from ppol import PPoll


class PCreate(PCommand):
    @staticmethod
    def get_name() -> str:
        return 'create'

    @staticmethod
    def get_info() -> str:
        return 'Create a poll.'

    @staticmethod
    def get_role() -> str:
        return 'PollideU'

    def __init__(self):
        self.parser = argparse.ArgumentParser()

        # Add arguments
        self.parser.add_argument('title', nargs='+',
                                 help='The title of the poll.')

        self.parser.add_argument('-d', '--description', nargs='+',
                                 help='Description of the poll.')

        self.parser.add_argument('-o', '--options',     action='extend', nargs='+', type=str,
                                 help='Options users can pick from.')

        self.parser.add_argument('-m', '--maximum', action='extend', nargs='+', type=int, dest='max_responses',
                                 help='Maximum number of responses.')

        self.parser.add_argument('-a', '--anonymous',   action='store_true', default=False,
                                 help='Whether this poll is anonymous or not. (Default: %(default)s)')

        self.parser.add_argument('-r', '--roles',    action='extend', nargs='+', type=str,
                                 help='Which roles are mentioned.')

        self.parser.add_argument('-c', '--channel', dest='dest_channel',
                                 help='Destination channel of the poll.')

        self.parser.add_argument('-ct', '--closing_time',
                                 help='Time the poll closes.')

        self.parser.add_argument('-cd', '--closing_date',
                                 help='Date the poll closes.')

    async def run(self, context: discord.ext.commands.Context, input: str):
        poll = PPoll()
        self.parser.parse_args(input.split(), namespace=poll)

        ppoll_store.store(poll)
        await context.send(embed=poll.get_as_embed())
