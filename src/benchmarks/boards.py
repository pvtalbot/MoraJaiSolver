from morajai_solver.models.MoraBoard import Coord, DictMoraBoard
from morajai_solver.models.MoraColor import MoraColor

STORED_BOARDS = {
    "Board 1": {
        "colors": {
            (1, 1): MoraColor.GREEN,
            (1, 2): MoraColor.WHITE,
            (1, 3): MoraColor.WHITE,
            (2, 1): MoraColor.BLACK,
            (2, 2): MoraColor.WHITE,
            (2, 3): MoraColor.BLACK,
            (3, 1): MoraColor.BLUE,
            (3, 2): MoraColor.WHITE,
            (3, 3): MoraColor.BLUE,
        },
        "targets": {
            (1, 1): MoraColor.BLUE,
            (1, 3): MoraColor.BLUE,
            (3, 3): MoraColor.BLUE,
            (3, 1): MoraColor.BLUE,
        },
    },
    "Board 2": {
        "colors": {
            (1, 1): MoraColor.PINK,
            (1, 2): MoraColor.BLUE,
            (1, 3): MoraColor.BLUE,
            (2, 1): MoraColor.BLUE,
            (2, 2): MoraColor.BLUE,
            (2, 3): MoraColor.PURPLE,
            (3, 1): MoraColor.GREEN,
            (3, 2): MoraColor.GREY,
            (3, 3): MoraColor.PINK,
        },
        "targets": {
            (1, 1): MoraColor.BLUE,
            (1, 3): MoraColor.BLUE,
            (3, 3): MoraColor.BLUE,
            (3, 1): MoraColor.BLUE,
        },
    },
    "Board 3": {
        "colors": {
            (1, 1): MoraColor.ORANGE,
            (1, 2): MoraColor.GREY,
            (1, 3): MoraColor.RED,
            (2, 1): MoraColor.WHITE,
            (2, 2): MoraColor.GREEN,
            (2, 3): MoraColor.PURPLE,
            (3, 1): MoraColor.ORANGE,
            (3, 2): MoraColor.GREEN,
            (3, 3): MoraColor.ORANGE,
        },
        "targets": {
            (1, 1): MoraColor.RED,
            (1, 3): MoraColor.RED,
            (3, 3): MoraColor.RED,
            (3, 1): MoraColor.RED,
        },
    },
    "Board 4": {
        "colors": {
            (1, 1): MoraColor.RED,
            (1, 2): MoraColor.PINK,
            (1, 3): MoraColor.ORANGE,
            (2, 1): MoraColor.WHITE,
            (2, 2): MoraColor.YELLOW,
            (2, 3): MoraColor.WHITE,
            (3, 1): MoraColor.ORANGE,
            (3, 2): MoraColor.RED,
            (3, 3): MoraColor.RED,
        },
        "targets": {
            (1, 1): MoraColor.GREY,
            (1, 3): MoraColor.GREY,
            (3, 3): MoraColor.GREY,
            (3, 1): MoraColor.GREY,
        },
    },
    "Board 5": {
        "colors": {
            (1, 1): MoraColor.ORANGE,
            (1, 2): MoraColor.ORANGE,
            (1, 3): MoraColor.PINK,
            (2, 1): MoraColor.BLUE,
            (2, 2): MoraColor.WHITE,
            (2, 3): MoraColor.WHITE,
            (3, 1): MoraColor.PINK,
            (3, 2): MoraColor.GREEN,
            (3, 3): MoraColor.PURPLE,
        },
        "targets": {
            (1, 1): MoraColor.PINK,
            (1, 3): MoraColor.PINK,
            (3, 3): MoraColor.PINK,
            (3, 1): MoraColor.PINK,
        },
    },
}


def get_board(params: dict[str, dict[Coord, MoraColor]]):
    board = DictMoraBoard()
    for k, v in params["colors"].items():
        board[k] = v
    for k, v in params["targets"].items():
        board.set_target(*k, v)

    return board


PRESET_BOARDS = [(k, get_board(STORED_BOARDS[k])) for k in STORED_BOARDS]
