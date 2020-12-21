from discord.ext import commands
import random
import discord

  
class CommandEvents(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_ready(self):
    await self.bot.change_presence(activity=discord.Game("dont't worry about it"))
    print('JCS Bot is ready!')
#error control
#@bot.event
#async def on_command_error(ctx,error):
# if isinstance(error,commands.MissingRequiredArguments):
#  await ctx.send('`Sorry, missing function arguments :(`')


  @commands.Cog.listener()
  async def on_member_join(self, member):
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
    await self.process_commands(member)


  @commands.Cog.listener()
  async def on_message(self, ctx):
    if ctx.author == self.bot.user:
        return

    ramen = ctx.content

    #chat replies
    if ramen.startswith('UWU') or ramen.startswith('uwu'):
        await ctx.channel.send('OWO')

    if ramen.startswith('OWO') or ramen.startswith('owo'):
        await ctx.channel.send('UWU')

    if ramen.startswith('LOL') or ramen.startswith('lol') or ramen.startswith(
            'LEL') or ramen.startswith('lel') or ramen.startswith(
                'LUL') or ramen.startswith('lul') or ramen.startswith(
                    'LUWL') or ramen.startswith('luwl') or ramen.startswith(
                        'LMAO') or ramen.startswith('lmao'):
        await ctx.channel.send('UMU')

    #await self.process_commands(ctx)


def setup(bot):
    bot.add_cog(CommandEvents(bot))
