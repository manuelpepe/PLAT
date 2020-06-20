import logging

from pygame.math import Vector2

from plat.core.utils import *


class MoverMixin:
    """ Call self.calculate_newpos() on child update method. """
    AXIS_X = 1
    AXIS_Y = 2
    AXIS_BOTH = 3

    FRICTION = -0.16
    FRICTION_AXIS = AXIS_X
    
    def new(self):
        self.velocity = Vector2(0, 0)
        self.base_acceleration = (0, 0)
        self.acceleration = Vector2(self.base_acceleration)

    def calculate_newpos(self):
        self.acceleration = self._calculate_acceleration()
        self.velocity = self._calculate_velocity()
        self.pos = self._calculate_position()
        print(self.acceleration, self.velocity, self.pos)


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
        return self.pos + self.velocity + 0.5 * self.acceleration


class JoyMoverMixin(MoverMixin):
    JOY_SPEED = Vector2(2, 2)
    AXIS_DEADZONE = 0.12
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
    GRAVITY = 2
    def new(self):
        super().new()
        self.base_acceleration = (0, self.GRAVITY)
