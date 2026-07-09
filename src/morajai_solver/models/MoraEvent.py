from enum import Enum


class MoraEvent(Enum):
    # Configuration
    MODE_CHANGED = "mode_changed"
    TILE_COLOR_CHANGED = "tile_color_changed"
    TARGET_COLOR_CHANGED = "target_color_changed"
    RANDOMIZE_BOARD = "randomize_board"

    # Jeu
    TILE_CLICKED = "tile_clicked"
    BOARD_UPDATED = "board_updated"
    RESET_SAVE = "reset_save"

    # Solveur
    SOLUTION_FOUND = "solution_found"
    VICTORY_ACHIEVED = "victory_achieved"
