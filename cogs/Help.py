from discord.ext import commands
import discord

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="도움말")
    async def help(self, ctx):
        embed = discord.Embed(title="📝 Command List",description="안녕하세요! 만나서 반갑습니다.", color=0x00aaff)
        embed.add_field(name = "🛠️ TOOL", value="!핑 \n !현제시간 \n !계산기 [수식]", inline=False)
        embed.add_field(name = "🎮 GAME", value="!주사위 \n !자판기 \n !판사님 [아무말]? \n !판사님 [아무말]? \n !가위바위보 (개발중)", inline=False)
        embed.add_field(name = "⚙️ SEVER TOOL", value="개발중", inline=False)
        embed.set_footer(text = "Copyright (C) 2023 By Mushroomsando. All right reserved.")
        await ctx.author.send(embed=embed)
        await ctx.message.add_reaction("✅")
    
async def setup(bot):
    await bot.add_cog(Help(bot))