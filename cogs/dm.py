from disnake.ext import commands
from utils import checks

# from utils.classes import DmQuest


class DmCommands(commands.Cog, name='DM Commands'):

    def __init__(self, bot):
        self.bot = bot

    @checks.is_dm()
    @commands.command(name="new_quest")
    async def dm_new_quest(self, ctx, *quest_name):
        # quest = await DmQuest.create(ctx, quest_name)
        # quest.save_quest()
        # return await ctx.send(f'Quest Name > `{quest.quest_name}`\n'
        #                       f'Category > `{quest.category.name}`\n'
        #                       f'RP Channel > `{quest.rp_channel.name}`\n'
        #                       f'OOC Channel > `{quest.ooc_channel.name}`\n'
        #                       f'DM Channel > `{quest.dm_channel.name}`\n')
        return await ctx.send('DM is creating a new quest')


def setup(bot):
    bot.add_cog(DmCommands(bot))
