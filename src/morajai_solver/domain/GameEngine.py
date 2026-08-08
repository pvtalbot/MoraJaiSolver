import random
import logging
import threading
from morajai_solver.domain.MovementVisitors import COLOR_VISITORS
from morajai_solver.domain.Solver import MoraSolver
from morajai_solver.domain.colors import MoraColor
from morajai_solver.infra.EventDispatcher import EventDispatcher
from morajai_solver.infra.repositories.json_board_repository import JsonBoardRepository
from morajai_solver.models.MoraBoard import AbstractMoraBoard, DictMoraBoard
from morajai_solver.infra.events import MoraEvent
from morajai_solver.models.types import Coord
from morajai_solver.ui.game_modes import MoraMode

logger = logging.getLogger(__name__)


class GameEngine:
    def __init__(self, ui_bus: EventDispatcher):
        self.ui_bus = ui_bus
        self.domain_bus = EventDispatcher()
        self._board = DictMoraBoard()
        for r in range(1, 4):
            for c in range(1, 4):
                self._board[r, c] = MoraColor.GREY
        for target in ((1, 1), (1, 3), (3, 1), (3, 3)):
            r, c = target
            self._board.set_target(r, c, MoraColor.GREY)

        self._repository = JsonBoardRepository()

        self._subscribe_events()

    def _subscribe_events(self):
        self.ui_bus.subscribe(MoraEvent.BOARD_READY, self._on_board_ready)
        self.ui_bus.subscribe(MoraEvent.TILE_CLICKED, self._on_tile_clicked)
        self.ui_bus.subscribe(MoraEvent.RANDOMIZE_BOARD, self._on_randomize_board)

        self.ui_bus.subscribe(MoraEvent.MODE_CHANGED, self._on_mode_changed)
        self.ui_bus.subscribe(MoraEvent.RESET_SAVE, self._on_reset_save)

        self.ui_bus.subscribe(MoraEvent.SOLVER_START, self._on_solver_start)

        self.ui_bus.subscribe(MoraEvent.SAVE_BOARD_REQUESTED, self._on_save_requested)
        self.ui_bus.subscribe(
            MoraEvent.LIST_LEVELS_REQUESTED, self._on_list_levels_requested
        )

        logger.debug("Moteur de jeu initialisé.")

    def _on_mode_changed(self, new_mode: MoraMode):
        if new_mode != MoraMode.PLAY:
            return
        self.saved_board_state = self._board.data.copy()

    def _on_reset_save(self):
        if not self.saved_board_state:
            return

        self._board.data = self.saved_board_state.copy()
        self.ui_bus.emit(MoraEvent.BOARD_UPDATED, board_state=self._board.data.copy())

    def _on_board_ready(
        self, board_state: dict[Coord, MoraColor], targets: dict[Coord, MoraColor]
    ):
        for k, v in board_state.items():
            self._board[k] = v
        for k, v in targets.items():
            self._board.set_target(*k, v)

    def _on_tile_clicked(self, r: int, c: int):
        color = self._board[r, c]
        visitor = COLOR_VISITORS[color]
        self._board.accept(visitor, (r, c))
        self.ui_bus.emit(MoraEvent.BOARD_UPDATED, board_state=self._board.data.copy())

        if self.check_victory():
            self.ui_bus.emit(MoraEvent.VICTORY_ACHIEVED)

    def _on_randomize_board(self):
        available_colors = list(MoraColor)

        for r in range(1, 4):
            for c in range(1, 4):
                random_color = random.choice(available_colors)
                self._board[(r, c)] = random_color

        self.ui_bus.emit(MoraEvent.BOARD_UPDATED, board_state=self._board.data.copy())

    def _on_solver_start(self):
        threading.Thread(target=self._run_solver_async, daemon=True).start()

    def _run_solver_async(self):
        solver = MoraSolver(self._board)
        result = solver.solve()

        self.ui_bus.emit(MoraEvent.SOLUTION_FOUND, steps=result)

    def check_victory(self, board: AbstractMoraBoard | None = None):
        if board:
            return board.check_victory()

        return self._board.check_victory()

    def _on_save_requested(self, board_id: str):
        try:
            saved_path = self._repository.save(
                board_id, self._board.get_bitmask_board()
            )
            logger.info(f"Niveau {saved_path} sauvegardé")
        except PermissionError:
            logger.error("Impossible de sauvegarder : mode dev inactif.")
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde : {e}")

    def _on_list_levels_requested(self):
        levels = self._repository.list_available_boards()
        self.ui_bus.emit(MoraEvent.LIST_LEVELS, levels=levels)
