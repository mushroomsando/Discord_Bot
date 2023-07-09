from discord.ext import commands

class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    #TODO Creating a help code
    @commands.command(name = "!도움말" or "!도움", help = "도움말을 출력합니다.")
    async def help(self, ctx):
        await ctx.reply("준비중")
        print("Utilities -> hello "+"\033[32m"+"Execution Successful"+"\033[O")

async def setup(bot):
    await bot.add_cog(Utilities(bot))