from discord.ext import commands

class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name = "채팅청소")
    async def message_clear(self, ctx):
        return 0
        #TODO
    
    @commands.command(name = "킥")
    async def user_kick(self, ctx):
        return 0
        #TODO
    
    @commands.command(name = "밴")
    async def user_ban(self, ctx):
        return 0
        #TODO

    @commands.command(name = "타임아웃")
    async def user_timeout(self, ctx):
        return 0
        #TODO 어떻게 하는거지;
    
    @commands.command(name = "서버정보")
    async def sever_info(self, ctx):
        return 0
        #TODO

async def setup(bot):
    await bot.add_cog(Utilities(bot))