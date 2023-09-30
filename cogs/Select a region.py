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
        # 입력값 확인
        if len(args) < 1:
            await ctx.message.add_reaction("⚠️")
            raise commands.BadArgument

        loading_emoji = '⚙️'
        success_reaction = '✅'
        await ctx.message.add_reaction(loading_emoji)

        # 검색어 추출
        province, county, town = None, None, None
        for term in args:
            if term in df['1단계'].unique():
                province = term
            elif term in df['2단계'].unique():
                county = term
            elif term in df['3단계'].unique():
                town = term

        # 조건에 맞는 데이터 검색
        filtered_data = filter_data(df, province, county, town)

        # 페이지 나누기
        chunk_size = 10
        pages = [filtered_data[i:i + chunk_size] for i in range(0, len(filtered_data), chunk_size)]
        total_pages = len(pages)
        page_number = 0

        def create_embed(page_number):
            current_page_data = pages[page_number]
            message = f"검색결과 {len(filtered_data)}개" if len(filtered_data) <= 30 else "검색결과가 많아 보입니다. 좀 더 많은 정보를 입력해 보세요."
            embed = discord.Embed(title="🔍 Search Results", description=message, color=0x00aaff)
            number = page_number * chunk_size + 1
            for item in current_page_data:
                embed.add_field(name=f"No. {number}", value=f"{item['1단계']} {item['2단계']} {item['3단계']}", inline=False)
                number += 1
            embed.set_footer(text=f"Copyright (C) 2023 By Mushroomsando. All right reserved\t\t\t페이지 {page_number + 1}/{total_pages}")
            return embed

        await ctx.message.remove_reaction(loading_emoji, ctx.me)
        await ctx.message.add_reaction(success_reaction)

        if len(filtered_data) == 1:
            selected_item = filtered_data[0]
            selected_embed = discord.Embed(title="✅ COMPLETE", description="💡검색결과가 1개여서 자동으로 선택했어요.", color=0x00aaff)
            selected_embed.add_field(name="앞으로 이 지역의 현재날씨와 일기예보를 조회할께요.", 
                                     value=f"{selected_item['1단계']} {selected_item['2단계']} {selected_item['3단계']}", inline=False)
            selected_embed.set_footer(text="Copyright (C) 2023 By Mushroomsando. All right reserved")
            await ctx.send(embed=selected_embed)
            print(selected_item['격자 X'], selected_item['격자 Y'])
            print("OK")

            data_to_save = {
                '서버 ID' : str(ctx.guild.id),
                '1단계': [selected_item['1단계']],
                '2단계': [selected_item['2단계']],
                '3단계': [selected_item['3단계']],
                'Nx' : [selected_item['격자 X']],
                'Ny' : [selected_item['격자 Y']]
            }

            save = pd.DataFrame(data_to_save)
            # Excel 파일로 저장
            excel_filename = 'DB\\Server_Lattice Location_Save DB.xlsx'
            save.to_excel(excel_filename, index=False, engine='openpyxl')
            print(f"Settings saved to {excel_filename}")
        else:
            paginated_embed = create_embed(page_number)
            paginated_message = await ctx.send(embed=paginated_embed)

            arrow_emojis = ['⬅️', '➡️', '🔍', '✖️']
            for emoji in arrow_emojis:
                if total_pages > 1 or emoji != '➡️':
                    await paginated_message.add_reaction(emoji)

            while True:
                try:
                    reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=lambda r, u: u == ctx.author and r.message.id == paginated_message.id)

                    if str(reaction.emoji) == '⬅️' and page_number > 0:
                        page_number -= 1
                    elif str(reaction.emoji) == '➡️' and page_number < total_pages - 1:
                        page_number += 1
                    elif str(reaction.emoji) == '✖️':
                        embed = discord.Embed(title="✅ INFO", color=0x00aaff)
                        embed.add_field(name="취소됨", value="작업이 취소되었습니다.", inline=False)
                        embed.set_footer(text="Copyright (C) 2023 By Mushroomsando. All right reserved")
                        await ctx.reply(embed=embed)
                        break
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

                                data_to_save = {
                                    '서버 ID' : str(ctx.guild.id),
                                    '1단계': [selected_item['1단계']],
                                    '2단계': [selected_item['2단계']],
                                    '3단계': [selected_item['3단계']],
                                    'Nx' : [selected_item['격자 X']],
                                    'Ny' : [selected_item['격자 Y']]
                                }

                                save = pd.DataFrame(data_to_save)
                                # Excel 파일로 저장
                                excel_filename = 'DB\\Server_Lattice Location_Save DB.xlsx'
                                save.to_excel(excel_filename, index=False, engine='openpyxl')
                                print(f"Settings saved to {excel_filename}")
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

    
    @search_data.error #예외처리
    async def kickerror(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            embed = discord.Embed(title="⚙️ ERROR", description="잘못된 값을 전달받았습니다. 다시 시도해 주세요.", color=0xff0000)
            embed.add_field(name="올바른 사용법", value="!선택 [번호 (정수)]", inline=False)
            embed.set_footer(text="Copyright (C) 2023 By Mushroomsando. All right reserved")
            await ctx.reply(embed=embed)
        elif isinstance(error, commands.BadArgument):
            embed = discord.Embed(title="⚠️ ERROR", description="사용법이 잘못되었습니다.", color=0xff0000)
            embed.add_field(name="올바른 사용법", value="!지역검색 [시/도] [군/구] [읍/면/동] (중 최소 한개 이상의 정보)", inline=False)
            embed.set_footer(text="Copyright (C) 2023 By Mushroomsando. All right reserved")
            await ctx.reply(embed=embed)
            
async def setup(bot):
    await bot.add_cog(Region(bot))