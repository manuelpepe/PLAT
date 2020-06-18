import logging
from utils import *

import pygame
from pygame.math import Vector2

class BaseComponent:
    """ Something that gets drawn to the screen. Can have child components. """
    def __init__(self, game, pos=None, children=None):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.game = game
        self.pos = pos
        self.children = children or []

    def _on_draw(self, screen) -> bool:
        """ Helper inner method to waterfall events to the children. """
        drawchilds = self.on_draw(screen)
        if drawchilds is False:
            return drawchilds
        for child in self.children:
            if isinstance(child, BaseComponent):
                child._on_draw(screen)

    def on_draw(self, screen) -> bool:
        """ Handles drawing to the screen. Returns wheter or not to 
        continue drawing children. """

        pass


class InteractiveComponent(BaseComponent):
    """ Component that listens to user events. """
    def _on_event(self, event) -> bool:
        """ Helper inner method to waterfall events to the children. """
        waterfall = self.on_event(event)
        if waterfall is False:
            return waterfall
        for child in self.children:
            if isinstance(child, InteractiveComponent):
                child._on_event(event)

    def on_event(self, event) -> bool:
        """ Handles pygame events. Returns wheter or not to waterfall
        the event to the children. """
        pass


class GridSizeComponent(BaseComponent):
    """ Proof of concept. """
    def __init__(self, *args, grid=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.text = self.game.font.render(f"{grid}", True, (0, 0, 0))

    def on_draw(self, screen):
        screen.blit(self.text, (0, 0))


class ArrowComponent(InteractiveComponent):
    """ Arrow moved by the player in Edit Mode """
    BASE_SPEED = (10, 10)
    AXIS_DEADZONE = 0.09

    def __init__(self, *args, **kwargs):
        super().__init__(*args, pos=(40, 40), **kwargs)
        self.joy = self.game.joystick
        self.velocity = Vector2(self.BASE_SPEED)

    def on_event(self, event):
        if event.type == pygame.JOYBUTTONDOWN:
            self.logger.info('BUTTON')

    def on_draw(self, screen) -> bool:
        if not self.joy:
            return False
        pos = tuple(int(v) for v in self.pos)
        pygame.draw.circle(screen, BLUE, pos, 20)
        # FIXME: This ties arrows speed to rendering speed (FPS)
        # Should take into account a delta, don't remember the mechanism in pygame rn
        self._calculate_newpos()

    def _calculate_newpos(self):
        print([self.joy.get_axis(a) for a in range(2)])
        self.delta = Vector2(self._normalized_axis_value(0), self._normalized_axis_value(1))
        new = self.pos + self.delta
        self.pos = Vector2(int(new[0]), int(new[1]))

    def _normalized_axis_value(self, axis):
        value = self.joy.get_axis(axis)
        if value > 1 or value < -1 or abs(value) < self.AXIS_DEADZONE:
            return 0
        return value * self.velocity[axis]
