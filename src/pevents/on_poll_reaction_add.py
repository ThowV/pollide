import discord
import ppoll_store
import pvars


async def run(channel_id: int, message_id: int, user_id: int, emoji_code: str):
    # Get channel
    channel: discord.TextChannel = pvars.bot.get_channel(channel_id)

    # Get message
    message: discord.Message = await channel.fetch_message(message_id)

    # Check if the response is by the bot itself
    if message.author.id == user_id:
        return

    # Get the poll object
    poll = ppoll_store.get(message_id)

    if poll is None:
        return

    # Add the response and get the removed emoji if there is one
    emoji_code_removed = poll.add_response(user_id, emoji_code)

    # Remove the emoji from the reactions
    if emoji_code_removed is not None:
        user = await pvars.bot.fetch_user(user_id)
        await message.remove_reaction(emoji_code_removed, user)

    # Update the poll embed
    await message.edit(embed=poll.get_as_embed())
