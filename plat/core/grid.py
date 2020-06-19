import logging
import pygame

from typing import List
from random import choice
from dataclasses import dataclass, field

from plat.core.components import BaseComponent
from plat.core.utils import *


class Square(BaseComponent):
    c: int
    r: int
    grid: 'Grid' = field(repr=False, compare=False)
    height: int = field(default=40, repr=False, compare=False)
    width: int = field(default=40, repr=False, compare=False)
    color: int = field(default=WHITE, repr=False, compare=False)

    def __init__(self, *args, c=None, r=None, grid=None, height=None, width=None, color=None, **kwargs):
        self.c = c
        self.r = r
        self.grid = grid
        self.height = height
        self.width = width
        self._color = color
        super().__init__(*args, **kwargs)

    @property
    def color(self):
        return self._color
    
    @color.setter
    def color(self, value):
        self._color = value
        self.image.fill(value)

    def get_attrs(self):
        img = pygame.Surface((self.height, self.width))
        img.fill(self.color)
        rect = img.get_rect()
        rect.x = self.x
        rect.y = self.y
        return img, rect

    @property
    def x(self):
        return self.c * self.width
    
    @property
    def y(self):
        return self.r * self.height


class Grid(BaseComponent):
    ROWCOLS = 1
    XY = 2

    def __init__(self, game, rows: int = 20, cols: int = 20, bheight: int = 40, bwidth: int = 40, **kwargs):
        self.logger = logging.getLogger('Grid')
        self.rows = rows
        self.cols = cols
        self.bheight = bheight
        self.bwidth = bwidth
        super().__init__(game, **kwargs)
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

    def get_attrs(self):
        img = pygame.Surface((self.rows * self.bheight, self.cols * self.bwidth))
        img.fill(WHITE)
        return img, img.get_rect()

    def _generate_grid(self) -> List[Square]:
        self.logger.debug(f'Generating grid {self}')
        self.grid = [
            [Square(self.game, c=c, r=r, grid=self, height=self.bheight, width=self.bwidth, color=WHITE) for c in range(self.cols)] 
            for r in range(self.rows)
        ]
        self.children.empty()
        for r in self.grid:
            for c in r:
                self.children.add(c)
        return self.grid

    def reset(self):
        self._generate_grid()

    def get_square(self, x, y, lookup) -> Square:
        if lookup == self.ROWCOLS:
            raise NotImplementedError()
        elif lookup == self.XY:
            return self.get_square_xy(x, y)
        else:
            raise ValueError(f'Unkown lookup {lookup}')

    def get_square_xy(self, x, y) -> Square:
        col = int(x // self.bwidth)
        row = int(y // self.bheight)
        return self.grid[row][col]
