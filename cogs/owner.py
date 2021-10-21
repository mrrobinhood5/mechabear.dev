import disnake
from disnake.ext import commands
from disnake import Option, OptionType
from utils import checks


class OwnerCommands(commands.Cog, name='Owner Commands'):

    def __init__(self, bot):
        self.bot = bot

    @checks.is_owner()
    @commands.slash_command(name="setupdmroles", description="Commands to Setup the Bot",
                            options=[Option("role", "Pass the @role to be added as DM ", type=OptionType.role, required=True)])
    # @commands.command(name="add_dm_roles")
    async def add_dm_roles(self, ctx, role):
        # get current roles
        _f = {"server_id": ctx.guild.id}
        _r = await self.bot.db.settings.find_one(_f)
        if not _r:
            dm_roles = []
        else:
            dm_roles = _r["dm_roles"]
        dm_roles.append(role.id) if role.id not in dm_roles else 0
        self.bot.db.settings.update_one(_f, {"$set": {"dm_roles": dm_roles}}, upsert=True)
        await ctx.response.send_message(f'Current Roles are {[ctx.guild.get_role(role_id).name for role_id in dm_roles]}')


def setup(bot):
    bot.add_cog(OwnerCommands(bot))
