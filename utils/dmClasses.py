from disnake import Permissions, PermissionOverwrite
from disnake.ext.commands import Context

dm_roles
EVERYONE_PERMS = (Permissions(0), Permissions(1024))
ME_PERMS = (Permissions(1024), Permissions(0))
SYSTEM_BOT_PERMS = (Permissions(36871952), Permissions(0))
QUEST_ROLE_PERMS = (Permissions(2048), Permissions(1024))


class DmQuest:

    @classmethod
    async def create(cls, ctx: Context, quest_name):
        self = DmQuest()
        self.quest_name = " ".join(quest_name)
        self.owner = ctx.author
        self.server = ctx.guild
        self.quest_role = await self.server.create_role(name=self.quest_name, permissions=Permissions.text(),
                                                        mentionable=True,
                                                        reason=f'New Quest created by {self.owner.display_name} in '
                                                               f'MechaBear')
        player_overwrites = {
            ctx.guild.default_role: PermissionOverwrite(read_messages=False),
            ctx.guild.me: PermissionOverwrite(read_messages=True)
        }
        dm_overwrites = {
            ctx.guild.default_role: PermissionOverwrite(read_messages=False),
            ctx.guild.me: PermissionOverwrite(read_messages=True)

        }
        self.category = await ctx.guild.create_category(name=f'🏷{self.quest_name}🏷')
        self.rp_channel = await self.category.create_text_channel(name=f'🎭rp-{self.quest_name}', overwrites=QUEST)
        self.ooc_channel = await self.category.create_text_channel(name=f'🎲ooc-{self.quest_name}', overwrites=overwrites)
        self.dm_channel = await self.category.create_text_channel(name=f'🧩dm-{self.quest_name}', overwrites=dm_overwrites)
        self.quest_members = []
        return self

    def save_quest(self):
        dm_quest = {
            "quest_owner": str(self.owner.id),
            "quest_server": str(self.server.id),
            "quest_name": self.quest_name,
            "quest_role": str(self.quest_role.id),
            "quest_category": str(self.category.id),
            "quest_members": self.quest_members
        }
        print(dm_quest)
        return