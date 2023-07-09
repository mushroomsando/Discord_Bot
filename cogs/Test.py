import discord
from discord.ext import commands

#TODO modify File
class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "hello")
    async def hello(self, ctx):
        await ctx.reply("Hello, world!")
        print("Core -> hello "+"\033[32m"+"Execution Successful"+"\033[O")
    
    @commands.command(name = "핑", help = "레이턴시를 출력합니다.")
    async def ping(self, ctx):
        latency = self.bot.latency
        await ctx.reply(f'핑: {round(latency * 1000)}ms')
        print("Core -> ping "+"\033[32m"+"Execution Successful"+"\033[O")
        
    
async def setup(bot):
    await bot.add_cog(Test(bot))