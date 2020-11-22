import shlex

import discord
from discord.ext import commands

from pparser import parse, check_formatting
from ppoll_manager import create_poll, respond_to_poll


async def create(ctx: commands.Context, msg: str):
    options = {
        # Option    [Value, Mandatory]  Description                     Type    Format
        '-n':       [None, True],       # Name                          str
        '-d':       [None, False],      # Description                   str
        '-o':       [None, False],      # Options                       str     (opt/opt/opt)
        '-m':       [None, False],      # Maximum number of responses   int     (int/int/int) / int
        '-c':       [None, False],      # Destination channel           str
        '-ct':      [None, False],      # Poll closing time             str     (hh:mm)
        '-cd':      [None, False]       # Poll closing date             str     (dd:mm:yyy)
    }

    # Check and parse options/arguments
    input = shlex.split(msg)

    try:
        check_formatting('create', input, options)
        input = parse(input, options)

        # Execute command
        poll = create_poll(input)
        await ctx.send(embed=discord.Embed(
            title=f"Poll #{id(poll)}: {poll.name}",
            description=poll.description,
            color=discord.Color.blue()
        ))
    except Exception as e:
        await ctx.send(embed=discord.Embed(
            title='Error',
            description=str(e),
            timestamp='21:00',
            color=discord.Color.red()
        ))
        return

    #print(args)

    """
    # Execute command
    create_poll(name, args)

    # Create response message
    filtered_args = {k: v for k, v in args.items() if v is not None}

    response = discord.Embed(
        title=name,
        description=
    )"""

    # Create the poll and send a response
    #await ctx.send(args)


async def respond(ctx: commands.Context, pid: int, response: str):
    """"
            Poll id     str
            Response    str (Y/N/M)
    """

    # Respond to the poll and send a response
    await ctx.send(respond_to_poll(pid, response))
