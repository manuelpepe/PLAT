import logging
import pygame

from plat.core.components import BaseComponent
from plat.core.mixins import JoyMoverMixin, GravityMixin, MoverCollissionsWithBlocksMixin, CollidableJumpFromSolidMixin, AnimationMixin
from plat.core.grid import Block, SolidBlock
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
                self.grid.set_square(*self.pos, Block.from_(sq))
            elif event.button == JOYBTN['X']:
                self.grid.set_square(*self.pos, SolidBlock.from_(sq))
            elif event.button == JOYBTN['SHARE']:
                self.grid.reset()

    def on_update(self):
        self.calculate_newpos()


class Player(AnimationMixin, CollidableJumpFromSolidMixin, GravityMixin, JoyMoverMixin, BaseComponent):
    """ Player for Game Mode """
    SIZE = 10 
    JOY_SPEED = pygame.Vector2(PLAYER_JOY_SPEED)
    
    FRICTION = PLAYER_FRICTION
    MIN_JUMP = PLAYER_MIN_JUMP
    JUMP_FORCE = PLAYER_JUMP_FORCE
    GRAVITY = PLAYER_GRAVITY

    def __init__(self, *args, **kwargs):
        self.walking_right = True
        super().__init__(*args, **kwargs)
            
    def get_animations(self):
        return {
            'standingRight': self.game.animate.get('playerStand', delay=200),
            'standingLeft': self.game.animate.get('playerStand', flip=True),
            'walkingRight': self.game.animate.get('playerWalk', delay=200),
            'walkingLeft': self.game.animate.get('playerWalk', flip=True),
        }

    def default_animation(self):
        return 'standingRight'

    def get_attrs(self):
        image = self.game.sprites.get('characters.blue', 'blue_01.png')
        image = pygame.transform.scale(image, (image.get_width() - 1, image.get_height() - 1))
        rect = image.get_rect()
        rect.x, rect.y = 40, 40
        return image, rect

    def on_update(self):
        self.calculate_newpos()
        super().on_update()
        if self.velocity.x > 0:
            self.change_animation('walkingRight')
            self.walking_right = True
        elif self.velocity.x < 0:
            self.change_animation('walkingLeft')
            self.walking_right = False
        elif self.walking_right:
            self.change_animation('standingRight')
        else:
            self.change_animation('standingLeft')

    def on_event(self, event):
        if event.type == pygame.JOYBUTTONUP:
            sq = self.grid.get_square(*self.pos, 2)
            if event.button == JOYBTN['L1']:
                self.JUMP_FORCE -= 0.1
            elif event.button == JOYBTN['R1']:
                self.JUMP_FORCE += 0.1
            elif event.button == JOYBTN['L2']:
                self.base_acceleration = (0, self.base_acceleration[1] - 0.01)
                self.GRAVITY -= 0.01
            elif event.button == JOYBTN['R2']:
                self.base_acceleration = (0, self.base_acceleration[1] + 0.01)
                self.GRAVITY += 0.01
            elif event.button == JOYBTN['SHARE']:
                self.MIN_JUMP -= 1
            elif event.button == JOYBTN['X']:
                self.MIN_JUMP += 1
        super().on_event(event)