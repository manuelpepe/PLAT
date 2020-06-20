import logging
import pygame

from typing import List

from pygame.math import Vector2
from pygame.sprite import Sprite, Group

from plat.core.utils import *
from plat.core.components import BaseComponent

class MoverMixin:
    """ Call self.calculate_newpos() on child update method. """
    AXIS_X = 1
    AXIS_Y = 2
    AXIS_BOTH = 3
    AXIS_NONE = 4

    FRICTION = -0.16
    FRICTION_AXIS = AXIS_X

    def new(self):
        super().new()
        self.velocity = Vector2(0, 0)
        self.base_acceleration = (0, 0)
        self.acceleration = Vector2(self.base_acceleration)

    def calculate_newpos(self):
        self.acceleration = self._calculate_acceleration()
        self.velocity = self._calculate_velocity()
        self.pos = self._calculate_position()
        print(self)

    def _calculate_acceleration(self) -> Vector2:
        """ Returns new acceleration in current update """
        acc = self.calculate_acceleration()
        if self.FRICTION_AXIS == self.AXIS_X:
        	acc.x += self.velocity.x * self.FRICTION
        elif self.FRICTION_AXIS == self.AXIS_Y:
        	acc.y += self.velocity.y * self.FRICTION
        elif self.FRICTION_AXIS == self.AXIS_BOTH:
        	acc += self.velocity * self.FRICTION
        else:
        	raise ValueError(f'Unkown FRICTION_AXIS for {self}')
        return acc

    def calculate_acceleration(self) -> Vector2:
        return Vector2(self.base_acceleration)

    def _calculate_velocity(self) -> Vector2:
        """ Returns new velocity in current update """
        return self.velocity + self.acceleration

    def _calculate_position(self):
        if self.FRICTION_AXIS != self.AXIS_NONE:
            return self.pos + self.velocity + 0.5 * self.acceleration
        else:
            return self.pos + self.velocity


class JoyMoverMixin(MoverMixin):
    JOY_SPEED = Vector2(2, 2)
    AXIS_DEADZONE = 0.30
    FRICTION = -0.5

    def new(self):
        super().new()
        self.joy = self.game.joystick

    def calculate_acceleration(self):
        acc = Vector2(self._normalized_axis_value(0), self._normalized_axis_value(1))
        acc.x = acc.x * self.JOY_SPEED.x
        acc.y = acc.y * self.JOY_SPEED.y
        acc += super().calculate_acceleration()
        return acc

    def _normalized_axis_value(self, axis):
        value = self.joy.get_axis(axis)
        if value > 1 or value < -1 or abs(value) < self.AXIS_DEADZONE:
            return 0
        return value


class GravityMixin(MoverMixin):
    GRAVITY = 0.1
    def new(self):
        super().new()
        self.base_acceleration = (0, self.GRAVITY)


class CollisionMixin:
    def get_collissions(self) -> List[Sprite]:
        return pygame.sprite.spritecollide(self, self.game.state.grid.children.sprites, False) 


class JumpMixin(MoverMixin, BaseComponent):
    MAX_JUMP = 3
    JUMP_FORCE = 4

    def on_event(self, event):
        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == JOYBTN['A']:
                self.start_jump()
        if event.type == pygame.JOYBUTTONUP:
            if event.button == JOYBTN['A']:
                self.end_jump()


    def start_jump(self):
        self.jumping = True
        self.velocity.y = -self.JUMP_FORCE

    def end_jump(self):
        if self.jumping:
            if self.velocity.y < -self.MAX_JUMP:
                self.velocity.y = -self.MAX_JUMP


class JumpFromSquareMixin(JumpMixin, CollisionMixin):
    def new(self):
        super().new()
        self.jumping = False

    def start_jump(self):
        if self.is_on_plat():
            super().start_jump()

    def is_on_plat(self):
        print(self.game.state.grid.height)
        if self.pos.y == self.game.state.grid.height:
            return True
        self.rect.y += 1
        hits = self.get_collissions()
        self.rect.y -= 1
        return any(h.color == RED for h in hits)
