# bot.py
import os

import discord
from dotenv import load_dotenv

# Get the bot token
load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

# Create a discord client, subscribe to events and run the client
client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

client.run(TOKEN)
