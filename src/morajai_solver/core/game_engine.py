from morajai_solver.event_dispatcher import EventDispatcher, SingletonMeta
from morajai_solver.components.MoraButton import MoraColor
from morajai_solver.logger import get_logger
from morajai_solver.core.movement_strategies import *
from logging import DEBUG, WARNING

logger = get_logger(WARNING, __name__)

class GameEngine(metaclass=SingletonMeta):
    def __init__(self):
        self.dispatcher = EventDispatcher()

        self.board_state = {}
        self.dispatcher.subscribe('tile_clicked', self._on_tile_clicked)
        self.dispatcher.subscribe('tile_color_changed', self._on_tile_color_changed)

        self._strategies = {
            MoraColor.YELLOW: YellowStrategy(),
            MoraColor.PURPLE: PurpleStrategy(),
            MoraColor.BLACK: BlackStrategy(),
        }

        logger.debug('Moteur de jeu initialisé.')

    def _on_tile_color_changed(self, r: int, c: int, color: MoraColor):
        self.board_state[(r, c)] = color

    def _on_tile_clicked(self, r: int, c: int, color: MoraColor):
        strategy = self._strategies.get(color)

        if not strategy:
            logger.warning("Aucune stratégie trouvée")
            return

        strategy.execute(r, c, self.board_state, self.dispatcher)
