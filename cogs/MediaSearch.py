from discord.ext import commands
import json
import os
import requests
import discord
import datetime

class Media_Search(commands.Cog):
  def __init__(self, bot):
   self.bot = bot

  #search for miscellaneous gifs from giphy      
  @commands.command(help="<search> Find a cute gif! (results from giphy so it might not make sense lmao)")
  async def cute(self, ctx, *, search):
    #user gif log
    print('')
    print("'^cute " + search + f"' came from the server: {ctx.guild}  (user: {ctx.author})")
    embed = discord.Embed(title='From {}'.format(ctx.author), description='Envoked: `Looking for a cute {}`'.format(search), colour=discord.Colour.blue())
    datetime_now = datetime.datetime.now()
    time = datetime_now.strftime("%d/%m/%Y %H:%M:%S")

    
    search.replace(' ', '+')

    response = requests.get('http://api.giphy.com/v1/gifs/random?api_key=' + os.getenv('GIPHY_key') + '&tag=' + search + '&rating=pg-13')
    data = json.loads(response.text)

    result_gif = data['data']['images']['original']['url']

    embed.set_image(url=result_gif)
    embed.set_footer(text="Sent by{} at {}. Gif pulled from Giphy".format(ctx.author, time))

    await ctx.send(embed=embed)


#search for anime-related stuff from tenorgif
  @commands.command(help="<search> Find an anime-related gif!")
  async def anime(self, ctx, search):
    print('')
    print("'^anime " + search + f"' came from the server: {ctx.guild}  (user: {ctx.author})")
    datetime_now = datetime.datetime.now()
    time = datetime_now.strftime("%d/%m/%Y %H:%M:%S")
    embed = discord.Embed(title='From {}'.format(ctx.author),description='Envoked: `OWO, Anime {}`'.format(search),colour=discord.Colour.magenta())
    search = "anime " + search
    search.replace(' ', '+')
    response = requests.get(("https://api.tenor.com/v1/random?q=%s&key=%s&limit=%s&media_filter=basic") % (search, os.getenv('tenor_key'), 1))

    if response.status_code == 200:
      try:
        data = response.json()['results']
        gif = data[0]
        gif = gif.get("media")
        gif = gif[0]
        gif = gif.get("gif")
        gif = gif.get("url")

        embed.set_image(url=gif)
        embed.set_footer(text="Sent by{} at {}. Gif pulled from Tenor".format(ctx.author, time))
        await ctx.channel.send(embed=embed)

      except:
        await ctx.channel.send("{} No image found. Sorry :<").format(ctx.author)

def setup(bot):
  bot.add_cog(Media_Search(bot))