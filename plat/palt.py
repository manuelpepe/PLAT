#!/usr/bin/env python3
import sys
import time
import pygame
import logging

from typing import List

from components import BaseComponent, ArrowComponent
from states import GameState, EditState, State
from grid import Grid, GridLineComponent, GridSizeComponent
from utils import *


pygame.init()
pygame.joystick.init()

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)

if len(sys.argv) > 1 and sys.argv[1] == 'v':
    logger.setLevel(logging.DEBUG)

FPS = 60


class Game:
    """ 
    Encapsulates basic game logic. 

    Has the grid of the level, screen and clock. Also the list of root components.
    """
    def __init__(self, width, height):
        self.height = height
        self.width = width
        self.screen = pygame.display.set_mode((width, height))
        self.font = pygame.font.SysFont("courier new", 20)
        self.components: List[Component] = []
        self.clock = pygame.time.Clock()
        self.running = False
        self.joystick = None
        self.joy()

        self.states = None
        self._cur_state = None

    @property
    def state(self) -> State:
        return self.states[self._cur_state]

    @state.setter
    def state(self, value):
        if isinstance(value, int) and value < len(self.states):
            self._cur_state = value
        else:
            raise ValueError(f'Unkown state {value}')

    def do_update(self):
        self.state.update()

    def do_event(self):
        while event := pygame.event.poll():
            if event.type == pygame.JOYAXISMOTION:
                continue

            logger.info(f'Handling {event}')
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == JOYBTN['Y']:
                    self.next_state()

            self.state.event(event)

    def do_draw(self):
        self.state.draw(self.screen)
        pygame.display.flip()

    def joy(self):
        joystick_count = pygame.joystick.get_count()
        if not joystick_count:
            return

        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()

    def set_states(self, states):
        self.states = states
        self.state = 0

    def next_state(self):
        self._cur_state = (self._cur_state + 1) % len(self.states)

    def run(self, states):
        self.set_states(states)
        logger.info('Starting')
        self.running = True
        self.joy()
        while self.running:
            self.clock.tick(FPS)
            self.do_event()
            self.do_update()
            self.do_draw()

g = Game(800, 800)

grid = Grid(g)
gl = GridLineComponent(g, grid=grid)
gs = GridSizeComponent(g, grid=grid)
arrow = ArrowComponent(g, grid=grid)

states = [
    EditState(g, children=[
        grid,
        gl,
        gs,
        arrow,
    ]),
    GameState(g, children=[
        grid,
        arrow,
    ])
]

g.run(states)