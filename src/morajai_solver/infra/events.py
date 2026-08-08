from enum import Enum


class MoraEvent(Enum):
    # Configuration
    MODE_CHANGED = "mode_changed"
    BOARD_READY = "board_ready"
    RANDOMIZE_BOARD = "randomize_board"
    SOLUTION_INVALIDATED = "solution_invalidated"

    # Jeu
    TILE_CLICKED = "tile_clicked"
    BOARD_UPDATED = "board_updated"
    RESET_SAVE = "reset_save"

    # Solveur
    SOLVER_START = "solver_start"
    SOLUTION_FOUND = "solution_found"
    VICTORY_ACHIEVED = "victory_achieved"

    # LOAD/SAVE
    LOAD_BOARD_REQUESTED = "load_board_requested"
    LIST_LEVELS_REQUESTED = "list_levels_requested"
    LIST_LEVELS = "list_levels"
    SAVE_BOARD_REQUESTED = "save_board_requested"
