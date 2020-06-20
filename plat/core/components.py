import logging

from typing import List
from collections import namedtuple

from pygame.math import Vector2
from pygame.sprite import Group, Sprite

from plat.core.utils import *

class BaseComponent(Sprite):

    def __init__(self, game, children: List[Sprite] = None):
        children = children or []
        Sprite.__init__(self)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.game = game
        self.image, self.rect = self.get_attrs()
        self.children = SpriteGroup()
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



class SpriteGroup:
    ALL_SPRITES = Group()

    def __init__(self):
        self.groups = {
            'all': Group()
        }
        self.sprites = Group()

    def add(self, sprite: Sprite):
        self.ALL_SPRITES.add(sprite)
        self.sprites.add(sprite)

    def update(self):
        self.sprites.update()

    def draw(self, screen):
        self.sprites.draw(screen)

    def empty(self):
        return self.sprites.empty()

    def check_player_collided(self):
        pass #pygame.sprite.spritecollide(self.PLAYER, self.)

    def __iter__(self):
        return self.sprites.__iter__()

    def __len__(self):
        return len(self.sprites)
