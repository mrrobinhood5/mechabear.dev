import disnake
from disnake.ext import commands


class DevCommands(commands.Cog, name='Developer', command_attrs=dict(hidden=True)):
    """These are the developer commands"""

    def __init__(self, bot):
        self.bot = bot

    # @bot_checks.is_admin()
    @commands.command(name="load")
    async def load(self, ctx, cog):
        """
        Loads a cog.
        """
        await ctx.message.delete()
        cog = f'cogs.{cog}'
        try:
            self.bot.load_extension(cog)
            await ctx.send(f"`{cog}` has successfully been loaded.")
        except commands.errors.ExtensionNotFound:
            await ctx.send(f"`{cog}` does not exist!")

    @commands.slash_command(description="Responds with 'World'")
    async def hello(self, inter: disnake.ApplicationCommandInteraction):
        await inter.response.send_message("World")


def setup(bot):
    bot.add_cog(DevCommands(bot))
