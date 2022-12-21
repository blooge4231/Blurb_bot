import discord
from discord.ext import commands
import os
import requests
import datetime
# initialize weather search related slash commands
def init_weather_search(bot):
    # openWeather API slash command
    @bot.slash_command(name='weather', description='<city> Get the current weather somewhere!', guild_ids=[788518876278423572])
    async def weather(ctx, *, city):
        # extract coordinate data
        weather_key = os.getenv('WEATHER_KEY')
        city_name = city
        complete_url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={weather_key}'
        response = requests.get(complete_url)
        x = response.json()

        channel = ctx.channel
        
        # format embed to send to channel
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
                timestamp=datetime.datetime.now(),
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
            embed.set_thumbnail(url="https://i.imgur.com/4p0DDQ6.jpg")
            embed.set_footer(text=f"Requested by {ctx.author.name}")
            await ctx.respond(embed=embed)
        else:
            await ctx.respond("City not found.")