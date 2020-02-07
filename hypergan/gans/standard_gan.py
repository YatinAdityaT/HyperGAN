import importlib
import json
import numpy as np
import os
import sys
import time
import uuid
import copy

from hypergan.discriminators import *
from hypergan.distributions import *
from hypergan.generators import *
from hypergan.inputs import *
from hypergan.samplers import *
from hypergan.trainers import *

import hyperchamber as hc
from hyperchamber import Config
import hypergan as hg

from hypergan.gan_component import ValidationException, GANComponent
from .base_gan import BaseGAN

class StandardGAN(BaseGAN):
    """ 
    Standard GANs consist of:
    
    *required to sample*
    
    * latent
    * generator
    * sampler

    *required to train*

    * discriminator
    * loss
    * trainer
    """
    def __init__(self, *args, **kwargs):
        self.discriminator = None
        self.latent = None
        self.generator = None
        self.loss = None
        self.trainer = None
        self.features = []
        BaseGAN.__init__(self, *args, **kwargs)

    def required(self):
        return "generator".split()

    def create(self):
        config = self.config

        self.latent = self.create_component(config.z_distribution or config.latent)
        self.generator = self.create_component(config.generator, input=self.latent)
        self.discriminator = self.create_component(config.discriminator)
        self.loss = self.create_component(config.loss, discriminator=self.discriminator)
        self.losses = [self.loss]
        self.trainer = self.create_component(config.trainer)

    def g_vars(self):
        return self.latent.variables() + self.generator.variables()
    def d_vars(self):
        return self.discriminator.variables()

    def input_nodes(self):
        "used in hypergan build"
        return [
                self.android_input
        ]

    def output_nodes(self):
        "used in hypergan build"
        return [
                self.android_output
        ]
