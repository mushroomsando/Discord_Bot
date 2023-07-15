'''#TODO
기상청 API에서 지금으로부터 최대 3시간 동안의 예보 받아오기
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
from discord import Embed, Color
from discord.ext import commands
import sys
sys.path.append('C:/Users/windows/Desktop/repository/Programing/Discord_bot/Wether_Function')
from Weather_data import get_weather_data

class Forecast(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="!일기예보")
    async def forecast(self, ctx):
        # '⚙️' 이모지로 반응
        loading_emoji = '⚙️'
        await ctx.message.add_reaction(loading_emoji)

        forecast_data = get_weather_data()

        # '⚙️' 이모지 삭제 및 '✅' 이모지로 교체
        await ctx.message.remove_reaction(loading_emoji, ctx.me)
        success_reaction = '✅'
        await ctx.message.add_reaction(success_reaction)

        # 예보 출력
        embed = Embed(title="Weather Forecast", color=Color.blue())
        for time, data in forecast_data.items():
            embed.add_field(name="Time", value=f"{time}00", inline=True)
            embed.add_field(name="Temperature", value=f"{data['TMP']}°C", inline=True)

            sky_code = int(data['SKY'])
            if sky_code == 1:
                sky_status = "맑음"
            elif sky_code == 3:
                sky_status = "구름 조금"
            elif sky_code == 4:
                sky_status = "흐림"
            else:
                sky_status = "알 수 없음"

            embed.add_field(name="Sky", value=sky_status, inline=True)
            embed.add_field(name="Rain Probability", value=f"{data['POP']}%", inline=True)
            embed.add_field(name="Humidity", value=f"{data['REH']}%", inline=True)
            embed.add_field(name="\u200b", value="\u200b", inline=False)  # 빈 필드 추가 (디자인 목적)

        await ctx.send(embed=embed)

print("PASS")
async def setup(bot):
    await bot.add_cog(Forecast(bot))