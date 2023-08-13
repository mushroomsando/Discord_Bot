""""
지역 선택 가능하게 만들기
    서버가 어던 값을 설정했는지 Excel로 저장해서 다음부터 이 서버에서 저장한 값으로 일기예보 출력
    로직
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

    @commands.command(name="지역검색") # 미친 개 거지 발상이 같이 짜놔서 코드가 정말 더럽네요
    async def search_data(self, ctx, *args):
        # 입력값 확인 및 변수 초기화
        province, county, town = None, None, None
        if len(args) < 1:
            embed = discord.Embed(title="⚠️ ERROR", description="사용법이 잘못되었습니다.", color=0xff0000)
            embed.add_field(name="올바른 사용법", value="!지역검색 [시/도] [군/구] [읍/면/동] (중 최소 한개 이상의 정보)", inline=False)
            embed.set_footer(text="Copyright (C) 2023 By Mushroomsando. All right reserved")
            await ctx.reply(embed=embed)

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
                if len(filtered_data) > 30:
                    message = f"검색결과 {len(filtered_data)}개 \n💡검색결과가 많아 보입니다. 좀 더 많은 정보를 입력해 보세요."
                else:
                    message = f"검색결과 {len(filtered_data)}개"
                
                current_page_data = pages[page_number]
                embed = discord.Embed(title="🔍 Search Results", description=message, color=0x00aaff)
                number = page_number * chunk_size + 1
                for item in pages[page_number]:
                    embed.add_field(name = f"No. {number}", value = f"{item['1단계']} {item['2단계']} {item['3단계']}", inline=False)
                    number += 1
                embed.set_footer(text=f"Copyright (C) 2023 By Mushroomsando. All right reserved\t\t\t페이지 {page_number + 1}/{total_pages}")
                return embed
        
        if len(filtered_data) == 1:  # 검색 결과가 한 개인 경우
            selected_item = filtered_data[0]
            selected_embed = discord.Embed(title="✅ COMPLETE", description="💡검색결과가 1개여서 자동으로 선택됬어요." ,color=0x00aaff)
            selected_embed.add_field(name="앞으로 이 지역의 현재날씨와 일기예보를 조회할께요.", 
                                     value=f"{selected_item['1단계']} {selected_item['2단계']} {selected_item['3단계']}", inline=False)
            selected_embed.set_footer(text="Copyright (C) 2023 By Mushroomsando. All right reserved")
            await ctx.send(embed=selected_embed)
            print(selected_item['격자 X'], selected_item['격자 Y'])
            print("OK")
            #TODO 설정결과 파일 저장

        else:
            # 초기 페이지
            paginated_embed = create_embed(page_number)
            paginated_message = await ctx.send(embed=paginated_embed)

            left_arrow = '⬅️'
            right_arrow = '➡️'
            search = '🔍'
            cancle = '✖️'
            # 이동용 이모지를 추가
            if total_pages > 1:
                await paginated_message.add_reaction(left_arrow)
                await paginated_message.add_reaction(right_arrow)
                await paginated_message.add_reaction(search)
                await paginated_message.add_reaction(cancle)
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
                    
                    elif str(reaction.emoji) == cancle:
                        embed = discord.Embed(title="✅ INFO", color=0x00aaff)
                        embed.add_field(name="취소됨", value="작업이 취소되었습니다.", inline=False)
                        embed.set_footer(text="Copyright (C) 2023 By Mushroomsando. All right reserved")
                        await ctx.reply(embed=embed)
                    
                    elif str(reaction.emoji) == '🔍':
                        await ctx.send("원하는 번호를 입력하세요: (예: !선택 3)")

                        def check(msg):
                            return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.startswith('!선택')

                        try:
                            selection_message = await self.bot.wait_for('message', timeout=30.0, check=check)
                            selected_number = int(selection_message.content.split()[1])  # 입력한 번호 추출

                            if 1 <= selected_number <= len(filtered_data):
                                selected_item = filtered_data[selected_number - 1]
                                selected_embed = discord.Embed(title="✅ COMPLETE", color=0x00aaff)
                                selected_embed.add_field(name="앞으로 이 지역의 현재날씨와 일기예보를 조회할께요.", 
                                                         value=f"{selected_item['1단계']} {selected_item['2단계']} {selected_item['3단계']}", inline=False)
                                selected_embed.set_footer(text="Copyright (C) 2023 By Mushroomsando. All right reserved")
                                await ctx.send(embed=selected_embed)
                                print(selected_item['격자 X'], selected_item['격자 Y'])
                                #TODO 설정결과 파일 저장
                            else:
                                embed = discord.Embed(title="⚠️ ERROR", color=0xff0000)
                                embed.add_field(name="유효하지 않은 번호", value="유효하지 않은 정보입니다. 다시 시도해 주세요.", inline=False)
                                embed.set_footer(text="Copyright (C) 2023 By Mushroomsando. All right reserved")
                                await ctx.reply(embed=embed)
                                    
                        except TimeoutError:
                            embed = discord.Embed(title="⏰ INFO", color=0xfffb00)
                            embed.add_field(name="시간초과", value="선택이 취소되었습니다.", inline=False)
                            embed.set_footer(text="Copyright (C) 2023 By Mushroomsando. All right reserved")
                            await ctx.reply(embed=embed)
                        break

                except TimeoutError:
                    break

async def setup(bot):
    await bot.add_cog(Region(bot))