from plat.core.states import State
from plat.components.player import ArrowComponent, Player
from plat.components.grid import GridLineComponent, GridSizeComponent


class GameState(State):
    COMPONENTS = [
        Player,
    ]


class EditState(State):
    COMPONENTS = [
        GridLineComponent,
        GridSizeComponent,
        ArrowComponent,
    ]
