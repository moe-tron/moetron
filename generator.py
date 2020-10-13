import discord
from discord.ext import commands
import random
import hashlib
import os

"""
 * Generate cog
 * Has commands: gen, rand, name, mess, trunc, mix
"""
class Generate(commands.Cog):

    def __init__(self, generator, delete_images = False):
        self.generator = generator
        self.generator.generate_one_image(1)
        self.generator.style_mix(100, 200)
        self.delete_images = delete_images

    #----------------------------------------------------------------------------

    @commands.command(help="Generates an image from a given seed. Params: seed", aliases=["generate"])
    async def gen(self, ctx, seed:int):
        img_path = self.generator.generate_one_image(seed)
        await ctx.send('Here is your generated anime girl from seed %s :)' % seed, file=discord.File(img_path, 'moe.png'))
        await self.cleanup(img_path)

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
        await self.cleanup(img_path)

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
        trunc = round(random.uniform(0.5, 1),3)
        seed = random.randint(0, 4294967295,)
        img_path = self.generator.generate_one_image(seed, trunc)
        await ctx.send('Here is your randomly generated anime girl :) seed: %s truncation: %.3f' % (seed, trunc), file=discord.File(img_path, 'moe.png'))
        await self.cleanup(img_path)

    @rand.error
    async def rand_error(self, ctx, error):
        print(error, error.original)
        await ctx.send("Uh oh something bad happened and idk what it was")

    #----------------------------------------------------------------------------

    @commands.command(help="Generates an image from a random seed with truncation turned off. Params: None", aliases=["messy"])
    async def mess(self, ctx):
        seed = random.randint(0, 4294967295)
        img_path = self.generator.generate_one_image(seed, 1)
        await ctx.send('Here is your randomly generated anime girl seed: %s :)\nShe may look kind of messed up' % seed, file=discord.File(img_path, 'moe.png'))
        await self.cleanup(img_path)

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
        await self.cleanup(img_path)

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
        seed = self.convertToSeed(input_string)
        img_path = self.generator.generate_one_image(seed)
        await ctx.send('Here is your generated anime girl from name %s seed: %s' % (input_string, seed), file=discord.File(img_path, 'moe.png'))
        await self.cleanup(img_path)

    @name.error
    async def name_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("No name provided")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Enter a string for the name")
        else:
            print(error, error.original)
            await ctx.send("Uh oh something bad happened and idk what it was")

    #----------------------------------------------------------------------------

    @commands.command(help="Applies the style a of input A onto input B, split with | if they're more than 1 word use -t to set the truncation. -t must come after all inputs and separated by whitespace.\nExamples:\nmoemix moetron moe\nmoemix moetron is awesome! | I love moetron!\nmoemix 100 500\nmoemix moetron is awesome! | I love moetron! -t 0.9")
    async def mix(self, ctx, *, args):
        trunc = 0.55
        if " -t " in args:
            args, temp_trunc = args.split(" -t ")
            trunc = float(temp_trunc)
            if trunc < -1 or trunc > 1:
                raise ValueError
        split_args = args.split(" | ") if " | " in args else args.split()
        arg1, arg2 = split_args[0], split_args[1] # This will throw for 1 arg that's fine
        img_path = self.generator.style_mix(self.convertToSeed(arg1), self.convertToSeed(arg2), truncation_psi=trunc)
        await ctx.send('Here is your generated anime girl from %s and %s :)' % (arg1, arg2), file=discord.File(img_path, 'moe.png'))
        await self.cleanup(img_path)

    @mix.error
    async def mix_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Not enough inputs provided")
        elif isinstance(error.original, IndexError):
            await ctx.send("Not enough inputs provided")
        elif isinstance(error.original, ValueError):
            await ctx.send("Enter a number between 1 and -1 for trunc")
        else:
            print(error, error.original)
            await ctx.send("Uh oh something bad happened and idk what it was")

    #----------------------------------------------------------------------------

    ## Helper Methods
    def convertToSeed(self, arg:str):
        return int.from_bytes(hashlib.md5(arg.encode('utf-8')).digest(), byteorder='big', signed=False) % 1000000000 if not arg.isdigit() else int(arg)

    async def cleanup(self, image_path):
        if self.delete_images and os.path.isfile(image_path):
           os.remove(image_path)
