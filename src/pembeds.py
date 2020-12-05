import discord

error_color = discord.Color.red()


class PError:
    @staticmethod
    def get_embed(command: str, message: str) -> discord.Embed:
        embed = discord.Embed(
            title=f'{command.capitalize()}: {message}.',
            description=f'Type "p:help {command}" for information on the command and its arguments.',
            color=error_color
        )

        return embed


class PArgumentError:
    @staticmethod
    def get_embed(command: str, argument: str) -> discord.Embed:
        return PError.get_embed(command, f'Wrong use of the {argument} argument')
