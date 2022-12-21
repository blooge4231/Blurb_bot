import json
import os
import requests
import discord
import datetime
# intialize slash commands, given bot object
def init_media_search(bot):

  @bot.slash_command(name='cute', description='<search> Find a cute gif online!', guild_ids=[788518876278423572])
  async def cute(ctx, *, search):
    #user gif log
    print('')
    print("'^cute " + search + f"' came from the server: {ctx.guild}  (user: {ctx.author})")
    embed = discord.Embed(title='From {}'.format(ctx.author), description='Envoked: `Looking for a cute {}`'.format(search), colour=discord.Colour.blue())
    datetime_now = datetime.datetime.now()
    time = datetime_now.strftime("%d/%m/%Y %H:%M:%S")
    
    search.replace(' ', '+')

    response = requests.get('http://api.giphy.com/v1/gifs/random?api_key=' + os.getenv('GIPHY_KEY') + '&tag=' + search + '&rating=pg-13')
    data = json.loads(response.text)

    result_gif = data['data']['images']['original']['url']

    embed.set_image(url=result_gif)
    embed.set_footer(text="Sent by{} at {}. Gif pulled from Giphy".format(ctx.author, time))

    await ctx.respond(embed=embed)

  @bot.slash_command(name='anime', description= '<search> Find an anime-related gif!', guild_ids=[788518876278423572])
  async def anime(ctx, search):
    print('')
    print("'^anime " + search + f"' came from the server: {ctx.guild}  (user: {ctx.author})")
    datetime_now = datetime.datetime.now()
    time = datetime_now.strftime("%d/%m/%Y %H:%M:%S")
    embed = discord.Embed(title='From {}'.format(ctx.author),description='Envoked: `OWO, Anime {}`'.format(search),colour=discord.Colour.magenta())
    search = "anime " + search
    search.replace(' ', '+')
    response = requests.get(("https://api.tenor.com/v1/random?q=%s&key=%s&limit=%s&media_filter=basic") % (search, os.getenv('TENOR_KEY'), 1))

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
        await ctx.respond(embed=embed)

      except:
        await ctx.respond("{} No image found. Sorry :<").format(ctx.author)
