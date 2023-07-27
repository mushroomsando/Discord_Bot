'''#TODO
기상청 API에서 지금으로부터 최대 6시간 동안의 예보 받아오기
    보여줄 정보 = 날씨, 기온, 습도, 강수확률, 풍향
    API에서 정보를 받아오고 가공하는 것은 이미 구현 완료

    봇 응답 메시지
    embed로 출력하기 (이건 알아서 잘 내가 만들어 볼께)

지역 선택 가능하게 만들기
    서버가 어던 값을 설정했는지 Excel로 저장해서 다음부터 이 서버에서 저장한 값으로 일기예보 출력
    로직
        기상청에서 제공한 Excel 파일에서 정보를 가져옴
        유저는 다음과 같은 파라메터를 봇에게 전달해서 봇이 처리
            !지역설정 [시/도][군/구][읍/면/동]
            셋중에 최소 한개 이상 아무 값이나 입력받음
        봇은 Excel 파일에서 다음과 같이 처리
            Excel 파일 구조
                [시/도]는 Excel Cn -> [군/구] Dn -> [읍/면/동] En 순서

            Excel 파일에서 유저가 입력한 값을 필터링 해서 한 페이지에 5개씩 검색결과 embed로 출력
                예외처리) 만약 검색 결과가 없다면 "검색결과가 없습니다" 라고 출력
                출력방법
                    봇이 보낸 메시지에 ⏩(다음)⏪(이전) 이모지 추가
                        조건)가장 첫페이지라면 이전 이모지를 추가하지 않음
                        조건)가장 마지막 페이지라면 다음 이모지를 추가하지 않음
                    이벤트 처리
                        유저가 다음 이모지를 누르면 검색결과 페이지를 다음으로 넘김
                        이전 메시지를 누르면 검색결과 페이지를 이전으로 넘김
                검색결과 선택
                    유저는 !선택 [번호]로 선택할 수 있게 함
                    봇은 선택받은 값을 기상청에서 제공한 Excel 파일에서 F열값, G값을 Excel 파일로 저장
                        저장구조) A열 -> 서버ID, B열 -> [시/도], C열 -> [군/구], D열 -> [읍/면/동], E열 -> Nx값, F열 ->Ny값
            
            설정 결과를 Embed로 출력
            
        
            

    기본값 = 울산광역시 중구 태화동
기상청 API에서 기상특보 정보 받아오기
    이건 연구중...
'''
import discord
from discord.ext import commands
import sys
import traceback
import math
sys.path.append('C:/Users/windows/Desktop/repository/Programing/Discord_bot/Weather_Function')
import Weather_data as Wd
import Weather_data_process as Wp
from datetime import datetime

class Forecast(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="날씨")
    async def now_weather(self, ctx):
        try:
            today = datetime.today()
            today_date = today.strftime("%Y%m%d")
            now = datetime.now()
            weather_data = Wd.get_ultra_short_live_check_raw_data(open("Weather_Function\\api_code.txt", "r"), today_date, now, 102, 84)
            process_data = Wd.ultra_short_live_chek(weather_data)
            
            wind = process_data['VEC']
            wind = str(math.trunc((int(wind) + 22.5 * 0.5) / 22.5))

            loading_emoji = '⚙️'
            await ctx.message.add_reaction(loading_emoji)
            print(wind)

            success_reaction = '✅'
            await ctx.message.remove_reaction(loading_emoji, ctx.me)
            await ctx.message.add_reaction(success_reaction)

            embed = discord.Embed(title = f"{Wp.get_visual_data(weather_data, 1)}NOW WEATHER\n-------------\n🚩울산광역시 중구 태화동\n\t\t\t\t\t\t\t🌡️ {process_data['T1H']}℃\n\t\t\t\t\t\t👤체감{Wp.discomfort_index(float(process_data['T1H']), int(process_data['REH']), float(process_data['WSD'])):.1f}℃",color=0x00aaff)
            embed.add_field(name = "💧습도", value=process_data['REH'] + "%", inline=True)
            embed.add_field(name = "💨바람", value=Wp.get_visual_data(weather_data, 2)+ process_data['WSD']+ "m/s", inline=True) #기상청 홈피랑 달라요 왜지?
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
    
    @commands.command(name = "일기예보") #TODO
    async def forecast_weather(self, ctx):
        try:
            today = datetime.today()
            today_date = today.strftime("%Y%m%d")
            now = datetime.now()
            
            weather_data = Wd.get_short_term_forecast_inquiry_raw_data(open("Weather_Function\\api_code.txt", "r"), today_date, now, 102, 84)
            loading_emoji = '⚙️'
            await ctx.message.add_reaction(loading_emoji)
            print("OK")
            
            success_reaction = '✅'
            await ctx.message.add_reaction(success_reaction)
            await ctx.message.remove_reaction(loading_emoji, ctx.me)
            
            await ctx.reply(f"Success! raw data is : \n{Wd.short_term_forecast(weather_data)} \n{now}")
            print("COMPELETE")
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