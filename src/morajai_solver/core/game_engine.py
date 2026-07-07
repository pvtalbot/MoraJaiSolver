import random, logging
from morajai_solver.event_dispatcher import EventDispatcher, SingletonMeta
from morajai_solver.components.MoraButton import MoraColor
from morajai_solver.core.movement_strategies import *

logger = logging.getLogger(__name__)

class GameEngine(metaclass=SingletonMeta):
    def __init__(self):
        self.dispatcher = EventDispatcher()

        self.board_state = {}
        self.dispatcher.subscribe('tile_clicked', self._on_tile_clicked)
        self.dispatcher.subscribe('tile_color_changed', self._on_tile_color_changed)
        self.dispatcher.subscribe('randomize_board', self._on_randomize_board)

        logger.debug('Moteur de jeu initialisé.')

    def _on_tile_color_changed(self, r: int, c: int, color: MoraColor):
        self.board_state[(r, c)] = color

    def _on_tile_clicked(self, r: int, c: int, color: MoraColor):
        strategy = STRATEGY_MAP.get(color)

        if not strategy:
            logger.warning("Aucune stratégie trouvée")
            return

        strategy.execute(r, c, self.board_state, self.dispatcher)

    def _on_randomize_board(self):
        available_colors = list(MoraColor)

        for r in range(1, 4):
            for c in range(1, 4):
                random_color = random.choice(available_colors)
                self.board_state[(r, c)] = random_color

        self.dispatcher.emit('board_updated', board_state=self.board_state)
