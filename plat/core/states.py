import logging
import pygame
from plat.core.components import BaseComponent


class State:
    def __init__(self, game, children: list = None):
        children = children or []
        self.logger = logging.getLogger(self.__class__.__name__)
        self.game = game
        self.children = pygame.sprite.Group()
        for c in children:
            self.children.add(c)

    def start(self):
        pass
    
    def end(self):
        pass
    
    def event(self, event):
        for child in self.children:
            child.event(event)

    def update(self):
        self.children.update()

    def draw(self, screen):
        self._draw(self, screen)

    def _draw(self, obj, screen):
        if hasattr(obj, 'on_draw'):
            obj.on_draw(screen)

        obj.children.draw(screen)
        for c in obj.children:
            if len(c.children) > 0:
                self._draw(c, screen)

            if hasattr(c, 'on_draw'):
                c.on_draw(screen)
