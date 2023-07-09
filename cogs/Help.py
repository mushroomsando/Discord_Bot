import discord
from discord.ext import commands

class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name = "도움말")
    async def help(self, ctx):
        return 0
        #TODO

async def setup(bot):
    await bot.add_cog(Utilities(bot))