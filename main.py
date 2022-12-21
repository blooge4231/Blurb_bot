import os
import asyncio
import discord
import requests
from discord.ext import commands
from dotenv import load_dotenv
from cogs.BlurbGPT import BlurbGPT
# #from online import online
# # globals
load_dotenv()

bot = BlurbGPT('DialoGPT-medium-KEL')

# # cog list
# extensions = ['cogs.CommandEvents','cogs.MediaSearch','cogs.Weather']

# # load cogs
# async def load():
#     for ext in extensions:
#         await bot.load_extension(ext)
#         # print(f"{ext} has loaded")

async def main():
    #Print Meta-data to user
    @bot.command(name='supremeBlurber', help='Da creator of this bot')
    async def supremeleaders(ctx):
        await ctx.send('blooge4231 (Roy Huang)')
    @bot.event
    async def on_ready():
        print("Blurb bot is up and ready to go!")
    # load cogs and start bot
    # await load()
    await bot.start(os.getenv('DISCORD_TOKEN'))

asyncio.run(main())


