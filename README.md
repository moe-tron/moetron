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

## Setup:

To get this working follow the steps on the official StyleGAN2 repo:
https://github.com/NVlabs/stylegan2

It's kind of a pain to set up everything... Honestly I'd just try to get StyleGAN2 running first on your machine, then you'll know that this will work. After you get it working, you should just need discord py and to set up your bot w/ discord to get your key.

See the license under docs, it's the same as the stylegan2 license.
https://nvlabs.github.io/stylegan2/license.html

The model I used can be obtained from:
https://www.gwern.net/Faces#stylegan-2
you can use whatever model you want obviously, but this bot was built around using this one. Hence the "moe" naming and such.

All credits for the trained model goes to the original creator Aaron Gokaslan.

Currently images are kept in the results dir, but not tracked in vcs so if you get a image you really like and you're running the bot yourself you can find the image in the directory. Obviously this is under the assumption that you're only running the bot on a few servers and it isn't being spammed too much.

This bot is not used for commercial purposes, and derivatives of this work should not be used for commercial purposes. See the license for more information.

## Other:

**Questions**
Q) Why do you use a truncation-psi of 0.55
A) Personal preference. Enough variation without the images being too messed up.

Q) Why is there a lot of weird headwear / animal ears?
A) No idea, my guess is that there's a large variance in headwear / ears in the anime art that the model was trained on so it's difficult for the model to correctly generate stuff like that. That and the messy half ear half bow stuff you see was presumably good enough to pass the discriminator. Anime-art style faces are generally the same though so the model does pretty well with the face itself.

Q) I see a lot of errors / warnings on startup, does that matter?
A) Probably not, tensorflow will probably give some deprecation warnings and on startup you may see some memory allocation warnings. You can ignore them. If the bot starts up you should be good to go, just give it a couple seconds.

Q) Can I use this for stuff other than anime images?
A) Sure, if you find a trained model that produces images that you want you can just replace the default network in the run_generator.py constructor and use that.

**Acknowledgement:**
* Aaron Gokaslan for the pre-trained model
* Gwern Branwen for all of their articles about StyleGAN.
* The creators of StyleGAN2.

**Future work**
* Possibly unit tests although there's not really much logic to test.
* Implement some kind of style mixing letting you mix seed A's style with seed B.

**Contribution**
Feel free to make a PR. I'll probably eventually get around to reviewing it. There's not any tests currently so please make sure your code is working before you make the PR.