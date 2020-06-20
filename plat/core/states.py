import logging
from plat.core.components import BaseComponent, SpriteGroup


class State:
    COMPONENTS = None

    def __init__(self, game, grid):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.game = game
        self.grid = grid
        self.children = SpriteGroup()
        self._init_components()

    def _init_components(self):
        if not self.COMPONENTS:
            raise RuntimeError('Empty state')
        self.children.add(self.grid)
        for c in self.COMPONENTS:
            self.children.add(c(self.game, grid=self.grid))

    def _del_components(self):
        for c in self.children:
            self.children.remove(c)

    def reset_components(self):
        self._del_components()
        self.children = SpriteGroup()
        self._init_components()

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
