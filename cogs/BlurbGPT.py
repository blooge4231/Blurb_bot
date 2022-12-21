import os
import requests
import discord
from discord.ext import commands
import random
import json
class BlurbGPT(commands.Bot):
    """Base Class for Chatting with Blurb the Discord Bot
    """
    def __init__(self, model_name):
        super().__init__(intents=discord.Intents.all())
        API_URL = 'https://api-inference.huggingface.co/models/blooge4231/'
        self.api_endpoint = API_URL + model_name
        token = os.getenv('HUGGINGFACE_TOKEN')
        self.request_headers = {
            'Authorization': 'Bearer {}'.format(token)
        }
        
    def query(self, payload):
        data = json.dumps(payload)
        response = requests.request('POST',
                                    self.api_endpoint,
                                    headers=self.request_headers,
                                    data=data)
        ret = json.loads(response.content.decode('utf-8'))
        return ret
        
    async def on_ready(self):
        # print out information when the bot wakes up
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
        # send a request to the model without caring about the response
        # just so that the model wakes up and starts loading
        self.query({'inputs': {'text': 'Hello!'}})
        # adjust activity status of bot
        await self.change_presence(activity=discord.Game("Blurb~"))

    # randomize message on each member join
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        #welcome texts
        welcome_texts =[
            f"Welcome **{member.name}**!",
            f"OWO new member! Their name is **{member.name}!**",
            f"YOYOYOOYOO it's **{member.name}**!",
            f"Believe in yourself, **{member.name}**, and you'll enjoy your time here!",
            f"It's a new day, with a new **{member.name}**!",
            f"Oh shoot, it's **{member.name}**...",
            f"Help me with my math homework plz, **{member.name}**."
        ]
        if channel is not None:
            await channel.send(random.choice(welcome_texts))
        return
    
    async def uwu_handler(self, ctx):
        ramen = ctx.content
        #chat replies
        if ramen.startswith('UWU') or ramen.startswith('uwu'):
            await ctx.channel.send('OWO')
            return True

        if ramen.startswith('OWO') or ramen.startswith('owo'):
            await ctx.channel.send('UWU')
            return True

        if ramen.startswith('LOL') or ramen.startswith('lol') or ramen.startswith(
                'LEL') or ramen.startswith('lel') or ramen.startswith(
                    'LUL') or ramen.startswith('lul') or ramen.startswith(
                        'LUWL') or ramen.startswith('luwl') or ramen.startswith(
                            'LMAO') or ramen.startswith('lmao'):
            await ctx.channel.send('UMU')
            return True
        await self.process_commands(ctx)
        return False

    async def on_message(self, message):
        # ignore the message if it comes from the bot itself
        if message.author.id == self.user.id or message.author.bot:
            return
        if await self.uwu_handler(message):
            return
        if len(message.content) == 0:
            return
            
        # form query using message contents
        payload = {'inputs': {'text': message.content}}
        # mark bot with "typing" status while response is generated
        async with message.channel.typing():
          response = self.query(payload)
        bot_response = response.get('generated_text', None)
        
        # in case of error, sad blurb :<
        if not bot_response:
            if 'error' in response:
                bot_response = '`Error: {}`'.format(response['error'])
            else:
                bot_response = 'Something went wrong... Sad blurb :('

        # send the model's response to the Discord channel
        await message.channel.send(bot_response)
    