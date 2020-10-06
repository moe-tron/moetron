import discord
from discord.ext import commands
from generator import Generate
from run_generator import Generator
import os
import csv
# Super simple discord bot that uses StyleGAN2 to create pics and send them.
# See generator.py for the commands 

bot = commands.Bot(command_prefix='moe')
global whitelist

# whilelist csv has guild ids separated by comma. If no file exists we ignore the whitelist feature.
def load_whitelist(whitelist_file):
    if os.path.isfile(whitelist_file):
        with open(whitelist_file,'r')as f:
            raw_data = f.read().strip("\n")
            return list(map(int, raw_data.split(",")))
    return []


async def verify_servers(guilds):
    global whitelist
    for guild in bot.guilds:
        if whitelist and guild.id not in whitelist:
            print("Leaving guild ID: %s, not whitelisted" % guild.id)
            await guild.leave()

@bot.event
async def on_guild_join(guild):
    global whitelist
    if whitelist and guild.id not in whitelist:
        print("Leaving guild ID: %s, not whitelisted" % guild.id)
        await guild.leave()

@bot.event
async def on_ready():
    print('Logged in as {}:{}'.format(bot.user.name, bot.user.id))
    print('------')
    print('Servers connected to:')
    for guild in bot.guilds:
        print(guild.name)
    await verify_servers(bot.guilds)
    status = discord.Game("Generating Anime!")
    await bot.change_presence(status=discord.Status.online, activity=status)

whitelist = load_whitelist('whitelist.csv')
print("Whitelisted ids: ", whitelist)
bot.add_cog(Generate(Generator()))
bot.run(os.environ.get('MOEKEY'))