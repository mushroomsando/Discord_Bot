from discord.ext import commands
import time

class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name = "현제시간")
    async def now_time(self ,ctx):
        return 0
        #TODO
    
    @commands.command(name = "핑")
    async def ping(self, ctx):
        return 0
        #TODO
    
    @commands.command(name = "계산기")
    async def caculate(slef, ctx, expression):
        return 0
        #TODO

async def setup(bot):
    await bot.add_cog(Utilities(bot))