import math
import pygame

from pygame.math import Vector2

from plat.core.grid import Block, SolidBlock, LiquidBlock
from plat.core.mixins import CollisionableMixin, MoverMixin
from plat.core.utils import *


class MoverCollissionsWithBlocksMixin(MoverMixin, CollisionableMixin):
    def _parse_direction(self, dir_):
        return Vector2((
            math.trunc(dir_.x * 1),
            math.trunc(dir_.y * 1),
        ))
        
    def on_update(self):
        self._check_collisions()
        super().on_update()


    def _check_collision(self, hit):
        super()._check_collision(hit)
        if isinstance(hit, SolidBlock):
            new_self_center = Vector2(self.center) - Vector2(hit.center)
            angle_to_hit = new_self_center.angle_to(Vector2((0, 0)))

            if self._left_of(angle_to_hit) and hit.COLLIDE_LEFT: 
                # print(f'Left Collision angle_to_hit: {angle_to_hit} ({self.center} to {hit.center})')
                self.rect.right = hit.rect.left
                self.velocity.x = 0
            elif self._below_of(angle_to_hit) and hit.COLLIDE_BOTTOM:
                # print(f'Top Collision angle_to_hit: {angle_to_hit} ({self.center} to {hit.center})')
                self.rect.top = hit.rect.bottom
                self.velocity.y = 0
            elif self._right_of(angle_to_hit) and hit.COLLIDE_RIGHT:
                # print(f'Right Collision angle_to_hit: {angle_to_hit} ({self.center} to {hit.center})')
                self.rect.left = hit.rect.right
                self.velocity.x = 0
            elif self._above_of(angle_to_hit) and hit.COLLIDE_TOP:
                # print(f'Bottom Collision angle_to_hit: {angle_to_hit} ({self.center} to {hit.center})')
                self.rect.bottom = hit.rect.top
                self.velocity.y = 0

    def _going_up(self):
        return self.velocity.y < 0

    def _left_of(self, angle):
        return 135 <= angle or angle < -135

    def _right_of(self, angle):
        return -45 <= angle < 45

    def _below_of(self, angle):
        return -45 > angle >= -135 and self._going_up()
        
    def _above_of(self, angle):
        return 134 > angle >= 48


class JumpMixin(MoverCollissionsWithBlocksMixin):
    MIN_JUMP = 3
    JUMP_FORCE = 3
    STORED_JUMP_FORCE = 0

    def on_event(self, event):
        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == JOYBTN['A']:
                self.start_jump()
        if event.type == pygame.JOYBUTTONUP:
            if event.button == JOYBTN['A']:
                self.end_jump()

    def calculate_acceleration(self):
        acc = super().calculate_acceleration()
        print('acc before jump:', acc)
        print('stored force:', self.STORED_JUMP_FORCE)
        if self.STORED_JUMP_FORCE:
            acc +=  Vector2(0, -self.STORED_JUMP_FORCE)
            self.STORED_JUMP_FORCE = 0
        print('acc after jump:', acc)
        return acc

    def start_jump(self):
        self.STORED_JUMP_FORCE = self.JUMP_FORCE

    def end_jump(self):
        if self.velocity.y < -self.MIN_JUMP:
            self.velocity.y = -self.MIN_JUMP


class CollidableJumpFromSolidMixin(JumpMixin):
    def new(self):
        super().new()

    def start_jump(self):
        if self.is_on_plat():
            super().start_jump()

    def is_on_plat(self):
        if self.pos.y == self.game.state.obj.grid.height:
            return True
        self.rect.y += 1
        hits = self.get_collissions()
        self.rect.y -= 1
        collisions = filter(lambda h: isinstance(h, SolidBlock), hits)
        for col in collisions:
            if col.rect.top == self.rect.bottom:
                return True
        return False


class SwimmerMixin(JumpMixin):
    CURRENT_LIQUID_SLOWDOWN = 0

    def _check_collision(self, hit):
        super()._check_collision(hit)
        if isinstance(hit, LiquidBlock):
            self._apply_liquid_slowdown(hit)

    def _apply_liquid_slowdown(self, hit):
        self.CURRENT_LIQUID_SLOWDOWN = hit.SLOWDOWN_DELTA

    def _calculate_velocity(self):
        vel = super()._calculate_velocity()
        if self.CURRENT_LIQUID_SLOWDOWN:
            vel.x /= 1 + self.CURRENT_LIQUID_SLOWDOWN 
            vel.x = 0 if abs(vel.x) < 0.1 else vel.x


            self.CURRENT_LIQUID_SLOWDOWN = 0
            # vel.y = 0 if abs(vel.y) < 0.1 else vel.y
        return vel

    # def _calculate_acceleration(self):
    #     bef_fri = self.FRICTION
    #     bef_fri_axs = self.FRICTION_AXIS

    #     self.FRICTION *= 1 + self.CURRENT_LIQUID_SLOWDOWN
    #     self.FRICTION_AXIS = self.AXIS_BOTH

    #     acc = super()._calculate_acceleration()

    #     self.FRICTION = bef_fri
    #     self.FRICTION_AXIS = bef_fri_axs
    #     self.CURRENT_LIQUID_SLOWDOWN = 0

    #     print('Acc from Swimmer: ', acc)
    #     return acc


    # def _calculate_acceleration(self):
    #   vel = super()._calculate_velocity()
    #   vel *= 1 - self.CURRENT_LIQUID_SLOWDOWN
    #   self.CURRENT_LIQUID_SLOWDOWN = 0
    #   return vel