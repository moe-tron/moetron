# Copyright (c) 2019, NVIDIA Corporation. All rights reserved.
#
# This work is made available under the Nvidia Source Code License-NC.
# To view a copy of this license, visit
# https://nvlabs.github.io/stylegan2/license.html

import numpy as np
import PIL.Image
import dnnlib
import dnnlib.tflib as tflib
import pickle

# Obviously changed from the old run_generator.py in stylegan2, but I kept the copyright because a lot of logic/code was re-used here.
class Generator:
    def __init__(self, networkpath="pretrained/2020-01-11-skylion-stylegan2-animeportraits-networksnapshot-024664.pkl"):
        self._cached_networks = dict()
        self._G, self._D, self.Gs = self.load_networks(networkpath)
        self.noise_vars = [var for name, var in self.Gs.components.synthesis.vars.items() if name.startswith('noise')]
        self.Gs_kwargs = dnnlib.EasyDict()
        self.Gs_kwargs.output_transform = dict(func=tflib.convert_images_to_uint8, nchw_to_nhwc=True)
        self.Gs_kwargs.randomize_noise = True

    def generate_one_image(self, seed, truncation_psi = 0.55):
        self.Gs_kwargs.truncation_psi = truncation_psi
        print('Generating image for seed %d ...' % seed)
        rnd = np.random.RandomState(seed)
        z = rnd.randn(1, *self.Gs.input_shape[1:]) 
        tflib.set_vars({var: rnd.randn(*var.shape.as_list()) for var in self.noise_vars}) 
        images = self.Gs.run(z, None, **self.Gs_kwargs) 
        img_path = 'results/seed%04d.png' % seed
        PIL.Image.fromarray(images[0], 'RGB').save(img_path)
        return img_path

    def load_networks(self, network_path):
        if network_path in self._cached_networks:
            return self._cached_networks[network_path]
        stream = open(network_path, 'rb')
        tflib.init_tf()
        with stream:
            G, D, Gs = pickle.load(stream, encoding='latin1')
        self._cached_networks[network_path] = G, D, Gs
        return G, D, Gs
