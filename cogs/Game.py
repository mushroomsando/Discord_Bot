import discord
from discord.ext import commands
import random
from asyncio import TimeoutError

class Game(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name = "주사위")
    async def dice(self, ctx):
        await ctx.send(f"(데굴) {ctx.author.mention}님이 주사위를 굴려 {random.randrange(1,6)}이 나왔습니다.")

    @commands.command(name="자판기")
    async def Vending_machine(self, ctx):
        Vending_machine_list = ["코카콜라", "파워에이드", "물", "캔커피", "데운유유", "칠성사이다", "코카콜라 제로", "포카리스웨트", "쿨피스"]
        if random.random() < 0.8:  # 80% chance of getting a drink
            drink = random.choice(Vending_machine_list)
            await ctx.send(f"(덜그럭) {ctx.author.mention}님이 자판기에서 {drink}를 뽑았습니다.")
        else:
            await ctx.send(f"(덜그럭) {ctx.author.mention}님이 자판기에 돈을 넣었지만 아무것도 뽑히지 않았습니다.")
    
    @commands.command(name = "신이시여")
    async def God(self, ctx):
        god_answer = ["불확실하다.", 
                      "고통을 감내하면 열매를 맺을지니.", 
                      "아직 때가 아니다.", 
                      "지혜로은 선택을 해라.", 
                      "예측하기 어렵다.", 
                      "잘 생각해 보아라.", 
                      "가능성이 높지 않다.", 
                      "결정은 너에게 있을지니.",
                      "곧.",
                      "가능성이 있다.",
                      "그렇게 되지 않는다.",
                      "세상은 항상 의도대로 흘러기지 않을지니.",
                      "어리석은 선택이다."]
        if "?" in ctx.message.content:
            answer = random.choice(god_answer)
            await ctx.send(f'(계시){ctx.author.mention}님의 질문에 "{answer}" 라고 답하셨습니다.')
    
    @commands.command(name = "판사님")
    async def Judge(self, ctx):
        judge_answer = ["응 아니야", "응 맞아"]
        if "?" in ctx.message.content:
            answer = random.choice(judge_answer)
            await ctx.reply(f"(판결) {answer}")
    
    @commands.command(name = "노래방점수")
    async def Score(self, ctx):
        await ctx.send(f"(가수왕이 탄생했어요) {ctx.author.mention}님의 노래실력은...! {random.randrange(1,100)}점 입니다!")
    
    @commands.command(name = "가위바위보")
    async def Rock_paper_scissors(slef, ctx):
        await ctx.reply("준비중")
        #TODO

async def setup(bot):
    await bot.add_cog(Game(bot))