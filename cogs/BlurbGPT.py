import os
import requests
import discord
from discord.ext import commands
import interactions
import json

class BlurbGPT(commands.Bot):
    """Base Class for Chatting with Blurb the Discord Bot
    """
    def __init__(self, model_name):
        super().__init__(command_prefix='^', intents=discord.Intents.all())
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
        await self.bot.change_presence(activity=discord.Game("I'm back muhahahahah"))
    
    async def on_message(self, message):
        # ignore the message if it comes from the bot itself
        if message.author.id == self.user.id:
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
    
# async def setup(bot):
#     await bot.add_cog(BlurbGPT(bot))