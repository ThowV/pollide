import discord
import ppoll_store


async def run(reaction: discord.Reaction, user: discord.User):
    message: discord.Message = reaction.message

    # Check if the response is by the bot itself
    if message.author.id == user.id:
        return

    # Get the poll object
    poll = ppoll_store.get(message.id)

    # Add the response and update the message
    poll.add_response(user.id, reaction.emoji)
    await message.edit(embed=poll.get_as_embed())

