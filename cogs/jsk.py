from disnake.ext import commands

from jishaku.cog import STANDARD_FEATURES


class CustomDebugCog(*STANDARD_FEATURES):
    pass


def setup(bot: commands.Bot):
    bot.add_cog(CustomDebugCog(bot=bot))
