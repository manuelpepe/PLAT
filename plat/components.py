import logging
from utils import *
from collections import namedtuple

import pygame
from pygame.math import Vector2


Pos = namedtuple('Pos', 'x y')

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

class ArrowComponent(BaseComponent):
    """ Arrow moved by the player in Edit Mode """

    BASE_SPEED = (10, 10)
    AXIS_DEADZONE = 0.09

    def __init__(self, *args, grid=None, **kwargs):
        self.grid = grid
        super().__init__(*args, **kwargs)

    @property
    def pos(self):
        return self.rect.x, self.rect.y

    @pos.setter
    def pos(self, value):
        self.rect.x = value[0]
        self.rect.y = value[1]

    def get_attrs(self):
        image = pygame.Surface((20, 20))
        image.fill(BLACK)
        rect = image.get_rect()
        rect.x = 40
        rect.y = 40
        return image, image.get_rect()

    def new(self):
        self.joy = self.game.joystick
        self.velocity = Vector2(self.BASE_SPEED)

    def on_event(self, event):
        if event.type == pygame.JOYBUTTONUP:
            sq = self.grid.get_square(*self.pos, 2)
            if event.button == JOYBTN['Y']:
                print(sq)
            elif event.button == JOYBTN['B']:
                sq.color = WHITE
            elif event.button == JOYBTN['X']:
                sq.color = RED
            elif event.button == JOYBTN['SHARE']:
                self.grid.reset()

    def on_update(self) -> bool:
        # FIXME: This ties arrows speed to rendering speed (FPS)
        # Should take into account a delta, don't remember the mechanism in pygame rn
        self._calculate_newpos()

    def on_draw(self, screen):
        pygame.draw.circle(screen, BLUE, self.pos, 20)

    def _calculate_newpos(self):
        self.delta = Vector2(self._normalized_axis_value(0), self._normalized_axis_value(1))
        new = self.pos + self.delta
        self.rect.x = int(new[0])
        self.rect.y = int(new[1])

    def _normalized_axis_value(self, axis):
        value = self.joy.get_axis(axis)
        if value > 1 or value < -1 or abs(value) < self.AXIS_DEADZONE:
            return 0
        return value * self.velocity[axis]


class Player(BaseComponent):
    """ Player for Game Mode """

    def on_event(self, event) -> bool:
        pass
    def on_draw(self, screen) -> bool:
        pass