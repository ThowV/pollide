import importlib
import os
import pkgutil
import discord
import pcommands

from discord.ext import commands
from dotenv import load_dotenv
from pcommands import pcommand


# Create custom decorator
def conditional_has_role(dec, condition):
    def decorator(func):
        if not condition:
            # Return the function unchanged, not decorated.
            return func
        # Return the function changed, decorated with a parameter.
        return (dec(condition))(func)

    return decorator


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
pcommands = {command for command in pcommand.PCommand.__subclasses__()}

# Create discord command for each command
for command in pcommands:
    command_inst = command()

    @bot.command(
        name=command_inst.parser.prog,
        help=command_inst.parser.description,
        pass_context=True
    )
    @conditional_has_role(commands.has_role, command_inst.get_role())
    async def dcommand(ctx: commands.Context, *, input: str, command=command_inst):
        await command.run(ctx, input)


# Subscribe to bot events
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.event
async def on_command_error(ctx: commands.Context, error: commands.CommandError):
    print(error)
    if isinstance(error, commands.errors.CheckFailure):
        embed = discord.Embed(
            title='You must have the role PollideU to execute this command.',
            description='Type p:help to see all commands and required roles',
            color=discord.Color.red()
        )

        await ctx.send(embed=embed)


# Run discord client.
bot.run(DISCORD_TOKEN)
