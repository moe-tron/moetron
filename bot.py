import discord
from discord.ext import commands
from generator import Generate

# Super simple discord bot that uses StyleGAN2 to create pics and send them.
# See generator.py for the commands 

bot = commands.Bot(command_prefix='moe')

@bot.event
async def on_ready():
    print('Logged in as {}:{}'.format(bot.user.name, bot.user.id))
    print('------')
    status = discord.Game("Generating Anime!")
    await bot.change_presence(status=discord.Status.online, activity=status)

bot.add_cog(Generate())
bot.run('key')
