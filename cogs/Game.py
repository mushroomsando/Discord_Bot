import discord
from discord.ext import commands
import random
from asyncio import TimeoutError

class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name = "주사위")
    async def dice(self, ctx):
        await ctx.send(f"(데굴) {ctx.author.mention}님이 주사위를 굴려 {random.randrange(1,6)}이 나왔습니다.")

    @commands.command(name = "자판기")
    async def Vending_machine(self, ctx):
        Vending_machine_list = ["코카콜라", "파워에이드", "물", "캔커피", "데운유유", "칠성사이다", "코카콜라 제로", "포카리스웨트"]
        await ctx.send(f"(덜그럭) {ctx.author.mention}님이 자판기에서 {random.choice(Vending_machine_list)}를 뽑았습니다.")
    
    @commands.command(name = "신이시여")
    async def God(self, ctx):
        return 0
        #TODO
    
    @commands.command(name = "판사님")
    async def Judge(self, ctx):
        return 0
        #TODO
    
    @commands.command(name = "노래방점수")
    async def Score(self, ctx):
        await ctx.send(f"(가수왕이 탄생했어요!) {ctx.author.mention}님의 노래점수는 {random.randrange(1,100)}점 입니다!")
    
    @commands.command(name = "가위바위보")
    async def Rock_paper_scissors(slef, ctx):
        return 0
        #TODO

async def setup(bot):
    await bot.add_cog(Utilities(bot))