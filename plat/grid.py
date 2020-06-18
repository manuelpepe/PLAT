import pygame

from typing import List
from random import choice
from dataclasses import dataclass, field

from components import BaseComponent
from utils import *


@dataclass
class Square:
    c: int
    r: int
    grid: 'Grid' = field(repr=False, compare=False)
    height: int = field(default=40, repr=False, compare=False)
    width: int = field(default=40, repr=False, compare=False)
    color: int = WHITE

    @property
    def x(self):
        return self.c * self.width
    
    @property
    def y(self):
        return self.r * self.height
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0)


class Grid(BaseComponent):
    def __init__(self, game, rows: int = 20, cols: int = 20, bheight: int = 40, bwidth: int = 40):
        super().__init__(game)
        self.rows = rows
        self.cols = cols
        self.bheight = bheight
        self.bwidth = bwidth
        self.grid: List[Square] = self._generate_grid()

    def __repr__(self):
        return f'Grid(rows={self.rows}, cols={self.cols})'

    def __str__(self):
        return f'Grid: {self.rows}x{self.cols} ({self.height}x{self.width})'

    @property
    def height(self):
        return self.rows * self.bheight
    
    @property
    def width(self):
        return self.cols * self.bwidth

    def _generate_grid(self) -> List[Square]:
        self.logger.debug(f'Generating grid {self}')
        return [
            [Square(c, r, self, self.bheight, self.bwidth, choice([GREY, WHITE])) for c in range(self.cols)] 
            for r in range(self.rows)
        ]

    def on_draw(self, screen):
        self.logger.debug('Drawing grid')
        for ix, row in enumerate(self.grid):
            for square in row:
                square.draw(screen)
        return True