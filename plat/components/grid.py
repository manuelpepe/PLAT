import pygame
from plat.core.components import BaseComponent
from plat.core.utils import *


class GridLineComponent(BaseComponent):
    def get_attrs(self):
        self.text = self.game.font.render(f"{self.grid}", True, (0, 0, 0))
        return self.text, self.text.get_rect()

    def on_draw(self, screen):
        for ix, row in enumerate(self.grid.grid):
            for square in row:
                if ix == len(self.grid.grid) - 1:
                    pygame.draw.line(screen, GREY, (square.x, 0), (square.x, self.game.height))
            _y = ix * self.grid.bwidth
            pygame.draw.line(screen, GREY, (0, _y), (self.game.width, _y))
        return True


class GridSizeComponent(BaseComponent):
    """ Show grid dimensions. """
    def get_attrs(self):
        self.text = self.game.font.render(f"{self.grid}", True, (0, 0, 0))
        return self.text, self.text.get_rect()

    def on_draw(self, screen):
        screen.blit(self.text, (0, 0))
