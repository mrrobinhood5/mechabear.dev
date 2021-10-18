from config import *
from disnake.ext import commands


def is_owner():
    async def predicate(ctx):
        if str(ctx.author.id) == BOT_AUTHOR_ID:
            return True
        else:
            ctx.send("You are not the Owner of this bot, I DONT KNOW YOU!")

    return commands.check(predicate)
