from plat.core.states import State
from plat.components.player import ArrowComponent, Player
from plat.components.grid import GridLineComponent, GridSizeComponent
from plat.core.components import SpriteGroup

class GameState(State):
    COMPONENTS = [
        Player,
    ]

    def start(self):
    	self.reset_components()
    	

class EditState(State):
    COMPONENTS = [
        GridLineComponent,
        GridSizeComponent,
        ArrowComponent,
    ]
