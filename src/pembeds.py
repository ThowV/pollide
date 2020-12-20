import discord

error_color = discord.Color.red()


class PError:
    @staticmethod
    def get_embed(command: str, message: str, reason: str = '') -> discord.Embed:
        embed = discord.Embed(
            title=f'{command.capitalize()}',
            description=f'{message}\n\nType "p:help {command}" for information on the command and its arguments.',
            color=error_color
        )

        if reason:
            embed.add_field(
                name='Reason',
                value=reason
            )

        return embed


class PArgumentError:
    @staticmethod
    def get_embed(command: str, argument: str) -> discord.Embed:
        return PError.get_embed(command, f'Wrong use of the {argument} argument')
