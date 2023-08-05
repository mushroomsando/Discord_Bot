""""
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
"""
import sys
sys.path.append('C:/Users/windows/Desktop/repository/Programing/Discord_bot/Weather_Function')

from discord.ext import commands
import asyncio
import pandas as pd
from Location_data_util import *

# 엑셀 파일 경로를 지정
excel_file_path = 'DB\\기상청_격자위치.xlsx'

# 엑셀 파일을 읽어서 DataFrame으로 저장.
df = pd.read_excel(excel_file_path)

class Region(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="지역검색")
    async def search_data(self, ctx, *args):
        # 입력값 확인 및 변수 초기화
        province, county, town = None, None, None
        if len(args) < 1:
            await ctx.reply("최소 한개 이상의 정보를 입력해 주세요.")
            return

        # 검색어 추출
        for term in args:
            if term in df['1단계'].unique():
                province = term
            elif term in df['2단계'].unique():
                county = term
            elif term in df['3단계'].unique():
                town = term

        # 조건에 맞는 데이터 검색
        filtered_data = filter_data(df, province, county, town)

        # 검색 결과가 35개 이상인지 확인
        while len(filtered_data) >= 35:
            # 검색 결과가 35개 이상이면 추가 정보를 입력받음
            await ctx.send(f"검색 결과가 35개 이상입니다. 추가 정보를 입력해주세요.")

            # 추가 정보를 입력받아 검색을 다시 수행
            def check(message):
                return message.author == ctx.author and message.channel == ctx.channel

            try:
                msg = await self.bot.wait_for('message', check=check, timeout=30.0)
                extra_data = msg.content

                # 입력된 추가 정보에 따라 검색을 다시 수행
                if province is None and extra_data in df['1단계'].unique():
                    province = extra_data
                elif county is None and extra_data in df['2단계'].unique():
                    county = extra_data
                elif town is None and extra_data in df['3단계'].unique():
                    town = extra_data

                filtered_data = filter_data(df, province, county, town)
            except asyncio.TimeoutError:
                await ctx.send("시간 초과로 처리되었습니다. 검색을 종료합니다.")
                return

        # 검색 결과를 디스코드 채팅으로 전송
        response = format_search_result(filtered_data)
        await ctx.send(response)

async def setup(bot):
    await bot.add_cog(Region(bot))