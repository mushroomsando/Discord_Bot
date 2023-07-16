from discord.ext import commands
import discord

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="도움말")
    async def help(self, ctx):
        embed = discord.Embed(title="📝 Command List",description="각 명령어의 기능이 굼금하다면 여기서 !정보 [명령어]를 입력해 주세요.", color=0x00aaff)
        embed.add_field(name = "🛠️ TOOL", value="!핑 \n !현제시간 \n !계산기 [수식] \n !도움말 \n !정보 [명령어 (접두사 '!'는 제거하고 입력)]", inline=False)
        embed.add_field(name = "🎮 GAME", value="!주사위 \n !자판기 \n !판사님 [아무말]? \n !판사님 [아무말]? \n !가위바위보 (개발중)", inline=False)
        embed.add_field(name = "⚙️ SEVER TOOL", value="!채팅청소 [청소 갯수] \n !킥 [유저] \n !밴 [유저] \n !언벤 [유저] \n !서버정보", inline=False)
        embed.set_footer(text = "Copyright (C) 2023 By Mushroomsando. All right reserved.")
        await ctx.author.send(embed=embed)
        await ctx.message.add_reaction("✅")
    
    @commands.command(name = "정보")
    async def command_info(slef, ctx, command): # type: ignore
        if isinstance(ctx.channel, discord.DMChannel):
            if command:
                await ctx.reply(f"{command} 입력")
            else:
                await ctx.reply("입력받지 않음")
        else:
            embed = discord.Embed(title="⚙️ INFO", description=f"이 명령어는 DM에서만 사용할 수 있어요.", color=0xffdd00)
            embed.set_footer(text="Copyright (C) 2023 By Mushroomsando. All right reserved")
            await ctx.reply(embed=embed)

async def setup(bot):
    await bot.add_cog(Help(bot))