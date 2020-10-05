from generator import Generate
import unittest
import asyncio

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
    def testgenShouldReturnImageForCorrectArgs(self):
        # not sure why, but I'm forced to pass the object itself into gen here. Idk why I have to do it
        yield from self.genCog.gen(self.genCog, self.ctx, 123)
        self.assertTrue(self.ctx.file.fp.name == self.imagePath)

    @async_test
    def testTruncShouldRaseValueErrorWhenTruncationOutOfRange(self):
        try: # doing this because im too lazy to get assertraises w/ async
            yield from self.genCog.trunc(self.genCog, self.ctx, 123, 12)
        except:
            pass
        self.assertTrue(self.ctx.file == None)

    
    @async_test
    def testTruncShouldReturnValidFileForCorrectArgs(self):
        yield from self.genCog.trunc(self.genCog, self.ctx, 123, 1)
        self.assertTrue(self.ctx.file.fp.name == self.imagePath)

    @async_test
    def testRandShouldReturnValidFile(self):
        yield from self.genCog.rand(self.genCog, self.ctx)
        self.assertTrue(self.ctx.file.fp.name == self.imagePath)
    
    @async_test
    def testMessShouldReturnValidFile(self):
        yield from self.genCog.mess(self.genCog, self.ctx)
        self.assertTrue(self.ctx.file.fp.name == self.imagePath)
    
    @async_test
    def testNameShouldReturnValidFile(self):
        yield from self.genCog.name(self.genCog, self.ctx, input_string = "hello")
        self.assertTrue(self.ctx.file.fp.name == self.imagePath)

if __name__ == '__main__':
    unittest.main()