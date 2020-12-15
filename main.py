import discord
import os
import requests
import json

client = discord.Client()



@client.event
async def on_read():
  print('We have logged in as {0.user}'.format(compile))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('^UWU') or message.content.startswith('^uwu'):
    await message.channel.send('OWO')

  if message.content.startswith('^OWO') or message.content.startswith('^owo'):
    await message.channel.send('UWU')

  if message.cont.startswith('^supremeleaders'):
    await message.channel.send('injestedllambird1234 & AQCOD3')
  


client.run(os.getenv('TOKEN'))

