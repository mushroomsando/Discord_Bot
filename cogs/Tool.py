import discord
from discord.ext import commands
import time
import json
import ast

now = time.strftime(f"%Y년%m월%d일 %H:%M:%S", time.localtime())
def load_info():
    with open("DB\\version.json", "r", encoding="utf-8") as file:
        info = json.load(file)
    return info
info = load_info()

class Tool(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="현재시간")
    async def now_time(self, ctx):
        embed = discord.Embed(title="⏰ 현재 시간",description=f"현재 시간은 {now} 입니다",color=0x00aaff)
        embed.set_footer(text="Copyright (C) 2023 By Mushroomsando. All right reserved")
        await ctx.reply(embed=embed)
    
    @commands.command(name="핑")
    async def ping(self, ctx):
        latency = round(self.bot.latency * 1000)  # 밀리초(ms) 단위로 변환하여 소수점 첫째 자리까지 표기
        embed = discord.Embed(title="🏓 퐁!", description=f"{latency}ms", color=0x00aaff)
        embed.set_footer(text="Copyright (C) 2023 By Mushroomsando. All right reserved")
        await ctx.reply(embed=embed)

    @commands.command(name="패치노트")
    async def info(self, ctx):
        embed = discord.Embed(title="🛠️ INFO", description="HELLO WORLD!",color = 0x00aaff)
        embed.add_field(name = "version", value = info['version'], inline=False)
        embed.add_field(name = "패치노트", value = info['패치노트'], inline=False)
        embed.set_footer(text="u : 업데이트     f : 버그픽스     m: 로직 개선 또는 마이너 업데이트  \nd : 개발버전     b : 베타버전     r : 릴리즈")
        await ctx.reply(embed=embed)
    
    @commands.command(name="계산기")
    async def calculate(self, ctx, *, expression):
        try:
            # 파싱된 AST를 평가하여 수식 계산
            parsed_expression = ast.parse(expression, mode='eval')
            result = eval(compile(parsed_expression, filename="<string>", mode='eval'))

            embed = discord.Embed(title="🛠️ COMPLETE", color=0x00aaff)
            embed.add_field(name="수식", value=expression, inline=False)
            embed.add_field(name="계산결과", value=result, inline=False)
            embed.set_footer(text="Copyright (C) 2023 By Mushroomsando. All right reserved")
            await ctx.reply(embed=embed)
        except ZeroDivisionError:
            embed = discord.Embed(title="🛠️ ERROR", description="0으로 나눌 수 없어요.", color=0xff0000)
            embed.set_footer(text="Copyright (C) 2023 By Mushroomsando. All right reserved")
            await ctx.reply(embed=embed)
        except SyntaxError:
            embed = discord.Embed(title="🛠️ ERROR", description="수식이 완성되지 않았어요.", color=0xff0000)
            embed.set_footer(text="Copyright (C) 2023 By Mushroomsando. All right reserved")
            await ctx.reply(embed=embed)
        except Exception as e:
            embed = discord.Embed(title="🛠️ ERROR", description=f"음... 무언가 잘못되었어요.", color=0xff0000)
            embed.add_field(name="오류내용", value=str(e))
            embed.set_footer(text="Copyright (C) 2023 By Mushroomsando. All right reserved")
            await ctx.reply(embed=embed)


    @calculate.error
    async def calculate_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="🛠️ ERROR", description="사용법이 잘못되었습니다.", color=0xff0000)
            embed.add_field(name="올바른 사용법", value="!계산기 [수식]", inline=False)
            embed.set_footer(text="Copyright (C) 2023 By Mushroomsando. All right reserved")
            await ctx.reply(embed=embed)

async def setup(bot):
    await bot.add_cog(Tool(bot))
