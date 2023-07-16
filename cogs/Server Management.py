from discord.ext import commands
import discord
import asyncio

class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="채팅청소")
    @commands.has_permissions(manage_messages=True)
    async def message_clear(self, ctx, amount: int):
        embed = discord.Embed(title="⚙️ COMPLETE", description=f"{amount}개의 메시지가 청소되었습니다.", color=0x00aaff)
        embed.set_footer(text="이 메시지는 3초 뒤에 자동으로 삭제됩니다...")
        await ctx.channel.purge(limit=amount + 1)  # amount + 1 만큼의 메시지 삭제

        cleanup_delay = 3  # 메시지 삭제까지의 딜레이 (단위: 초)
        cleanup_message = await ctx.send(embed=embed)

        await asyncio.sleep(cleanup_delay)  # 딜레이 시간 대기
        await cleanup_message.delete()  # 메시지 삭제

    @commands.command(name="킥")
    @commands.has_permissions(kick_members=True)
    async def user_kick(self, ctx, member: discord.Member):
        await member.kick()  # 멤버를 킥
        embed = discord.Embed(title="⚙️ COMPLETE", description=f"{member.mention}님이 서버에서 추방되었습니다.", color=0x00aaff)
        await ctx.reply(embed=embed)
    
    @commands.command(name="밴")
    @commands.has_permissions(ban_members=True)
    async def user_ban(self, ctx, member: discord.Member):
        await member.ban()  # 멤버를 밴
        embed = discord.Embed(title="⚙️ COMPLETE", description=f"{member.mention}님이 서버에서 밴 되었습니다.", color=0x00aaff)
        await ctx.reply(embed=embed)  # 밴 완료 메시지 전송
    
    @commands.command(name="언벤")
    @commands.has_permissions(ban_members=True)
    async def user_unban(self, ctx, member_id: int):
        banned_users = await ctx.guild.bans()
        for ban_entry in banned_users:
            user = ban_entry.user
            if user.id == member_id:
                await ctx.guild.unban(user)
                embed = discord.Embed(title="⚙️ COMPLETE", description=f"{member_id}님이 서버에서 언벤되었습니다.", color=0x00aaff)
                await ctx.reply(embed=embed)  # 언벤 완료 메시지 전송
                return
        embed = discord.Embed(title="⚙️ INFO", description=f"해당 유저는 서버에서 밴되어 있지 않습니다.", color=0xffdd00)
        await ctx.reply(embed=embed) # 밴되어 있지 않은 경우 메시지 전송

    @commands.command(name="서버정보")
    async def server_info(self, ctx):
        server = ctx.guild
        members = server.member_count
        channels = len(server.channels)
        roles = len(server.roles)
        embed = discord.Embed(title="서버 정보", color=discord.Color.blue())
        embed.add_field(name="멤버 수", value=members, inline=False)
        embed.add_field(name="채널 수", value=channels, inline=False)
        embed.add_field(name="역할 수", value=roles, inline=False)
        await ctx.reply(embed=embed)  # Embed 형식으로 서버 정보 전송
    
    #=========예외처리 부분=========

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(title="⚙️ ERROR", description="이 명령어를 사용하려면 서버 관리 권한이 필요합니다.", color=0xff0000)
            embed.set_footer(text="Copyright (C) 2023 By Mushroomsando. All right reserved")
            await ctx.reply(embed=embed)
        elif isinstance(error, discord.errors.Forbidden):
            embed = discord.Embed(title="⚙️ ERROR", description="봇이 서버를 관리할 수 있는 권한이 없습니다.", color=0xff0000)
            embed.set_footer(text="Copyright (C) 2023 By Mushroomsando. All right reserved")
            await ctx.reply(embed=embed)
 
    @message_clear.error #채팅청소 예외처리
    async def clearerror(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="⚙️ ERROR", description="사용법이 잘못되었습니다.", color=0xff0000)
            embed.add_field(name="올바른 사용법", value="!채팅청소 [청소할 메시지 갯수]", inline=False)
            embed.set_footer(text="Copyright (C) 2023 By Mushroomsando. All right reserved")
            await ctx.reply(embed=embed)
        elif isinstance(error, commands.BadArgument):
            embed = discord.Embed(title="⚙️ ERROR", description="유요하지 않은 데이터를 입력받았습니다.", color=0xff0000)
            embed.add_field(name="올바른 사용법", value="!채팅청소 [청소할 메시지 갯수]", inline=False)
            embed.set_footer(text="Copyright (C) 2023 By Mushroomsando. All right reserved")
            await ctx.reply(embed=embed)
        elif isinstance(error, discord.errors.NotFound):
            embed = discord.Embed(title="⚙️ ERROR", description="더이상 청소할 메시지가 없습니다.", color=0xff0000)
            embed.set_footer(text="Copyright (C) 2023 By Mushroomsando. All right reserved")
            await ctx.reply(embed=embed)
        else:
            embed = discord.Embed(title="⚙️ ERROR", description="음... 무언가 잘못되었습니다. \n 여러분의 잘못이 아니니 걱정 마세요.", color=0xff0000)
            embed.add_field(name="오류내용", value=str(error))
            embed.set_footer(text="Copyright (C) 2023 By Mushroomsando. All right reserved")
            await ctx.reply(embed=embed)
    
    @user_kick.error #유저 킥 예외처리
    async def kickerror(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="⚙️ ERROR", description="사용법이 잘못되었습니다.", color=0xff0000)
            embed.add_field(name="올바른 사용법", value="!킥 [유저멘션]", inline=False)
            embed.set_footer(text="Copyright (C) 2023 By Mushroomsando. All right reserved")
            await ctx.reply(embed=embed)
        else:
            embed = discord.Embed(title="⚙️ ERROR", description="음... 무언가 잘못되었습니다. \n 여러분의 잘못이 아니니 걱정 마세요.", color=0xff0000)
            embed.add_field(name="오류내용", value=str(error))
            embed.set_footer(text="Copyright (C) 2023 By Mushroomsando. All right reserved")
            await ctx.reply(embed=embed)
    
    @user_ban.error #유저 밴 예외처리
    async def banerror(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="⚙️ ERROR", description="사용법이 잘못되었습니다.", color=0xff0000)
            embed.add_field(name="올바른 사용법", value="!밴 [유저맨션]", inline=False)
            embed.set_footer(text="Copyright (C) 2023 By Mushroomsando. All right reserved")
            await ctx.reply(embed=embed)
        else:
            embed = discord.Embed(title="⚙️ ERROR", description="음... 무언가 잘못되었습니다. \n 여러분의 잘못이 아니니 걱정 마세요.", color=0xff0000)
            embed.add_field(name="오류내용", value=str(error))
            embed.set_footer(text="Copyright (C) 2023 By Mushroomsando. All right reserved")
            await ctx.reply(embed=embed)
    
    @user_unban.error #유저 언벤 예외처리
    async def unbanerror(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="⚙️ ERROR", description="사용법이 잘못되었습니다.", color=0xff0000)
            embed.add_field(name="올바른 사용법", value="!언벤 [유저 ID]", inline=False)
            embed.set_footer(text="Copyright (C) 2023 By Mushroomsando. All right reserved")
            await ctx.reply(embed=embed)
        else:
            embed = discord.Embed(title="⚙️ ERROR", description="음... 무언가 잘못되었습니다. \n 여러분의 잘못이 아니니 걱정 마세요.", color=0xff0000)
            embed.add_field(name="오류내용", value=str(error))
            embed.set_footer(text="Copyright (C) 2023 By Mushroomsando. All right reserved")
            await ctx.reply(embed=embed)
    
    @server_info.error #서버 정보 예외처리
    async def infoerror(self, ctx, error):
        if isinstance(error, discord.errors.NotFound):
            embed = discord.Embed(title="⚙️ ERROR", description="서버를 찾을 수 없습니다.", color=0xff0000)
            embed.set_footer(text="Copyright (C) 2023 By Mushroomsando. All right reserved")
            await ctx.reply(embed=embed)
        elif isinstance(error, discord.errors.HTTPException):
            embed = discord.Embed(title="⚙️ ERROR", description="네트워크 오류가 발생하여 서버 정보를 가져올 수 없습니다.", color=0xff0000)
            embed.set_footer(text="Copyright (C) 2023 By Mushroomsando. All right reserved")
            await ctx.reply(embed=embed)
        elif isinstance(error, discord.errors.DiscordException):
            embed = discord.Embed(title="⚙️ ERROR", description="디스코드 API에 문제가 발생하여 서버 정보를 가져올 수 없습니다.", color=0xff0000)
            embed.set_footer(text="Copyright (C) 2023 By Mushroomsando. All right reserved")
            await ctx.reply(embed=embed)
        else:
            embed = discord.Embed(title="⚙️ ERROR", description="음... 무언가 잘못되었습니다. \n 여러분의 잘못이 아니니 걱정 마세요.", color=0xff0000)
            embed.add_field(name="오류내용", value=str(error))
            embed.set_footer(text="Copyright (C) 2023 By Mushroomsando. All right reserved")
            await ctx.reply(embed=embed)

async def setup(bot):
    await bot.add_cog(Utilities(bot))