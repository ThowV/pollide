import shlex
import traceback
from typing import List

import discord
from discord.ext import commands

from pparser import parse
from ppoll_manager import create_poll, respond_to_poll


async def create(ctx: commands.Context, msg: str):
    options = {
        # Option    [Value, Mandatory,  [Format]]           Description
        '-n':       [None,  True,       [str]],             # Name
        '-d':       [None,  False,      [str]],             # Description
        '-o':       [None,  False,      [List[str], str]],  # Options
        '-a':       [None,  False,      [bool]],            # Anonymous
        '-m':       [None,  False,      [List[int], int]],  # Maximum number of responses
        '-mr':      [None,  False,      [str]],             # Mention role
        '-c':       [None,  False,      [str]],             # Destination
        '-ct':      [None,  False,      [str]],             # Poll closing time
        '-cd':      [None,  False,      [str]]              # Poll closing date
    }

    # Check and parse options/arguments
    input = shlex.split(msg)

    try:
        input = parse('create', input, options)

        # Execute command
        poll = create_poll(input)

        embed = discord.Embed(
            title=f"Poll #{id(poll)}: {poll.name}",
            description=poll.description,
            url=f"https://www.google.com/search?q={poll.name}",
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=poll.logo_url)

        print(embed.to_dict())

        await ctx.send(embed=embed)
    except Exception as e:
        traceback.print_exc()

        await ctx.send(embed=discord.Embed(
            title='Error',
            description=str(e),
            color=discord.Color.red()
        ))

        return


async def respond(ctx: commands.Context, pid: int, response: str):
    # Respond to the poll and send a response
    await ctx.send(respond_to_poll(pid, response))
