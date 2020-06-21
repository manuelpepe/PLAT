from plat.core.states import State
from plat.components.player import ArrowComponent, Player
from plat.components.grid import GridLineComponent, GridSizeComponent
from plat.components.helper import PlayerStats
from plat.core.components import SpriteGroup

class GameState(State):
    COMPONENTS = [
        Player,
        PlayerStats
    ]

    def start(self):
    	self.reset_components()
    	self.game.player = [x for x in self.children][1]

class EditState(State):
    COMPONENTS = [
        GridLineComponent,
        GridSizeComponent,
        ArrowComponent,
        PlayerStats,
    ]

    def start(self):
    	self.game.player = [x for x in self.children][3]