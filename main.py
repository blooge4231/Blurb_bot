import discord
from discord.ext import commands
import os
import random
import requests
import json
import datetime

bot = commands.Bot(command_prefix='^')


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game("dont't worry about it"))
    print('JCS Bot is ready!')


#error control
#@bot.event
#async def on_command_error(ctx,error):
# if isinstance(error,commands.MissingRequiredArguments):
#  await ctx.send('`Sorry, missing function arguments :(`')


@bot.event
async def on_member_join(member):
    #welcome texts
    welcome_texts = [
        f"Welcome {member.name}!",
        f"OWO new member whose name is {member.name}",
        f"YOYOYOOYOO it's {member.name}!",
        f"Believe in yourself, {member.name}, and you'll enjoy your time here!",
        f"It's a new day, with a new {member.name}!",
        f"Oh shoot, it's {member.name}...",
        f"Help me with my math homework plz, {member.name}."
    ]

    await member.create_dm()
    await member.dm_channel.send(random.choice(welcome_texts))
    await bot.process_commands(member)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    ramen = message.content

    #chat replies
    if ramen.startswith('UWU') or ramen.startswith('uwu'):
        await message.channel.send('OWO')

    if ramen.startswith('OWO') or ramen.startswith('owo'):
        await message.channel.send('UWU')

    if ramen.startswith('LOL') or ramen.startswith('lol') or ramen.startswith(
            'LEL') or ramen.startswith('lel') or ramen.startswith(
                'LUL') or ramen.startswith('lul') or ramen.startswith(
                    'LUWL') or ramen.startswith('luwl') or ramen.startswith(
                        'LMAO') or ramen.startswith('lmao'):
        await message.channel.send('UMU')

    await bot.process_commands(message)


#commands
@bot.command(
    name='supremeleaders', help='Shows the admins of this discord server')
async def supremeleaders(ctx):
    await ctx.send('injestedllamabird1234 & AQCOD3')


#weather commands
base_url = "http://api.openweathermap.org/data/2.5/weather?"


@bot.command(
    help="<city> Shows what the weather's like somewhere in the world")
async def weather(ctx, *, city: str):
    city_name = city
    complete_url = base_url + "appid=" + os.getenv(
        'api_key') + "&q=" + city_name
    response = requests.get(complete_url)
    x = response.json()
    channel = ctx.message.channel
    if x["cod"] != "404":
        async with channel.typing():
            y = x["main"]
            current_temperature = y["temp"]
            current_temperature_celsiuis = str(
                round(current_temperature - 273.15))
            current_pressure = y["pressure"]
            current_humidity = y["humidity"]
            z = x["weather"]
            weather_description = z[0]["description"]
        weather_description = z[0]["description"]
        embed = discord.Embed(
            title=f"Weather in {city_name}",
            color=ctx.guild.me.top_role.color,
            timestamp=ctx.message.created_at,
        )
        embed.add_field(
            name="Description",
            value=f"**{weather_description}**",
            inline=False)
        embed.add_field(
            name="Temperature(C)",
            value=f"**{current_temperature_celsiuis}°C**",
            inline=False)
        embed.add_field(
            name="Humidity(%)", value=f"**{current_humidity}%**", inline=False)
        embed.add_field(
            name="Atmospheric Pressure(hPa)",
            value=f"**{current_pressure}hPa**",
            inline=False)
        embed.set_thumbnail(url="https://i.ibb.co/CMrsxdX/weather.png")
        embed.set_footer(text=f"Requested by {ctx.author.name}")
        await channel.send(embed=embed)
    else:
        await channel.send("City not found.")


@bot.command(
    help=
    "<search> Find something cute (it's from giphy so some stuff might not make sense)"
)
async def cute(ctx, *, search):
    #user gif log
    print('')
    print("'^cute " + search +
          f"' came from the server: {ctx.guild}  (user: {ctx.author})")
    embed = discord.Embed(
        title='From {}'.format(ctx.author),
        description='Envoked: `Looking for a cute {}`'.format(search),
        colour=discord.Colour.blue())
    datetime_now = datetime.datetime.now()
    time = datetime_now.strftime("%d/%m/%Y %H:%M:%S")

    search = search
    search.replace(' ', '+')

    response = requests.get('http://api.giphy.com/v1/gifs/random?api_key=' +
                            os.getenv('GIPHY_key') + '&tag=' + search +
                            '&rating=pg-13')
    data = json.loads(response.text)

    result_gif = data['data']['images']['original']['url']

    embed.set_image(url=result_gif)
    embed.set_footer(
        text="Sent by{} at {}. Gif pulled from Giphy".format(ctx.author, time))

    await ctx.send(embed=embed)


@bot.command(help="<search> Find something anime-related")
async def anime(ctx, search):
    print('')
    print("'^anime " + search +
          f"' came from the server: {ctx.guild}  (user: {ctx.author})")
    datetime_now = datetime.datetime.now()
    time = datetime_now.strftime("%d/%m/%Y %H:%M:%S")
    embed = discord.Embed(
        title='From {}'.format(ctx.author),
        description='Envoked: `OWO, Anime {}`'.format(search),
        colour=discord.Colour.magenta())
    search = "anime " + search
    search.replace(' ', '+')

    response = requests.get((
        "https://api.tenor.com/v1/random?q=%s&key=%s&limit=%s&media_filter=basic"
    ) % (search, os.getenv('tenor_key'), 1))

    if response.status_code == 200:
        try:
            data = response.json()['results']
            gif = data[0]
            gif = gif.get("media")
            gif = gif[0]
            gif = gif.get("gif")
            gif = gif.get("url")

            embed.set_image(url=gif)
            embed.set_footer(text="Sent by{} at {}. Gif pulled from Tenor".
                             format(ctx.author, time))
            await ctx.channel.send(embed=embed)
        except:
            await ctx.channel.send("{} No image found. Sorry :<").format(
                ctx.author)

bot.load_extension('cogs.CommandEvents')

bot.run(os.getenv('TOKEN'))
