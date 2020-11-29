import discord

from ppol import PPoll


async def run(reaction: discord.Reaction, user: discord.User, poll: PPoll):
    message: discord.Message = reaction.message

    # Check if the emoji is a valid option.
    try:
        emoji_idx = poll.get_emojis().index(reaction.emoji)
    except ValueError:
        await reaction.remove(user)
        return

    # Add the response and update the message
    poll.add_response(user.id, emoji_idx)
    await message.edit(embed=poll.get_as_embed())

