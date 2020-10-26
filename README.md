## Discord Bot using StyleGAN2 to generate anime face images.

This is just a simple discord bot that interfaces with the StyleGAN2 generator to create images.

## Commands:

**gen / generate** 
Generates an image from a given seed.

![Generate example](docs/gen_example.png)


**rand / random** 
Generates an image from a random seed.

![Random example](docs/rand_example.png)


**trunc / truncate** 
Generates an image from the given seed with the provided truncation-psi.

![Truncation example](docs/trunc_example.png)


**mess / messy** 
Generates an image from a random seed w/ truncation turned off.

![Random example](docs/mess_example.png)


**opp / opposite**
Generates an image from a given seed w/ truncation-psi flipped.

![Random example](docs/opp_example.png)


**name** 
Generates an image based on the hash of a string.

![Generate example](docs/name_example.png)

**mix** 
Mixes the style of either 2 seeds or 2 strings. For multi word args split them using " | "

Examples:

moemix Moetron is awesome! | We love moetron!

moemix 123 500

moemix me you

moemix Moetron is awesome! | We love moetron! -t 0.9

![Mix example](docs/mix_example.png)

## Setup:

To get this working follow the steps on the official StyleGAN2 repo:
https://github.com/NVlabs/stylegan2

It's kind of a pain to set up everything... Honestly I'd just try to get StyleGAN2 running first on your machine, then you'll know that this will work. After you get it working, you should just need discord py and to set up your bot w/ discord to get your key.

Off the top of my head the requirements for windows are:
* Python 3.7 (3.8 or newer won't work)
* CUDA 10.0
* cuDNN 7.5 or newer
* Visual Studio 2017 w/ MSVC

You can install python reqs using `pip install -r requirements.txt`

You can test CUDA by running test_nvcc.cu

Currently the bot's key is set to be read from an env var. You can just hardcode it though if you want.

After everything is setup run the bot using `python bot.py` It'll take a few seconds to start up because it starts up tensorflow and generates a couple images before the bot starts.

For linting, I use the following settings:

"python.linting.pylintArgs": [
    "--extension-pkg-whitelist=numpy",
    "--errors-only"
]

The model I used can be obtained from:
https://www.gwern.net/Faces#stylegan-2
you can use whatever model you want, but this bot was built around using this one. Hence the "moe" naming and such.

All credits for the trained model goes to the original creator Aaron Gokaslan.

This bot is not used for commercial purposes, and derivatives of this work should not be used for commercial purposes. See the license for more information.

See the license under docs, it's the same as the stylegan2 license.
https://nvlabs.github.io/stylegan2/license.html

**Alternatively**
You can use the provided dockerfile if you have either a linux host or dev channel windows build w/ wsl2 set up. Idk if it works I haven't tested it because windows refuses to let me use the dev insider build for some reason.

## Options: 

**Image Deletion:**
You can choose to have images be deleted after creation. By default this is disabled and images are kept in the results directory. To enable image deletion you can just pass in True as the second arg for cog.

**Whitelisting Feature:**
This bot uses a whitelisting feature to automatically leave guilds that aren't whitelisted. If you don't want this feature enabled you can just not create a whitelist.csv file, it won't remove servers if the file does not exist. Otherwise create a file whitelist.csv with the guild ids separated by ,

**Model / Network changing:**
To change the model that the bot uses simply pass in the path to the network when creating the Generator.

## Other:

**Questions**

Q) I see a lot of errors / warnings on startup, does that matter?

A) Probably not, tensorflow will probably give some deprecation warnings and on startup you may see some memory allocation warnings. You can ignore them. If the bot starts up you should be good to go, just give it a couple seconds.


Q) Can I add this bot to my server? 

A) Moetron is public, but I currently only use it on a few servers that I have whitelisted. I don't currently planning on adding additional servers unless I personally know someone in the server. The reasoning behind this is that he bot's workload is pretty compute heavy and I don't want tons of people spamming it at once. You're free to use this code to host your own bot though.

**Acknowledgement:**
* Aaron Gokaslan for the pre-trained model
* Gwern Branwen for all of their articles about StyleGAN.
* The creators of StyleGAN2, dnnlib is from there w/ all copyrights / attributions remaining.

**Future work**
* Not sure what else to add atm, I'm pretty happy with the state of this bot.

**Contribution**
Let me know if you want to be added as a contributor. If you make a PR I'll probably eventually get around to reviewing it. There's simple unit tests that test the commands, make sure the CI passes or else I won't merge the PR. If you add any new commands to the cog add unit tests for the new commands as well. I'd also recommend testing out the bot yourself before making the PR, I have separate dev moetron I (usually) use to do testing before I commit changes.