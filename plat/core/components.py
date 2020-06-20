import logging

from typing import List
from collections import namedtuple

from pygame.math import Vector2
from pygame.sprite import Group, Sprite

from plat.core.utils import *


Pos = namedtuple("Pos", "x y")

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
        return Pos(self.rect.midbottom[0], self.rect.midbottom[1])

    @pos.setter
    def pos(self, xypair):
        """ Pos will remain inside boundries of grid. Hitting an edge will stop the player. """
        x, y = xypair
        if x < 0 or self.game.state.grid.width < x:
            self.velocity.x = 0
        if y < 0 or self.game.state.grid.height < y:
            self.velocity.y = 0
        x = min(max(x, 0), self.game.state.grid.width)
        y = min(max(y, 0), self.game.state.grid.height)
        self.rect.midbottom = (x, y)

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

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        if len(self.children):
            for child in self.children:
                child.draw(screen)

    def __repr__(self):
        return f"<{self.__class__.__name__}  pos={self.pos} acc={self.acceleration} vel={self.velocity}>"



class SpriteGroup:
    ALL_SPRITES = Group()

    def __init__(self):
        self.sprites = Group()

    @property
    def children(self):
        return self.sprites

    def add(self, sprite: Sprite):
        self.ALL_SPRITES.add(sprite)
        self.sprites.add(sprite)

    def remove(self, sprite: Sprite):
        self.ALL_SPRITES.remove(sprite)
        self.sprites.remove(sprite)

    def update(self):
        self.sprites.update()

    def draw(self, screen):
        for sprite in self.sprites:
            if hasattr(sprite, 'on_draw'):
                sprite.on_draw(screen)
            sprite.draw(screen)

    def empty(self):
        return self.sprites.empty()

    def __iter__(self):
        return self.sprites.__iter__()

    def __len__(self):
        return len(self.sprites)
