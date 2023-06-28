import os
import discord
import logging
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('TOKEN')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    datefmt='%d-%m-%Y %H:%M:%S')

bot = commands.Bot(
    command_prefix='!ted',
    intents=discord.Intents.all(),
    description='ted incident tracker')

@bot.event
async def on_ready():
    logging.info(f'{bot.user} has connected to Discord!')
    await bot.change_presence(activity=discord.Game(name='/help'))

if __name__ == '__main__':
    if TOKEN is None:
        logging.error('TOKEN is not set')
        exit(1)

    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}')

    bot.run(TOKEN)