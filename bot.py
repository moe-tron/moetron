import discord
from discord.ext import commands
from generator import Generate
from run_generator import Generator
import os

# Discord bot that uses StyleGAN2 to create pics and send them.
# See generator.py for the commands 

class Moetron(commands.Bot):

    def __init__(self, prefix, **options):
        super().__init__(prefix, **options)
        self.add_cog(Generate(Generator(), delete_images=False))
        self.whitelist = self.load_whitelist('whitelist.csv')
        print("Whitelisted ids: ", self.whitelist)


    # whilelist csv has guild ids separated by comma. If no file exists we ignore the whitelist feature.
    def load_whitelist(self, whitelist_file):
        if os.path.isfile(whitelist_file):
            with open(whitelist_file,'r')as f:
                raw_data = f.read().strip("\n")
                return list(map(int, raw_data.split(",")))
        return []


    async def verify_servers(self, guilds):
        for guild in self.guilds:
            if self.whitelist and guild.id not in self.whitelist:
                print("Leaving guild ID: %s, not whitelisted" % guild.id)
                await guild.leave()

    async def on_guild_join(self, guild):
        if self.whitelist and guild.id not in self.whitelist:
            print("Leaving guild ID: %s, not whitelisted" % guild.id)
            await guild.leave()

    async def on_ready(self):
        print('Logged in as {}:{}'.format(self.user.name, self.user.id))
        print('------')
        print('Servers connected to:')
        for guild in self.guilds:
            print(guild.name)
        await self.verify_servers(self.guilds)
        status = discord.Game("Generating Anime!")
        await self.change_presence(status=discord.Status.online, activity=status)



def runBot():
    moetron = Moetron(prefix='moe')
    moetron.run(os.environ.get('MOEKEY'))


if __name__ == '__main__':
    runBot()