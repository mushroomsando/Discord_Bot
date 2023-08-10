import sys
sys.path.append('C:/Users/windows/Desktop/repository/Programing/Discord_bot/Weather_Function')

import discord
from discord.ext import commands

import traceback
import math
from datetime import datetime
import Weather_data as Wd
import Weather_data_supplementary_information as Wi
import asyncio

class Forecast(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.pages = []
    
    @commands.command(name="날씨")
    async def now_weather(self, ctx):
        try:
            today = datetime.today()
            today_date = today.strftime("%Y%m%d")
            now = datetime.now()
            weather_data = Wd.get_ultra_short_live_check_raw_data(open("Weather_Function\\api_code.txt", "r"), today_date, now, 102, 84)
            process_data = Wd.ultra_short_live_chek(weather_data)

            loading_emoji = '⚙️'
            await ctx.message.add_reaction(loading_emoji)

            success_reaction = '✅'
            await ctx.message.remove_reaction(loading_emoji, ctx.me)
            await ctx.message.add_reaction(success_reaction)

            embed = discord.Embed(title = f"{Wi.get_visual_data(weather_data, 1)}NOW WEATHER\n-------------\n🚩울산광역시 중구 태화동\n\t\t\t\t\t\t\t🌡️ {process_data['T1H']}℃\n\t\t\t\t\t\t👤체감{Wi.discomfort_index(float(process_data['T1H']), int(process_data['REH']), float(process_data['WSD'])):.1f}℃",description="상세정보",color=0x00aaff)
            embed.add_field(name = "💧습도", value=process_data['REH'] + "%", inline=True)
            embed.add_field(name = "💨바람", value=f"{Wi.get_visual_data(weather_data, 2)} {process_data['WSD']}m/s", inline=True) #기상청 홈피랑 달라요 왜지?
            embed.add_field(name = "☔1시간 강수량", value=process_data['RN1'] + "mm", inline=True)
            embed.set_footer(text=f"최종 업데이트: {now.month}.{now.day} {now.hour}:{now.minute}\t\t\tProvision 대한민국 기상청")
            await ctx.reply(embed=embed)

        except Exception as e:
            error_emoji = '⚠️'
            await ctx.message.add_reaction(error_emoji)
            error_msg = "오류가 발생했습니다:\n```\n"
            error_msg += f"{e}\n"
            error_msg += "".join(traceback.format_exception(type(e), e, e.__traceback__))
            error_msg += "```"
            await ctx.send(error_msg)
    
    @commands.command(name="일기예보")
    async def forecast_weather(self, ctx, debug_able=0):
        try:
            today = datetime.today()
            today_date = today.strftime("%Y%m%d")
            now = datetime.now()
            weather_data = Wd.get_short_term_forecast_inquiry_raw_data(open("Weather_Function\\api_code.txt", "r"), today_date, now, 102, 84)
            process_data = Wd.short_term_forecast(weather_data)

            # process_data를 페이지별로 3개씩 끊기
            chunk_size = 3
            pages = [process_data[i:i + chunk_size] for i in range(0, len(process_data), chunk_size)]

            page_number = 0
            total_pages = len(pages)

            # 페이지별 embed를 생성하는 함수를 정의
            def create_embed(page_number):
                embed = discord.Embed(title="📺 WEATHER FORECAST\n\n🚩울산광역시 중구 태화동", 
                                      description="6시간 동안의 일기예보 입니다.", color=0x00aaff)
                for item in pages[page_number]:
                    embed.add_field(
                        name=f"{item['sky_emoji']} {item['date'][:4]}년 {item['date'][4:6]}월 {item['date'][6:]}일 {item['time']}:00",
                        value=f"🌡 기온: {item['temperature']}°C\n"
                              f"💧 습도: {item['humidity']}%\n"
                              f"🌬 바람: {item['wind_dir_emoji']} {item['wind_speed']}m/s\n"
                              f"🌧 강수 확률: {item['precipitation_probability']}%\n"
                              f"☔️ 강우량: {item['one_hour_precipitation']}")

                embed.set_footer(text=f"페이지 {page_number + 1}/{total_pages}\t\t\t\t최종 업데이트: {now.month}.{now.day} {now.hour}:{now.minute}\t\t\t\tProvision 대한민국 기상청")
                return embed

            loading_emoji = '⚙️'
            await ctx.message.add_reaction(loading_emoji)

            # 초기 페이지
            paginated_embed = create_embed(page_number)
            paginated_message = await ctx.send(embed=paginated_embed)

            success_reaction = '✅'
            await ctx.message.remove_reaction(loading_emoji, ctx.me)
            await ctx.message.add_reaction(success_reaction)

            left_arrow = '⬅️'
            right_arrow = '➡️'
            # 이동용 이모지를 추가
            if total_pages > 1:
                await paginated_message.add_reaction(left_arrow)
                await paginated_message.add_reaction(right_arrow)

            print("OK")

            while True:
                try:
                    reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=lambda r, u: u == ctx.author and r.message.id == paginated_message.id)

                    if str(reaction.emoji) == left_arrow and page_number > 0:
                        page_number -= 1
                        paginated_embed = create_embed(page_number)
                        await paginated_message.edit(embed=paginated_embed)
                        await paginated_message.remove_reaction(reaction, user)

                    elif str(reaction.emoji) == right_arrow and page_number < total_pages - 1:
                        page_number += 1
                        paginated_embed = create_embed(page_number)
                        await paginated_message.edit(embed=paginated_embed)
                        await paginated_message.remove_reaction(reaction, user)

                except TimeoutError:
                    break

        except Exception as e:
            error_emoji = '⚠️'
            await ctx.message.add_reaction(error_emoji)
            error_msg = "오류가 발생했습니다:\n```\n"
            error_msg += f"{e}\n"
            error_msg += "".join(traceback.format_exception(type(e), e, e.__traceback__))
            error_msg += "```"
            await ctx.send(error_msg)
    

async def setup(bot):
    await bot.add_cog(Forecast(bot))