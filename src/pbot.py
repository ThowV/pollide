# pbot.py
import os
import pcommands as pcommands

from discord.ext import commands
from dotenv import load_dotenv

role_msg = '(Requires the PollideU role.)'

# Get the bot token
load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

# Create a discord client, subscribe to events and run the client
bot = commands.Bot(command_prefix='p:')


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.event
async def on_command_error(ctx: commands.Context, error: commands.CommandError):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('Error: You must have the role PollideU to execute this command.')


@bot.command(
    name='create',
    help=f"{role_msg} Create a poll.",
    pass_context=True
)
@commands.has_role('PollideU')
async def cmd_create(ctx: commands.Context, *, msg: str):
    await pcommands.create(ctx, msg)

@bot.command(
    name='respond',
    help=f"{role_msg} Respond to a poll.",
)
async def cmd_create(ctx: commands.Context, pid: int, response: str):
    await pcommands.respond(ctx, pid, response)


bot.run(TOKEN)
