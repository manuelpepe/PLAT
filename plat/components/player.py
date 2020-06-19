import logging
import pygame

from plat.core.components import BaseComponent
from plat.core.utils import *


class ArrowComponent(BaseComponent):
    """ Arrow moved by the player in Edit Mode """

    BASE_SPEED = (10, 10)
    AXIS_DEADZONE = 0.09
    SIZE = 10

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
        image = pygame.Surface((self.SIZE, self.SIZE))
        image.fill(BLACK)
        rect = image.get_rect()
        rect.x = 40
        rect.y = 40
        return image, image.get_rect()

    def new(self):
        self.joy = self.game.joystick
        self.velocity = pygame.Vector2(self.BASE_SPEED)

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
        # FIXME: This ties arrow speed to rendering speed (FPS)
        # Should take into account a delta, don't remember the mechanism in pygame rn
        self._calculate_newpos()

    def on_draw(self, screen):
        pygame.draw.circle(screen, BLUE, self.pos, self.SIZE)

    def _calculate_newpos(self):
        self.delta = pygame.Vector2(self._normalized_axis_value(0), self._normalized_axis_value(1))
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