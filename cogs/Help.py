from discord.ext import commands
import discord
import json

# 명령어 정보 로드
def load_command_info():
    with open("DB\\command.json", "r", encoding="utf-8") as file:
        command_info = json.load(file)
    return command_info
command_info = load_command_info()

# 명령어 정보 저장
def save_command_info(command_info):
    with open("DB\\command.json", "w", encoding="utf-8") as file:
        json.dump(command_info, file, ensure_ascii=False, indent=4)


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="도움말")
    async def help(self, ctx):
        embed = discord.Embed(title="📝 Command List", description="각 명령어의 기능 및 사용법이 궁금하다면 여기서 `!정보 [명령어]`를 입력해 주세요.", color=0x00aaff)
        for category, commands in command_info.items():
            category_description = commands.get("description", "")
            category_commands = "\n".join([f"!{command}" for command in commands if command != "description"])
            if category_commands:
                embed.add_field(name=f"**{category}** \n {category_description}", value=category_commands, inline=False)
        await ctx.author.send(embed=embed)
        await ctx.message.add_reaction("✅")

    @commands.command(name="정보")
    async def command_info(self, ctx, command):
        if isinstance(ctx.channel, discord.DMChannel):
            for category, commands in command_info.items():
                if command in commands:
                    command_data = commands[command]
                    embed = discord.Embed(title=f"🔍 Command Info - !{command}", description=command_data["description"], color=0x00aaff)
                    embed.add_field(name="사용법", value=command_data["usage"])
                    await ctx.reply(embed=embed)
                    return
            print("없따!")
        else:
            embed = discord.Embed(title="ℹ️ INFO", description="이 명령어는 DM에서만 사용할 수 있어요.", color=0xffdd00)
            embed.set_footer(text = "Copyright (C) 2023 By Mushroomsando. All right reserved.")
            await ctx.reply(embed=embed)

async def setup(bot):
    await bot.add_cog(Help(bot))