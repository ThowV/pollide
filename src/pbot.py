import importlib
import os
import pkgutil
import discord
import pcommands

from discord.ext import commands
from dotenv import load_dotenv
from pcommands import pcommand

# Get the bot token and create a discord client.
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
bot = commands.Bot(command_prefix='p:')

# Import all command modules
for importer, command_module, is_package in pkgutil.walk_packages(
        path=pcommands.__path__, prefix=pcommands.__name__ + '.', onerror=lambda x: None):
    try:
        importlib.import_module(command_module)
        print(f'Found command module: {command_module}')
    except Exception as e:
        print(f'Something went wrong in {command_module} - {e}')

# Get all commands
commands = {command for command in pcommand.PCommand.__subclasses__()}

# Create discord command for each command
for command in commands:
    command_inst = command()

    @bot.command(
        name=command_inst.parser.prog,
        help=command_inst.parser.description,
        pass_context=True
    )
    async def dcommand(ctx: discord.ext.commands.Context, *, input: str, command=command_inst):
        await command.run(ctx, input)

# Run discord client.
bot.run(DISCORD_TOKEN)
