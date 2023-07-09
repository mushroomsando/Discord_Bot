import discord
from colorama import init, Fore, Style
from discord.ext import commands
import os
import time

init() # Color initialization
now = time.strftime(f"{Fore.LIGHTBLACK_EX}%Y-%m-%d %H:%M:%S{Style.RESET_ALL}", time.localtime()) # Set Current time

# Create Discord Client
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

# token file load
def load_token():
    with open('token.txt', 'r') as file:
        return file.read().strip()

# Cogs load
async def load_cogs():
    for filename in os.listdir('cogs'):
        if filename.endswith('.py'):
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                print(f"{now}{Fore.GREEN} PASS     {Fore.MAGENTA}Cogs load process{Style.RESET_ALL} cogs.{filename[:-3]} Load successful.")
            except Exception as e:
                print(f"{now}{Fore.RED} ERROR    {Fore.MAGENTA}Cogs load process{Style.RESET_ALL} cogs.{filename[:-3]} Load Failed.")
                print(f'Error: {type(e).__name__} - {e}')

# Login
@bot.event
async def on_ready():
    await load_cogs()
    print("=====================")
    color_code = '3b8eea'
    print(f'\033[38;2;{int(color_code[:2], 16)};{int(color_code[2:4], 16)};{int(color_code[4:], 16)}m' +
        f"{now}{Fore.CYAN} INFO     \033[38;2;{int(color_code[:2], 16)};{int(color_code[2:4], 16)};{int(color_code[4:], 16)}m" +
        f"{Fore.MAGENTA}Login process{Style.RESET_ALL} LOGIN  : {bot.user.name}")

    print(f'\033[38;2;{int(color_code[:2], 16)};{int(color_code[2:4], 16)};{int(color_code[4:], 16)}m' +
        f"{now}{Fore.CYAN} INFO     \033[38;2;{int(color_code[:2], 16)};{int(color_code[2:4], 16)};{int(color_code[4:], 16)}m" +
        f"{Fore.MAGENTA}Login process{Style.RESET_ALL} BOT ID : {bot.user.id}")
    print("=====================")

# Bot run
bot.run(load_token())