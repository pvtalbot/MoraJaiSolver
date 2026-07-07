from morajai_solver.event_dispatcher import EventDispatcher, SingletonMeta
from morajai_solver.components.MoraButton import MoraColor
from morajai_solver.logger import get_logger
from logging import DEBUG

logger = get_logger(DEBUG, __name__)

class GameEngine(metaclass=SingletonMeta):
    def __init__(self):
        self.dispatcher = EventDispatcher()

        self.board_state = {}
        self.dispatcher.subscribe('tile_clicked', self._on_tile_clicked)
        self.dispatcher.subscribe('tile_color_changed', self._on_tile_color_changed)

        logger.debug('Moteur de jeu initialisé.')

    def _on_tile_color_changed(self, r: int, c: int, color: MoraColor):
        self.board_state[(r, c)] = color

    def _on_tile_clicked(self, r: int, c: int, color: MoraColor):
        if color == MoraColor.YELLOW:
            other_row = r - 1
            other_col = c

            if (other_row, other_col) not in self.board_state:
                return

            other_color = self.board_state[(other_row, other_col)]
            self.dispatcher.emit('update_tile_color', r=other_row, c=other_col, color=MoraColor.YELLOW)
            self.dispatcher.emit('update_tile_color', r=r, c=c, color=other_color)

                