from config import *
from disnake.ext import commands


def is_god():
    async def predicate(ctx):
        if str(ctx.author.id) == BOT_AUTHOR_ID:
            return True
        else:
            ctx.send("You are not the Owner of this bot, I DONT KNOW YOU!")

    return commands.check(predicate)


def is_dm():
    async def predicate(ctx):
        for role in ctx.author.roles:
            if role.name == "Quest Master" or role.name == "Dungeon Master":
                return True
        else:
            await ctx.send("You are not a DM/GM")

    return commands.check(predicate)


def is_owner():
    async def predicate(ctx):
        if ctx.author.id == ctx.guild.owner.id:
            return True
        else:
            ctx.send("You are not the Guild Owner, Only he has the power. ")

    return commands.check(predicate)
