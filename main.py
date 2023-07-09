import discord
from colorama import init, Fore, Style
from discord.ext import commands
import os
import tracemalloc
import time

init() # Color initialization
now = time.strftime("\033[90m"+"%Y-%m-%d %H:%M:%S"+"\033[0m", time.localtime()) # Set Current time

#TODO Replace color output code with colora module
# Create Discord Client
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
tracemalloc.start()

# token file load
def load_token():
    with open('token.txt', 'r') as file:
        return file.read().strip()

#Cogs load
async def load_cogs():
    for filename in os.listdir('cogs'):
        if filename.endswith('.py'):
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                print(now + "\033[32m" + " PASS     "+ "\033[0m"+"\033[35m"+"Cogs load process"+"\033[0m"+f" cogs.{filename[:-3]} Load successful.")
            except Exception as e:
                print(now + "\033[31m" + " ERROR    "+"\033[0m"+"\033[35m"+"Cogs load process"+"\033[0m"+f" cogs.{filename[:-3]} Load Faile")
                print(f'Error: {type(e).__name__} - {e}')

#Login
@bot.event
async def on_ready():
    await load_cogs()
    print("=====================")
    print(now + "\033[36m" + " INFO     "+ "\033[0m"+"\033[35m"+"Login process"+"\033[0m"+f' LOGIN  : {bot.user.name}')
    print(now + "\033[36m" + " INFO     "+ "\033[0m"+"\033[35m"+"Login process"+"\033[0m"+f" BOT ID : {bot.user.id}")
    print("=====================")

# Bot run
bot.run(load_token())