""""
지역 선택 가능하게 만들기
    서버가 어던 값을 설정했는지 Excel로 저장해서 다음부터 이 서버에서 저장한 값으로 일기예보 출력
    로직
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
import discord
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

        #한 페이지에 보여줄 정보 갯수 설정
        chunk_size = 10

        #페이지 나누기
        pages = [filtered_data[i:i + chunk_size] for i in range(0, len(filtered_data), chunk_size)]
        page_number = 0
        total_pages = len(pages)

        def create_embed(page_number):
                embed = discord.Embed(title="🔍 Search Results", description=f"검색결과 {len(filtered_data)}개", color=0x00aaff)
                number = 1
                for item in pages[page_number]:
                    embed.add_field(name = f"No. {number}", value = f"{item['1단계']} {item['2단계']} {item['3단계']}", inline=False)
                    number += 1
                embed.set_footer(text=f"페이지 {page_number + 1}/{total_pages}")
                return embed
        
        # 초기 페이지
        paginated_embed = create_embed(page_number)
        paginated_message = await ctx.send(embed=paginated_embed)

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

async def setup(bot):
    await bot.add_cog(Region(bot))