import shlex

from discord.ext import commands

from pparser import parse_optional_args
from ppoll_manager import create_poll


async def create(ctx: commands.Context, msg: str):
    args = shlex.split(msg)
    """"
            Name                            str
    -m      Maximum number of responses:    int
    -c      Destination channel:            str
    -ct     Poll closing time:              str (hh:mm)
    -cd     Poll closing date:              str (dd:mm:yyyy)
    """

    # First argument must be name
    name = args[0]
    args.remove(name)

    # Parse optional arguments
    optional_args = parse_optional_args(
        args,
        {
            '-m':   None,   # Maximum number of responses
            '-c':   None,   # Destination channel
            '-ct':  None,   # Poll closing time
            '-cd':  None    # Poll closing date
        }
    )

    # Create the poll and send a response
    await ctx.send(create_poll(name, optional_args))
