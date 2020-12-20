from discord.ext import commands as dcommands

bot: dcommands.Bot


def get_alphabet_emoji(index: int):
    index = 230 + index
    alphabet_emoji_hex = str.upper(str(hex(index)).replace('0x', ''))
    emoji_hex = '\\U0001F1' + alphabet_emoji_hex

    return emoji_hex.encode('ascii').decode('unicode-escape')
