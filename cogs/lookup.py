from disnake.ext import commands
from disnake import Option, OptionType
from utils.lookupClasses import LookupLanguage, LookupFeat


class LookupCommands(commands.Cog, name="Lookup Commands"):

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Lookup Commands")
    async def lookup(self, inter):
        pass

    @lookup.sub_command(name="languages", description="Lookup Language information",
                        options=[Option("keyword", "part or all of the language",
                                        type=OptionType.string, required=True)])
    async def languages(self, ctx, keyword):
        await ctx.response.defer()
        language = LookupLanguage(keyword)
        return await ctx.edit_original_message(embeds=[language.build_embed(ctx)])

    @lookup.sub_command(name="feats", description="Lookup feats information",
                        options=[Option("keyword", "part or all of the feat",
                                        type=OptionType.string, required=True)])
    async def feats(self, ctx, keyword):
        await ctx.response.defer()
        feat = LookupFeat(keyword)
        return await ctx.edit_original_message(embeds=[feat.build_embed(ctx)])


def setup(bot):
    bot.add_cog(LookupCommands(bot))
