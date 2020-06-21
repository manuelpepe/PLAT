import logging
import pygame
import math

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

    def _calculate_acceleration(self) -> Vector2:
        """ Returns new acceleration in current update """
        acc = self.calculate_acceleration()
        if self.FRICTION_AXIS == self.AXIS_X:
        	acc.x += self.velocity.x * self.FRICTION
        elif self.FRICTION_AXIS == self.AXIS_Y:
        	acc.y += self.velocity.y * self.FRICTION
        elif self.FRICTION_AXIS == self.AXIS_BOTH:
        	acc += self.velocity * self.FRICTION
        elif self.FRICTION_AXIS == self.AXIS_NONE:
            pass
        else:
        	raise ValueError(f'Unkown FRICTION_AXIS for {self}')

        return acc

    def calculate_acceleration(self) -> Vector2:
        return Vector2(self.base_acceleration)

    def _calculate_velocity(self) -> Vector2:
        """ Returns new velocity in current update. """
        vel = self.velocity + self.acceleration    
        vel.x = 0 if abs(vel.x) < 0.01 else vel.x
        vel.y = 0 if abs(vel.y) < 0.01 else vel.y
        return vel

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
        self.joyinput = (0, 0)
        self.beforefic = None
        self.baseacc = None

    def calculate_acceleration(self):
        self.joyinput = self._normalized_axis_value(0), self._normalized_axis_value(1)
        self.baseacc = super().calculate_acceleration()
        acc = Vector2(self.joyinput)
        acc.x = acc.x * self.JOY_SPEED.x
        acc.y = acc.y * self.JOY_SPEED.y
        beforefic = self.baseacc + acc
        self.beforefic = (beforefic.x, beforefic.y)
        return beforefic

    def _normalized_axis_value(self, axis):
        """ joy.get_axis() returns a number between """
        value = self.joy.get_axis(axis)
        if abs(value) < self.AXIS_DEADZONE:
            return 0
        return max(min(value, 0.99), -0.99)


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
        if self.pos.y == self.game.state.grid.height:
            return True
        self.rect.y += 1
        hits = self.get_collissions()
        self.rect.y -= 1
        return any(h.color == RED for h in hits)


class AnimationMixin(BaseComponent):
    def new(self):
        self.animations = self.get_animations()
        self.current_animation = self.default_animation()
        super().new()

    def get_animations(self) -> dict:
        """ Return dict of ´name-animation´ pairs """
        return {}

    def default_animation(self) -> str:
        """ Return name of default animation """
        return ''

    def on_update(self):
        super().on_update()
        self.animate()

    def change_animation(self, name):
        if name not in self.animations.keys():
            raise KeyError(name)
        if name != self.current_animation:
            self.animations[self.current_animation].reset()
            self.current_animation = name
            self.animations[self.current_animation].reset()

    def animate(self):
        now = pygame.time.get_ticks()
        anim = self.animations[self.current_animation]
        if now - anim.last_update > anim.speed:
            frame = anim.get_next_frame(now)
            self.image = frame

