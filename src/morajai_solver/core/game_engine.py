import random, logging
from morajai_solver.event_dispatcher import EventDispatcher, SingletonMeta
from morajai_solver.components.MoraButton import MoraColor
from morajai_solver.core.movement_strategies import *

logger = logging.getLogger(__name__)

class GameEngine(metaclass=SingletonMeta):
    def __init__(self):
        self.dispatcher = EventDispatcher()

        self.board_state = {}
        self.target_state = {}

        self.dispatcher.subscribe('tile_clicked', self._on_tile_clicked)
        self.dispatcher.subscribe('tile_color_changed', self._on_tile_color_changed)
        self.dispatcher.subscribe('target_color_changed', self._on_target_color_changed)
        self.dispatcher.subscribe('randomize_board', self._on_randomize_board)

        logger.debug('Moteur de jeu initialisé.')

    def _on_tile_color_changed(self, r: int, c: int, color: MoraColor):
        self.board_state[(r, c)] = color

    def _on_target_color_changed(self, r: int, c: int, color: MoraColor):
        self.target_state[(r, c)] = color

    def _on_tile_clicked(self, r: int, c: int, color: MoraColor):
        strategy = STRATEGY_MAP.get(color)

        if not strategy:
            logger.warning("Aucune stratégie trouvée")
            return

        strategy.execute(r, c, self.board_state, self.dispatcher)

        if self.check_victory():
            self.dispatcher.emit('victory_achieved')

    def _on_randomize_board(self):
        available_colors = list(MoraColor)

        for r in range(1, 4):
            for c in range(1, 4):
                random_color = random.choice(available_colors)
                self.board_state[(r, c)] = random_color

        self.dispatcher.emit('board_updated', board_state=self.board_state)

    def check_victory(self, board = None):
        mapping = {
            (0, 0): (1, 1),
            (0, 4): (1, 3),
            (4, 4): (3, 3),
            (4, 0): (3, 1)
        }

        if board:
            return all([self.target_state[a] == board[b] for (a, b) in mapping.items()])

        return all([self.target_state[a] == self.board_state[b] for (a, b) in mapping.items()])
