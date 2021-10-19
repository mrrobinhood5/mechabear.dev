import datetime

from disnake import Permissions, Option, OptionType
from disnake.ext.commands import Context, SubCommand
from utils.constants import *


class DmQuest:

    def __init__(self, ctx: Context, name):
        self.name = name
        self.dm = ctx.author
        self.server = ctx.guild
        self.quest_role = None
        self.category = None
        self.rp_channel = None
        self.ooc_channel = None
        self.dm_channel = None
        self.quest_members = []
        self.status = "Active"
        self.date_started = datetime.datetime.utcnow()
        self.date_completed = None
        self.description = ""

    @property
    def f(self):
        return {"dm": str(self.dm.id), "server": str(self.server.id)}

    async def create_channels(self, ctx: Context):
        self.quest_role = await self.server.create_role(name=self.quest_name, permissions=Permissions.text(),
                                                        mentionable=True,
                                                        reason=f'New Quest created by {self.dm.display_name} in '
                                                               f'MechaBear')
        perms = {ctx.guild.me: CHANNEL_ADMIN, ctx.guild.default_role: CHANNEL_READ}
        self.category = await ctx.guild.create_category(name=f'🏷{self.name}🏷')
        self.rp_channel = await self.category.create_text_channel(name=f'🎭rp-{self.name}', overwrites=perms)
        self.ooc_channel = await self.category.create_text_channel(name=f'🎲ooc-{self.name}', overwrites=perms)
        perms.update({self.quest_role: CHANNEL_READ_WRITE})
        self.dm_channel = await self.category.create_text_channel(name=f'🧩dm-{self.name}', overwrites=perms)

    async def destroy_channels(self, ctx: Context):
        pass

    def save(self, ctx: Context):
        # build the dict
        dm_quest = {
            "name": self.name,
            "dm": str(self.dm.id),
            "server": str(self.server.id),
            "quest_role": str(self.quest_role.id),
            "category": str(self.category.id),
            "rp_channel": str(self.rp_channel),
            "ooc_channel": str(self.ooc_channel),
            "dm_channel": str(self.dm_channel),
            "quest_members": self.quest_members,
            "status": self.status,
            "date_started": self.date_started,
            "date_completed": self.date_completed,
            "descriptions": self.description
        }
        ctx.bot.db.dm_quests.update_one(self.f, dm_quest)
        return

    def add_members(self):
        # add members to the quest db, and add roles
        pass

    def load(self, ctx: Context):
        quests = ctx.bot.db.dm_quests.find(self.f)
        async for quest in quests:
            if self.name in quest.name:
                self.name = quest.name
                self.dm = ctx.guild.get_member(int(quest.dm))
                self.server = int(self.server)
                self.quest_role = int(quest.quest_role)
                self.category = int(quest.category)
                self.rp_channel = int(quest.rp_channel)
                self.ooc_channel = int(quest.ooc_channel)
                self.dm_channel = int(quest.dm_channel)
                self.quest_members = quest.quest_members
                self.status = quest.status
                self.date_started = quest.date_started
                self.date_completed = quest.date_completed
                self.description = quest.description
            else:
                return await ctx.response.send_message("No Quests with that name")
        return

    def complete(self, ctx, description):
        # add final description
        self.description = description
        # deactivate status
        self.status = "Complete"
        # set the date
        self.date_completed = datetime.datetime.utcnow()
        # remove roles from members

        # destroy channels
        await self.destroy_channels()
