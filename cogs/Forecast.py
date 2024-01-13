import sys
sys.path.append('C:/Users/windows/Desktop/repository/Programing/Discord_bot/Weather_API')

import discord
from discord.ext import commands
import Weather_data as Wd
import Location_data_util as location
import pandas as pd

class Forecast(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.pages = []
    
    @commands.command(name="날씨")
    async def now_weather(self, ctx, debug_able=0):
        excel_file_path = 'DB\\Sever_save.xlsx'
        df = pd.read_excel(excel_file_path)

        target_server_id = ctx.guild.id
        result = location.server_filter_data(df,target_server_id)
        if result is None:
            await ctx.reply(discord.Embed(title="⚠️ WARNING", 
                                          description="이 서버에서 일기예보를 조회할 지역이 설정되지 않았습니다. \n `!지역검색` 명령어를 이용하여 지역을 선택해 주세요.",
                                          color=0xffdd00))
            return
        
        #TODO : 단기예보 기반 일기예보 정보 받아오기

        await ctx.reply("현재 작업중...")

    
    @commands.command(name="일기예보")
    async def forecast_weather(self, ctx, debug_able=0):
        excel_file_path = 'DB\\Sever_save.xlsx'
        df = pd.read_excel(excel_file_path)

        target_server_id = ctx.guild.id
        result = location.server_filter_data(df,target_server_id)
        if result is None:
            await ctx.reply(discord.Embed(title="⚠️ WARNING", 
                                          description="이 서버에서 일기예보를 조회할 지역이 설정되지 않았습니다. \n `!지역검색` 명령어를 이용하여 지역을 선택해 주세요.",
                                          color=0xffdd00))
            return
        
        await ctx.reply("현재 작업중...")

        # TODO : API 구조 변경에 따른 코드 재작성

        # weather_data = Wd.get_short_term_forecast_inquiry_raw_data(open("Weather_Function\\api_code.txt", "r"), today_date, now, result['Nx'], result['Ny'])
        # process_data = Wd.short_term_forecast(weather_data)

        # process_data를 페이지별로 3개씩 끊기
        # chunk_size = 3
        # pages = [process_data[i:i + chunk_size] for i in range(0, len(process_data), chunk_size)]

        # page_number = 0
        # total_pages = len(pages)

        # # 페이지별 embed를 생성하는 함수를 정의
        # def create_embed(page_number):
        #     embed = discord.Embed(title=f"📺 WEATHER FORECAST\n\n🚩{result['1단계']} {result['2단계']} {result['3단계']}", 
        #                               description="6시간 동안의 일기예보 입니다.", color=0x00aaff)
        #     for item in pages[page_number]:
        #         embed.add_field(
        #             name=f"{item['sky_emoji']} {item['date'][:4]}년 {item['date'][4:6]}월 {item['date'][6:]}일 {item['time']}:00",
        #             value=f"🌡 기온: {item['temperature']}°C\n"
        #                     f"💧 습도: {item['humidity']}%\n"
        #                     f"🌬 바람: {item['wind_dir_emoji']} {item['wind_speed']}m/s\n"
        #                     f"🌧 강수 확률: {item['precipitation_probability']}%\n"
        #                     f"☔️ 강우량: {item['one_hour_precipitation']}")

        #     embed.set_footer(text=f"페이지 {page_number + 1}/{total_pages}\t\t\t\t최종 업데이트: {now.month}.{now.day} {now.hour}:{now.minute}\t\t\t\tPower by 기상청")
        #     return embed

        # loading_emoji = '⚙️'
        # await ctx.message.add_reaction(loading_emoji)

        # # 초기 페이지
        # paginated_embed = create_embed(page_number)
        # paginated_message = await ctx.send(embed=paginated_embed)

        # success_reaction = '✅'
        # await ctx.message.remove_reaction(loading_emoji, ctx.me)
        # await ctx.message.add_reaction(success_reaction)

        # left_arrow = '⬅️'
        # right_arrow = '➡️'
        # # 이동용 이모지를 추가
        # if total_pages > 1:
        #     await paginated_message.add_reaction(left_arrow)
        #     await paginated_message.add_reaction(right_arrow)

        # print("OK")

        # while True:
        #     try:
        #         reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=lambda r, u: u == ctx.author and r.message.id == paginated_message.id)

        #         if str(reaction.emoji) == left_arrow and page_number > 0:
        #             page_number -= 1
        #             paginated_embed = create_embed(page_number)
        #             await paginated_message.edit(embed=paginated_embed)
        #             await paginated_message.remove_reaction(reaction, user)

        #         elif str(reaction.emoji) == right_arrow and page_number < total_pages - 1:
        #             page_number += 1
        #             paginated_embed = create_embed(page_number)
        #             await paginated_message.edit(embed=paginated_embed)
        #             await paginated_message.remove_reaction(reaction, user)

        #     except TimeoutError:
        #         break

async def setup(bot):
    await bot.add_cog(Forecast(bot))