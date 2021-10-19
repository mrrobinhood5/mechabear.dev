from disnake.ext import commands
from disnake import Option, OptionType
from utils import checks
from utils.dmClasses import DmQuest, DmQuestNew


# from utils.classes import DmQuest


class DmCommands(commands.Cog, name='DM Commands'):

    def __init__(self, bot):
        self.bot = bot

    @checks.is_dm()
    @commands.slash_command(description="DM Commands")
    async def dm(self, inter):
        pass

    @dm.sub_command(name="new_quest", description="Starts a new quest",
                    options=[Option(name="name",
                                    description="The name of the quest, will also be used as the channel names",
                                    type=OptionType.string, required=True)])
    async def dm_new_quest(self, ctx, name):
        # make an object
        quest = DmQuest.make(ctx, name)
        # create channels
        await quest.create_channels(ctx)
        # save to db
        quest.save(ctx)
        # return embed
        return await ctx.response.send_message(f'New quest Created {quest.rp_channel.mention}')

    @dm.sub_command(name="finish_quest", description="Closes out a quest",
                    options=[Option("name", "The name of the quest",
                                    type=OptionType.string, required=True),
                             Option("description", "A synopsis of the quest", type=OptionType.string, required=True)])
    async def dm_finish_quest(self, ctx, name, description):
        # instantiate a quest object
        quest = DmQuest(ctx, name)
        # load it from db
        quest.load(ctx)
        # close it out
        quest.complete(ctx, description)
        # sve to db
        quest.save(ctx)
        return await ctx.response.send_message(f'Quest: `{quest.quest_name}` completed and added to DB.')


def setup(bot):
    bot.add_cog(DmCommands(bot))
