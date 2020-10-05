import discord
from discord.ext import commands
import random
import hashlib

# Generator cog, has 4 commands
class Generate(commands.Cog):

    def __init__(self, generator):
        self.generator = generator
        self.generator.generate_one_image(1)

    #----------------------------------------------------------------------------

    @commands.command(help="Generates an image from a given seed. Params: seed", aliases=["generate"])
    async def gen(self, ctx, seed:int):
        img_path = self.generator.generate_one_image(seed)
        await ctx.send('Here is your generated anime girl from seed %s :)' % seed, file=discord.File(img_path, 'moe.png'))

    @gen.error
    async def gen_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("No seed provided")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Enter a number for the seed")
        elif isinstance(error.original, ValueError):
            await ctx.send("Enter a number between 0 and 2^32 -1")
        else:
            print(error, error.original)
            await ctx.send("Uh oh something bad happened and idk what it was")

    #----------------------------------------------------------------------------

    @commands.command(help="Generates the opposite image from a given seed. Params: seed", aliases=["opp"])
    async def opposite(self, ctx, seed:int):
        img_path = self.generator.generate_one_image(seed, -0.55)
        await ctx.send('Here is your generated anime girl opposite of seed %s :)' % seed, file=discord.File(img_path, 'moe.png'))

    @opposite.error
    async def opposite_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("No seed provided")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Enter a number for the seed")
        elif isinstance(error.original, ValueError):
            await ctx.send("Enter a number between 0 and 2^32 -1")
        else:
            print(error, error.original)
            await ctx.send("Uh oh something bad happened and idk what it was")

    #----------------------------------------------------------------------------

    @commands.command(help="Generates an image from a random seed. Params: None", aliases=["random"])
    async def rand(self, ctx):
        seed = random.randint(0, 4294967295)
        img_path = self.generator.generate_one_image(seed)
        await ctx.send('Here is your randomly generated anime girl :) seed: %.4d' % seed, file=discord.File(img_path, 'moe.png'))

    @rand.error
    async def rand_error(self, ctx, error):
        print(error, error.original)
        await ctx.send("Uh oh something bad happened and idk what it was")

    #----------------------------------------------------------------------------

    @commands.command(help="Generates an image from a random seed with truncation turned off. Params: None", aliases=["messy"])
    async def mess(self, ctx):
        seed = random.randint(0, 4294967295)
        img_path = self.generator.generate_one_image(seed, 1)
        await ctx.send('Here is your randomly generated anime girl seed: %.4d :)\nShe may look kind of messed up' % seed, file=discord.File(img_path, 'moe.png'))

    @mess.error
    async def mess_error(self, ctx, error):
        print(error, error.original)
        await ctx.send("Uh oh something bad happened and idk what it was")
    
    #----------------------------------------------------------------------------

    @commands.command(help="Generates an image from a given seed with truncation value. Params: seed, truncation", aliases=["truncation"])
    async def trunc(self, ctx, seed:int, truncation:float):
        if truncation < -1.0 or truncation > 1.0:
            raise ValueError
        img_path = self.generator.generate_one_image(seed, truncation)
        await ctx.send('Here is your generated anime girl with seed %s and truncation %s :)' % (seed, truncation), file=discord.File(img_path, 'moe.png'))

    @trunc.error
    async def trunc_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("No seed or truncation value provided")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Enter a number for the seed and truncation")
        elif isinstance(error.original, ValueError):
            await ctx.send("Enter a number between 0 and 2^32 -1 for the seed and -1 -> 1 for truncation value")
        else:
            print(error, error.original)
            await ctx.send("Uh oh something bad happened and idk what it was")

    #----------------------------------------------------------------------------

    @commands.command(help="Generates an image from a seed based on a string. Params: string(s)")
    async def name(self, ctx, *, input_string):
        seed = int.from_bytes(hashlib.md5(input_string.encode('utf-8')).digest(), byteorder='big', signed=False) % 1000000000
        img_path = self.generator.generate_one_image(seed)
        await ctx.send('Here is your generated anime girl from name %s and seed %.4d' % (input_string, seed), file=discord.File(img_path, 'moe.png'))

    @name.error
    async def name_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("No name provided")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Enter a string for the name")
        else:
            print(error, error.original)
            await ctx.send("Uh oh something bad happened and idk what it was")