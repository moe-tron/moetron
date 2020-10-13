from generator import Generate
import unittest
import asyncio
import shutil
import os

# pylint: disable=too-many-function-args

# Simple unit tests on generator cog, yes it's a mess I'm not used to unit testing in python
# Just tests the small amount of logic in the cog, basically just makes sure that for properly formatted args
# an error isn't thrown.

class MockCtx:

    def __init__(self):
        self.text = None
        self.file = None
    
    async def send(self, text = None, file = None):
        self.text = text
        self.file = file
        self.file.close()

class MockGenerator():

    def __init__(self, imagePath = "docs/gen_example.png"):
        self.imagePath = imagePath

    def generate_one_image(self, seed, truncation = 0.55):
        return self.imagePath
    
    def style_mix(self, seed1, seed2, truncation_psi = 0.55):
        return self.imagePath

def async_test(f):
    def wrapper(*args, **kwargs):
        coro = asyncio.coroutine(f)
        future = coro(*args, **kwargs)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(future)
    return wrapper

class TestGeneratorCog(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.imagePath = "docs/gen_example.png"
        self.genCog = Generate(MockGenerator(self.imagePath))
        
    def setUp(self):
        self.ctx = MockCtx()

    @async_test
    async def testgenShouldReturnImageForCorrectArgs(self):
        # not sure why, but I'm forced to pass the object itself into gen here. Idk why I have to do it
        await self.genCog.gen(self.genCog, self.ctx, 123)
        self.assertTrue(self.ctx.file.fp.name == self.imagePath)

    @async_test
    async def testTruncShouldRaseValueErrorWhenTruncationOutOfRange(self):
        with self.assertRaises(ValueError):
            await self.genCog.trunc(self.genCog, self.ctx, 123, 12)
    
    @async_test
    async def testTruncShouldReturnValidFileForCorrectArgs(self):
        await self.genCog.trunc(self.genCog, self.ctx, 123, 1)
        self.assertTrue(self.ctx.file.fp.name == self.imagePath)

    @async_test
    async def testRandShouldReturnValidFile(self):
        await self.genCog.rand(self.genCog, self.ctx)
        self.assertTrue(self.ctx.file.fp.name == self.imagePath)
    
    @async_test
    async def testMessShouldReturnValidFile(self):
        await self.genCog.mess(self.genCog, self.ctx)
        self.assertTrue(self.ctx.file.fp.name == self.imagePath)
    
    @async_test
    async def testNameShouldReturnValidFile(self):
        await self.genCog.name(self.genCog, self.ctx, input_string = "hello")
        self.assertTrue(self.ctx.file.fp.name == self.imagePath)

    @async_test
    async def testMixShouldThrowForMissingArg(self):
        with self.assertRaises(IndexError):
            await self.genCog.mix(self.genCog, self.ctx, args='123')
    
    @async_test
    async def testMixShouldReturnValidImg(self):
        await self.genCog.mix(self.genCog, self.ctx, args='123 1234')
        self.assertTrue(self.ctx.file.fp.name == self.imagePath)
    
    @async_test
    async def testMixShouldReturnValidImgForStringArgs(self):
        await self.genCog.mix(self.genCog, self.ctx, args="string1 | string2 asdf")
        self.assertTrue(self.ctx.file.fp.name == self.imagePath)
    
    @async_test
    async def testWhenDeleteIsEnabledImageShouldBeRemoved(self):
        shutil.copyfile("docs/gen_example.png", "results/image_to_be_deleted.png")
        self.imagePath = "results/image_to_be_deleted.png"
        self.genCog = Generate(MockGenerator(self.imagePath), True)
        await self.genCog.gen(self.genCog, self.ctx, 123)
        self.assertFalse(os.path.isfile(self.imagePath))

if __name__ == '__main__':
    unittest.main()