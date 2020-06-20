import pygame
import logging

from typing import List
from collections import namedtuple

from pygame.math import Vector2

from plat.core.utils import *

class BaseComponent(pygame.sprite.Sprite):

    def __init__(self, game, children: List[pygame.sprite.Sprite] = None):
        children = children or []
        pygame.sprite.Sprite.__init__(self)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.game = game
        self.image, self.rect = self.get_attrs()
        print(self.rect.midbottom)
        self.children = pygame.sprite.Group()
        for child in children:
            self.children.add(child) 
        self.new()

    @property
    def pos(self):
        return self.rect.midbottom[0], self.rect.midbottom[1]

    @pos.setter
    def pos(self, xypair):
        self.rect.midbottom = xypair

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
