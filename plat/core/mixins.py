import logging
import pygame
import math

from typing import List

from pygame.math import Vector2
from pygame.sprite import Sprite, Group
from pygame.mask import from_surface

from plat.core.utils import *
from plat.core.components import BaseComponent


class MoverMixin:
    """ Call self.calculate_newpos() on child update method. """
    AXIS_X = 1
    AXIS_Y = 2
    AXIS_BOTH = 3
    AXIS_NONE = 4

    # NOTE: 
    FRICTION = -0.16
    FRICTION_AXIS = AXIS_X

    INPUT_VEL_MULTIPLIER = Vector2(2, 2)

    @property
    def direction(self):
        return self.velocity.normalize() if self.velocity.length() > 0 else Vector2(0,0)

    @direction.setter
    def direction(self, newdir):
        self.velocity = self.velocity * newdir.normalize()
    
    def new(self):
        super().new()
        self.velocity = Vector2(0, 0)
        self.base_acceleration = (0, 0)
        self.acceleration = Vector2(self.base_acceleration)
        self.last_pos = None

    def calculate_newpos(self):
        self.last_pos = self.pos
        self.input_vel = self.get_input_vel()
        self.calculated_vel = self._get_calculated_vel()
        self.acceleration = self._calculate_acceleration()
        self.velocity = self._calculate_velocity()
        self.pos = self._calculate_position()

    def _get_calculated_vel(self):
        vel = Vector2(self.input_vel)
        vel.x *= self.INPUT_VEL_MULTIPLIER.x
        vel.y *= self.INPUT_VEL_MULTIPLIER.y
        return vel

    def _calculate_acceleration(self) -> Vector2:
        """ Returns new acceleration in current update """
        acc = self.calculate_acceleration()
        print('acc before joystick input:', acc)
        acc = acc + self.calculated_vel
        acc = self._calculate_friction(acc)
        print('acc after frition: ', acc)
        return acc

    def _calculate_friction(self, acc) -> Vector2:
        # if self.FRICTION_AXIS == self.AXIS_X:
        #     # print(f"(acc) {acc.x} + {self.velocity.x} * {self.FRICTION} = {acc.x + self.velocity.x * self.FRICTION}")
        #     acc.x += self.velocity.x * self.FRICTION
        # elif self.FRICTION_AXIS == self.AXIS_Y:
        #     acc.y += self.velocity.y * self.FRICTION
        # elif self.FRICTION_AXIS == self.AXIS_BOTH:
        #     acc += self.velocity * self.FRICTION
        # elif self.FRICTION_AXIS == self.AXIS_NONE:
        #     pass
        # else:
        #     raise ValueError(f'Unkown FRICTION_AXIS for {self}')
        acc += self.velocity * self.FRICTION
        return acc

    def calculate_acceleration(self) -> Vector2:
        return Vector2(self.base_acceleration)

    def _calculate_velocity(self) -> Vector2:
        """ Returns new velocity in current update. """
        vel = self.velocity + self.acceleration
        vel.x = 0 if abs(vel.x) < 0.1 else vel.x
        vel.y = 0 if abs(vel.y) < 0.1 else vel.y

        return vel

    def _calculate_position(self):
        if self.FRICTION_AXIS != self.AXIS_NONE:
            # print(f"(pos) {self.pos} + {self.velocity} + 0.5 * {self.acceleration} = {self.pos + self.velocity + 0.5 * self.acceleration}")
            return self.pos + self.velocity + 0.5 * self.acceleration
        else:
            return self.pos + self.velocity


class JoyMoverMixin(MoverMixin):
    AXIS_DEADZONE = 0.30
    FRICTION = -0.5

    def new(self):
        super().new()
        self.joy = self.game.joystick
        self.joyinput = (0, 0)

    def get_input_vel(self):
        return self._normalized_axis_value(0), self._normalized_axis_value(1)

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


class CollisionableMixin(BaseComponent):
    # TODO: Add flags to enable collisions on each side
    COLLIDE_LEFT = True
    COLLIDE_RIGHT = True
    COLLIDE_TOP = True
    COLLIDE_BOTTOM = True
    
    def new(self):
        self.mask = None
        super().new()

    def on_update(self):
        super().on_update()
        if self.image:
            self.mask = from_surface(self.image)

    def get_collissions(self) -> List[Sprite]:
        dir_ = self._parse_direction(self.direction)
        self.rect.y += dir_.y
        cols = pygame.sprite.spritecollide(self, self.game.state.obj.grid.children.sprites, False) 
        self.rect.y -= dir_.y
        self.rect.x += dir_.x
        cols += pygame.sprite.spritecollide(self, self.game.state.obj.grid.children.sprites, False) 
        self.rect.x -= dir_.x
        return cols

    def _check_collisions(self):
        hits = self.get_collissions()
        for hit in hits:
            self._check_collision(hit)

    def _check_collision(self, hit):
        pass

    def on_collision_start(self, other: 'CollisionableMixin'):
        pass

    def on_collision_end(self, other: 'CollisionableMixin'):
        pass


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
        if now - anim.last_update > anim.delay:
            frame = anim.get_next_frame(now)
            self.image = frame


