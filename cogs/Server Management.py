from discord.ext import commands
import discord
import asyncio

class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="채팅청소", signature="!채팅청소 [청소갯수]")
    @commands.has_permissions(manage_messages=True)
    async def message_clear(self, ctx, amount: int):
        embed = discord.Embed(title="⚙️ COMPLETE", description=f"{amount}개의 메시지가 청소되었습니다.", color=0x00aaff)
        embed.set_footer(text="이 메시지는 3초 뒤에 자동으로 삭제됩니다...")
        await ctx.channel.purge(limit=amount + 1)  # amount + 1 만큼의 메시지 삭제

        cleanup_delay = 3  # 메시지 삭제까지의 딜레이 (단위: 초)
        cleanup_message = await ctx.send(embed=embed)

        await asyncio.sleep(cleanup_delay)  # 딜레이 시간 대기
        await cleanup_message.delete()  # 메시지 삭제

    @commands.command(name="킥", signature="!킥 [유저맨션]")
    @commands.has_permissions(kick_members=True)
    async def user_kick(self, ctx, member: discord.Member):
        await member.kick()  # 멤버를 킥
        embed = discord.Embed(title="⚙️ COMPLETE", description=f"{member.mention}님이 서버에서 추방되었습니다.", color=0x00aaff)
        await ctx.reply(embed=embed)

    @commands.command(name="밴", signature="!밴 [유저맨션]")
    @commands.has_permissions(ban_members=True)
    async def user_ban(self, ctx, member: discord.Member):
        await member.ban()  # 멤버를 밴
        embed = discord.Embed(title="⚙️ COMPLETE", description=f"{member.mention}님이 서버에서 밴 되었습니다.", color=0x00aaff)
        await ctx.reply(embed=embed)  # 밴 완료 메시지 전송

    @commands.command(name="언벤", signature="!언벤 [유저맨션]")
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
        embed = discord.Embed(title="⚙️ INFO", description=f"해당 유저는 서버에서 밴되어 있지 않아요.", color=0xffdd00)
        await ctx.reply(embed=embed) # 밴되어 있지 않은 경우 메시지 전송

    @commands.command(name="서버정보")
    async def server_info(self, ctx):
        server = ctx.guild
        members = server.member_count
        channels = len(server.channels)
        roles = len(server.roles)
        embed = discord.Embed(title="서버 정보", color=discord.Color.blue())
        embed.add_field(name="멤버 수", value=members)
        embed.add_field(name="채널 수", value=channels)
        embed.add_field(name="역할 수", value=roles)
        await ctx.reply(embed=embed)  # Embed 형식으로 서버 정보 전송
    
    @commands.Cog.listener() #예외처리
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(title="⚙️ ERROR", description="이 명령어를 사용하려면 서버 관리 권한이 필요합니다.", color=0xff0000)
            await ctx.reply(embed=embed)
        elif isinstance(error, commands.MissingRequiredArgument):
            command = ctx.command
            embed = discord.Embed(title="⚙️ ERROR", description="사용법이 잘못되었습니다.", color=0xff0000)
            embed.add_field(name="사용법", value=f"!{command.name} {command.signature}")
            await ctx.reply(embed=embed)
        else:
            embed = discord.Embed(title="⚙️ ERROR", description="음... 무언가 잘못되었습니다. \n 여러분의 잘못이 아니니 걱정 마세요.", color=0xff0000)
            embed.add_field(name="오류내용", value=str(error))
            await ctx.reply(embed=embed)

async def setup(bot):
    await bot.add_cog(Utilities(bot))