import logging
import threading

from morajai_solver.domain.board_manager import BoardManager
from morajai_solver.domain.solver import MoraSolver
from morajai_solver.infra.event_dispatcher import EventDispatcher
from morajai_solver.infra.events import (
    BoardLoadedEvent,
    JumpToStepCommand,
    ListLevelsEvent,
    ListLevelsQuery,
    LoadLevelCommand,
    MoveEvaluatedEvent,
    PlayTileCommand,
    RandomizeBoardCommand,
    RegisterBoardCommand,
    SaveLevelCommand,
    SolutionFoundEvent,
    StartSolverCommand,
    StepUpdatedEvent,
    VictoryAchievedEvent,
)
from morajai_solver.infra.repositories.json_board_repository import JsonBoardRepository

logger = logging.getLogger(__name__)


class GameEngine:
    def __init__(self, ui_bus: EventDispatcher):
        self.ui_bus = ui_bus
        self.board_manager = BoardManager()
        self._repository = JsonBoardRepository()

        self._subscribe_events()

    def _subscribe_events(self):
        self.ui_bus.subscribe(RegisterBoardCommand, self._on_register_board)
        self.ui_bus.subscribe(PlayTileCommand, self._on_play_tile)
        self.ui_bus.subscribe(RandomizeBoardCommand, self._on_randomize_board)
        self.ui_bus.subscribe(JumpToStepCommand, self._on_jump_to_step)
        self.ui_bus.subscribe(StartSolverCommand, self._on_solver_start)
        self.ui_bus.subscribe(SaveLevelCommand, self._on_save_level)
        self.ui_bus.subscribe(ListLevelsQuery, self._on_list_levels_requested)
        self.ui_bus.subscribe(LoadLevelCommand, self._on_load_level)

        logger.debug("Moteur de jeu initialisé.")

    def emit_new_board_loaded(self):
        board = self.board_manager.get_state_as_dict()
        targets = self.board_manager.get_targets_as_dict()
        self.ui_bus.emit(BoardLoadedEvent(board=board, targets=targets))

    def _on_jump_to_step(self, command: JumpToStepCommand):
        victory = self.board_manager.force_move(command.step)

        self.ui_bus.emit(
            StepUpdatedEvent(
                board=self.board_manager.get_state_as_dict(),
                current_index=self.board_manager.index,
            )
        )

        if victory:
            self.ui_bus.emit(VictoryAchievedEvent())

    def _on_register_board(self, event: RegisterBoardCommand):
        self.board_manager.load_state_from_dict(event.board, event.targets)

    def _on_play_tile(self, event: PlayTileCommand):
        victory = self.board_manager.play_move(event.position)
        self.ui_bus.emit(
            MoveEvaluatedEvent(
                board=self.board_manager.get_state_as_dict(), last_move=event.position
            )
        )

        if victory:
            self.ui_bus.emit(VictoryAchievedEvent())

    def _on_randomize_board(self, _):
        self.board_manager.randomize()
        self.board_manager.reset()
        self.emit_new_board_loaded()

    def _on_solver_start(self, _):
        threading.Thread(target=self._run_solver, daemon=True).start()

    def _run_solver(self):
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

        self._on_list_levels_requested(ListLevelsQuery())

    def _on_list_levels_requested(self, _):
        levels = self._repository.list_available_boards()
        self.ui_bus.emit(ListLevelsEvent(levels=levels))

    def _on_load_level(self, command: LoadLevelCommand):
        board = self._repository.get(command.id)

        if board is None:
            return

        self.board_manager.board.data = board.data
        self.board_manager.board.target_state = board.target_state
        self.emit_new_board_loaded()
