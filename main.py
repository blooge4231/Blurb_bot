import discord
from discord.ext import commands
import os
import requests


bot = commands.Bot(command_prefix='^')

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game("dont't worry about it"))
    print('JCS Bot is ready!')


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



#cog list
extensions = ['cogs.CommandEvents','cogs.MediaSearch']

if __name__ == '__main__':
  for ext in extensions:
    bot.load_extension(ext)



bot.run(os.getenv('TOKEN'))
