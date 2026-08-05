import random
import logging
import threading
from morajai_solver.core.MovementVisitors import COLOR_VISITORS
from morajai_solver.core.Solver import MoraSolver
from morajai_solver.event_dispatcher import EventDispatcher, SingletonMeta
from morajai_solver.components.MoraButton import MoraColor
from morajai_solver.models.MoraBoard import AbstractMoraBoard, DictMoraBoard
from morajai_solver.models.MoraEvent import MoraEvent
from morajai_solver.models.MoraMode import MoraMode

logger = logging.getLogger(__name__)


class GameEngine(metaclass=SingletonMeta):
    def __init__(self):
        self.dispatcher = EventDispatcher()
        self._board = DictMoraBoard({})

        self._subscribe_events()

    def _subscribe_events(self):
        self.dispatcher.subscribe(MoraEvent.TILE_CLICKED, self._on_tile_clicked)
        self.dispatcher.subscribe(
            MoraEvent.TILE_COLOR_CHANGED, self._on_tile_color_changed
        )
        self.dispatcher.subscribe(
            MoraEvent.TARGET_COLOR_CHANGED, self._on_target_color_changed
        )
        self.dispatcher.subscribe(MoraEvent.RANDOMIZE_BOARD, self._on_randomize_board)

        self.dispatcher.subscribe(MoraEvent.MODE_CHANGED, self._on_mode_changed)
        self.dispatcher.subscribe(MoraEvent.RESET_SAVE, self._on_reset_save)

        self.dispatcher.subscribe(MoraEvent.SOLVER_START, self._on_solver_start)

        logger.debug("Moteur de jeu initialisé.")

    def _on_mode_changed(self, new_mode: MoraMode):
        if new_mode != MoraMode.PLAY:
            return
        self.saved_board_state = self._board.data.copy()

    def _on_reset_save(self):
        if not self.saved_board_state:
            return

        self._board.data = self.saved_board_state.copy()
        self.dispatcher.emit(
            MoraEvent.BOARD_UPDATED, board_state=self._board.data.copy()
        )

    def _on_tile_color_changed(self, r: int, c: int, color: MoraColor):
        self._board[(r, c)] = color

    def _on_target_color_changed(self, r: int, c: int, color: MoraColor):
        self._board.set_target(r, c, color)

    def _on_tile_clicked(self, r: int, c: int, color: MoraColor):
        visitor = COLOR_VISITORS[color]
        self._board.accept(visitor, (r, c))

        if self.check_victory():
            self.dispatcher.emit(MoraEvent.VICTORY_ACHIEVED)

    def _on_randomize_board(self):
        available_colors = list(MoraColor)

        for r in range(1, 4):
            for c in range(1, 4):
                random_color = random.choice(available_colors)
                self._board[(r, c)] = random_color

        self.dispatcher.emit(
            MoraEvent.BOARD_UPDATED, board_state=self._board.data.copy()
        )

    def _on_solver_start(self):
        threading.Thread(target=self._run_solver_async, daemon=True).start()

    def _run_solver_async(self):
        solver = MoraSolver(self._board)
        result = solver.solve()

        self.dispatcher.emit(MoraEvent.SOLUTION_FOUND, steps=result)

    def check_victory(self, board: AbstractMoraBoard | None = None):
        if board:
            return board.check_victory()

        return self._board.check_victory()
