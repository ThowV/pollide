import importlib
import os
import pkgutil

import discord
from discord.ext import commands as dcommands
from dotenv import load_dotenv

import pcommands
import pevents
import pvars
from pevents import on_poll_reaction_add, on_poll_reaction_remove
from pcommands import pcommand


def get_pcommands():
    # Import all command modules
    for importer, command_module, is_package in pkgutil.walk_packages(
            path=pcommands.__path__, prefix=pcommands.__name__ + '.', onerror=lambda x: None):
        try:
            importlib.import_module(command_module)
            print(f'Found command module: {command_module}')
        except Exception as e:
            print(f'Something went wrong in {command_module} - {e}')

    # Get all commands
    pcommands_inst = {command() for command in pcommand.PCommand.__subclasses__()}

    return pcommands_inst


if __name__ == '__main__':
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
    pvars.bot = dcommands.Bot(command_prefix='p:')
    pvars.bot.remove_command('help')

    pcommands_inst = get_pcommands()

    # Create discord command for each command
    for pcommand in pcommands_inst:
        @conditional_has_role(dcommands.has_role, pcommand.get_role())
        @pvars.bot.command(
            name=pcommand.get_name(),
            pass_context=True
        )
        async def dcommand(ctx: dcommands.Context, *, input='', command=pcommand):
            await command.run(ctx, input)


    # Subscribe to bot events
    @pvars.bot.event
    async def on_ready():
        await pvars.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='p:help'))
        print(f'{pvars.bot.user.name} has connected to Discord!')


    @pvars.bot.event
    async def on_command_error(ctx: dcommands.Context, error: dcommands.CommandError):
        if isinstance(error, dcommands.errors.CheckFailure):
            embed = discord.Embed(
                title='You must have the role PollideU to execute this command.',
                description='Type p:help to see all commands and required roles',
                color=discord.Color.red()
            )

            await ctx.send(embed=embed)


    @pvars.bot.event
    async def on_reaction_add(reaction: discord.Reaction, user: discord.User):
        await pevents.on_poll_reaction_add.run(reaction, user)


    @pvars.bot.event
    async def on_reaction_remove(reaction: discord.Reaction, user: discord.User):
        await pevents.on_poll_reaction_remove.run(reaction, user)

    @pvars.bot.event
    async def on_raw_reaction_remove(payload: discord.RawReactionActionEvent):
        await pevents.on_poll_reaction_remove.run(
            payload.channel_id, payload.message_id, payload.user_id, payload.emoji.name
        )


    # Run discord client.
    pvars.bot.run(DISCORD_TOKEN)
