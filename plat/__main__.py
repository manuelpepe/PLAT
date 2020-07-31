#!/usr/bin/env python3
import sys
import time
import pygame
import logging
import pathlib

from typing import List
from collections import namedtuple

from plat.core.grid import Grid
from plat.core.components import SpriteGroup, SpriteManager, AnimationManager
from plat.states import GameState, EditState, PauseState, State

from plat.core.utils import *
from plat.config import FPS, SPRITE_MAPS, ANIMATIONS


pygame.init()
pygame.joystick.init()

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)

if len(sys.argv) > 1 and sys.argv[1] == 'v':
    logger.setLevel(logging.DEBUG)


CurrentState = namedtuple("CurrentState", "name obj")


class Game:
    """ 
    Encapsulates basic game logic. 

    Has the grid of the level, screen and clock. Also the list of root components.
    """
    logger = logging.getLogger('Game')

    GAME = "game"
    PAUSE = "pause"
    EDIT = "edit"

    def __init__(self, width, height, sprites_dir, sprite_maps):
        self.height = height
        self.width = width
        self.screen = pygame.display.set_mode((width, height))
        self.font_size = 20
        self.font = pygame.font.SysFont("courier new", self.font_size)
        self.components: List[Component] = []
        self.clock = pygame.time.Clock()
        self.player = None
        self.joystick = None
        self.states = {}
        self.joy()

        self.sprites = SpriteManager(self, SPRITE_MAPS, sprites_dir)
        self.sprites.load()

        self.animate = AnimationManager(ANIMATIONS, self.sprites)

        self.running = False
        self.dt = None
        self._cur_state = None

    @property
    def state(self) -> State:
        return CurrentState(self._cur_state, self.states[self._cur_state])

    @state.setter
    def state(self, value):
        if value not in self.states.keys():
            raise ValueError(f'Unkown state {value}')
        self.logger.debug(f"changing from {self._cur_state} to {value}")
        if self._cur_state is not None:
            self.state.obj.end()
        self._cur_state = value
        self.state.obj.start()

    def do_update(self):
        self.state.obj.update()

    def do_event(self):
        while event := pygame.event.poll():
            if event.type == pygame.JOYAXISMOTION:
                continue

            self.logger.info(f'Handling {event}')
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == JOYBTN['Y']:
                    if self.state.name == self.EDIT:
                        self.states.get(self.GAME).reset_components()
                        self.state = self.GAME
                    elif self.state.name == self.GAME:
                        self.state = self.EDIT
                if event.button == JOYBTN['B']:
                    breakpoint()
                if event.button == JOYBTN['START']:
                    if self.state.name == self.PAUSE:
                        self.state = self.GAME
                    elif self.state.name == self.GAME:
                        self.state = self.PAUSE

            self.state.obj.event(event)

    def do_draw(self):
        self.state.obj.draw(self.screen)
        pygame.display.update()

    def joy(self):
        joystick_count = pygame.joystick.get_count()
        if not joystick_count:
            return

        self.joystick = pygame.joystick.Joystick(1)
        self.joystick.init()

    def run(self, start_state: str, states: list = None):
        self.logger.info('Starting')
        self.states = states
        self.state = start_state
        self.running = True
        self.joy()
        while self.running:
            self.dt = self.clock.tick(FPS) / 1000
            # print('====== New Frame ======')
            self.do_event()
            self.do_update()
            self.do_draw()
            


sprites_dir = pathlib.Path(__file__).parent.absolute() / 'sprites'
game = Game(800, 800, sprites_dir, SPRITE_MAPS)
grid = Grid(game)
states = {
    "edit": EditState(game, grid), 
    "game": GameState(game, grid),
    "pause": PauseState(game, grid)
}


print('GO')
game.run(start_state="edit", states=states)
print('END')
