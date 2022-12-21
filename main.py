import os
from discord.ext import commands
from dotenv import load_dotenv
from cogs.BlurbGPT import BlurbGPT
from cogs.MediaSearch import init_media_search
from cogs.Weather import init_weather_search

# instantiate bot and load all slash commands
def main():
    load_dotenv()
    bot = BlurbGPT('DialoGPT-medium-KEL')
    init_media_search(bot)
    init_weather_search(bot)
    bot.run(os.getenv('DISCORD_TOKEN'))

if __name__ == '__main__':
    main()
