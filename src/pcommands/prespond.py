import argparse
import discord
import ppoll_store

from pcommands.pcommand import PCommand


class Create(PCommand):
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            prog='respond',
            description='Respond to a poll (Requires the PollideU role.)'
        )

        # Add arguments
        self.parser.add_argument('poll_id', type=int,
                                 help='The id of the poll.')

        self.parser.add_argument('option_id', type=int,
                                 help='The chosen option identified by id')

    async def run(self, context: discord.ext.commands.Context, input: str):
        namespace = self.parser.parse_args(input.split())

        print(vars(namespace))
        poll = ppoll_store.get(namespace.poll_id)

        if poll:
            poll.respond(namespace.option_id)
            await context.send(poll.get_responses())
