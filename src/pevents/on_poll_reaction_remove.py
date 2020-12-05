import discord
import ppoll_store
import pvars


async def run(channel_id: int, message_id: int, user_id: int, emoji: str):
    # Get channel
    channel: discord.TextChannel = pvars.bot.get_channel(channel_id)

    # Get message
    message: discord.Message = await channel.fetch_message(message_id)

    # Check if the response is by the bot itself
    if message.author.id == user_id:
        return

    # Get the poll object
    poll = ppoll_store.get(message_id)

    if not poll:
        return

    # Add the response and update the message
    poll.remove_response(user_id, emoji)
    await message.edit(embed=poll.get_as_embed())

