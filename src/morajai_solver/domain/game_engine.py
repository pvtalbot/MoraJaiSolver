import logging
import threading
from morajai_solver.domain.board_manager import BoardManager
from morajai_solver.domain.solver import MoraSolver
from morajai_solver.infra.event_dispatcher import EventDispatcher
from morajai_solver.infra.repositories.json_board_repository import JsonBoardRepository
from morajai_solver.infra.events import (
    SubmitBoardCommand,
    BoardUpdatedEvent,
    ListLevelsEvent,
    ListLevelsQuery,
    RandomizeBoardCommand,
    ResetGameCommand,
    SaveLevelCommand,
    SolutionFoundEvent,
    StartSolverCommand,
    PlayTileCommand,
    VictoryAchievedEvent,
)

logger = logging.getLogger(__name__)


class GameEngine:
    def __init__(self, ui_bus: EventDispatcher):
        self.ui_bus = ui_bus
        self.domain_bus = EventDispatcher()
        self.board_manager = BoardManager()
        self._repository = JsonBoardRepository()

        self._subscribe_events()

    def _subscribe_events(self):
        self.ui_bus.subscribe(SubmitBoardCommand, self._on_submit_board)
        self.ui_bus.subscribe(PlayTileCommand, self._on_play_tile)
        self.ui_bus.subscribe(RandomizeBoardCommand, self._on_randomize_board)
        self.ui_bus.subscribe(ResetGameCommand, self._on_reset_game)
        self.ui_bus.subscribe(StartSolverCommand, self._on_solver_start)
        self.ui_bus.subscribe(SaveLevelCommand, self._on_save_level)
        self.ui_bus.subscribe(ListLevelsQuery, self._on_list_levels_requested)

        logger.debug("Moteur de jeu initialisé.")

    def emit_board_updated(self):
        board = self.board_manager.get_state_as_dict()
        targets = self.board_manager.get_targets_as_dict()
        self.ui_bus.emit(BoardUpdatedEvent(board=board, targets=targets))

    def _on_reset_game(self):
        self.board_manager.reset()
        self.emit_board_updated()

    def _on_submit_board(self, event: SubmitBoardCommand):
        self.board_manager.load_state_from_dict(event.board, event.targets)

    def _on_play_tile(self, event: PlayTileCommand):
        victory = self.board_manager.play_move(event.position)
        self.emit_board_updated()

        if victory:
            self.ui_bus.emit(VictoryAchievedEvent())

    def _on_randomize_board(self):
        self.board_manager.randomize()
        self.emit_board_updated()

    def _on_solver_start(self):
        threading.Thread(target=self._run_solver_async, daemon=True).start()

    def _run_solver_async(self):
        solver = MoraSolver(self.board_manager.board)
        result = solver.solve()

        self.ui_bus.emit(SolutionFoundEvent(result=result))

    def _on_save_level(self, command: SaveLevelCommand):
        try:
            saved_path = self._repository.save(command.id, self.board_manager.board)
            logger.info(f"Niveau {saved_path} sauvegardé")
        except PermissionError:
            logger.error("Impossible de sauvegarder : mode dev inactif.")
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde : {e}")

    def _on_list_levels_requested(self):
        levels = self._repository.list_available_boards()
        self.ui_bus.emit(ListLevelsEvent(levels=levels))
