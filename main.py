import discord
from discord.ext import commands
import os
import requests


bot = commands.Bot(command_prefix='^')


#simple text-invoked commands
@bot.command(
    name='supremeleaders', help='Shows the admins of this discord server')
async def supremeleaders(ctx):
    await ctx.send('injestedllamabird1234 & AQCOD3')



#cog list
extensions = ['cogs.CommandEvents','cogs.MediaSearch','cogs.MiscApps']

if __name__ == '__main__':
  for ext in extensions:
    bot.load_extension(ext)



bot.run(os.getenv('TOKEN'))
