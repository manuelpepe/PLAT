import pygame
from plat.core.components import BaseComponent


class PauseTitle(BaseComponent):
    """ Show grid dimensions. """
    def get_attrs(self):
        self.text = self.game.font.render("PAUSED", True, (0, 0, 0))
        return self.text, self.text.get_rect()

    def on_draw(self, screen):
        screen.blit(self.text, (0, 0))
