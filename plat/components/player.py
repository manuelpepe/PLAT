import logging
import pygame

from plat.core.components import BaseComponent
from plat.core.mixins import JoyMoverMixin, GravityMixin, CollisionMixin
from plat.core.utils import *


class ArrowComponent(JoyMoverMixin, BaseComponent):
    """ Arrow moved by the player in Edit Mode """
    SIZE = 10
    FRICTION_AXIS = JoyMoverMixin.AXIS_BOTH

    def __init__(self, *args, grid=None, **kwargs):
        self.grid = grid
        super().__init__(*args, **kwargs)

    def get_attrs(self):
        image = pygame.Surface((self.SIZE, self.SIZE))
        image.fill(BLUE)
        rect = image.get_rect()
        rect.x, rect.y = 40, 40
        return image, rect

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

    def on_update(self):
        self.calculate_newpos()


class Player(CollisionMixin, GravityMixin, JoyMoverMixin, BaseComponent):
    """ Player for Game Mode """
    SIZE = 10
    JOY_SPEED = pygame.Vector2(2, 0)
    
    def __init__(self, *args, grid=None, **kwargs):
        self.grid = grid
        super().__init__(*args, **kwargs)

    def get_attrs(self):
        image = pygame.Surface((self.SIZE, self.SIZE))
        image.fill(BLACK)
        rect = image.get_rect()
        rect.x, rect.y = 40, 40
        return image, rect

    def on_update(self):
        print(self)
        self.calculate_newpos()
        hits = self.get_collissions()
        for hit in hits:
            if hit.color == RED:
                self.pos = (self.pos.x, hit.rect.top)
                self.velocity.y = 0
                print(self)
