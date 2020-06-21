import logging
import pygame

from plat.core.components import BaseComponent
from plat.core.mixins import JoyMoverMixin, GravityMixin, CollisionMixin, JumpFromSquareMixin, AnimationMixin
from plat.core.utils import *

from plat.config import *


class ArrowComponent(JoyMoverMixin, BaseComponent):
    """ Arrow moved by the player in Edit Mode """
    SIZE = 10
    FRICTION = ARROW_FRICTION
    FRICTION_AXIS = JoyMoverMixin.AXIS_BOTH
    ACCELERATION = False
    JOY_SPEED = pygame.Vector2(ARROW_JOY_SPEED)

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
            elif event.button == JOYBTN['A']:
                sq.color = WHITE
            elif event.button == JOYBTN['X']:
                sq.color = RED
            elif event.button == JOYBTN['SHARE']:
                self.grid.reset()

    def on_update(self):
        self.calculate_newpos()


class Player(AnimationMixin, JumpFromSquareMixin, GravityMixin, JoyMoverMixin, BaseComponent):
    """ Player for Game Mode """
    SIZE = 10
    JOY_SPEED = pygame.Vector2(PLAYER_JOY_SPEED)
    
    FRICTION = PLAYER_FRICTION
    MAX_JUMP = PLAYER_MAX_JUMP
    JUMP_FORCE = PLAYER_JUMP_FORCE
    GRAVITY = PLAYER_GRAVITY
    
    def get_animations(self):
        return {
            'standing': self.game.animate.get('playerStand'),
            'walking': self.game.animate.get('playerWalk'),
        }

    def default_animation(self):
        return 'standing'

    def get_attrs(self):
        image = self.game.sprites.get('characters.blue', 'blue_01.png')
        rect = image.get_rect()
        rect.x, rect.y = 40, 40
        return image, rect

    def on_update(self):
        self.calculate_newpos()
        hits = self.get_collissions()
        for hit in hits:
            if hit.color == RED:
                self.pos = (self.pos.x, hit.rect.top)
                self.velocity.y = 0
                self.jumping = False

        if self.velocity.x != 0:
            self.change_animation('walking')
        else:
            self.change_animation('standing')

        super().on_update()
