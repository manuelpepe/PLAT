import logging
from collections import namedtuple

import pygame
from pygame.math import Vector2

from plat.core.utils import *

class BaseComponent(pygame.sprite.Sprite):

    def __init__(self, game, children: list = None):
        pygame.sprite.Sprite.__init__(self)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.game = game
        self.image, self.rect = self.get_attrs()

        children = children or []
        g = pygame.sprite.Group()
        for c in children:
            g.add(c)
        self.children = g

        self.new()

    def get_attrs(self):
        raise NotImplementedError()

    def new(self):
        pass

    def event(self, event):
        self.on_event(event)
        for child in self.children:
            child.on_event(event)

    def on_event(self, event):
        pass

    def update(self):
        self.on_update()
        if self.children:
            self.children.update()

    def on_update(self):
        pass
