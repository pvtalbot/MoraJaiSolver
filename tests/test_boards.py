from morajai_solver.models.MoraBoard import BitmaskMoraBoard, DictMoraBoard
from morajai_solver.models.MoraColor import MoraColor


def test_dict_and_bitmask_consistency():
    intial_data = {
        (1, 1): MoraColor.YELLOW,
        (1, 2): MoraColor.BLACK,
        (1, 3): MoraColor.GREEN,
        (2, 1): MoraColor.WHITE,
        (2, 2): MoraColor.BLUE,
        (2, 3): MoraColor.PINK,
        (3, 1): MoraColor.RED,
        (3, 2): MoraColor.GREEN,
        (3, 3): MoraColor.ORANGE,
    }

    dict_board = DictMoraBoard(intial_data.copy())

    bitmask_board = BitmaskMoraBoard(0)
    for pos, color in intial_data.items():
        bitmask_board[pos] = color

    for r in range(1, 4):
        for c in range(1, 4):
            assert dict_board[r, c] == bitmask_board[r, c]

    dict_board.swap((1, 1), (1, 2))
    bitmask_board.swap((1, 1), (1, 2))

    assert dict_board[1, 1] == bitmask_board[1, 1] == MoraColor.BLACK
    assert dict_board[1, 2] == bitmask_board[1, 2] == MoraColor.YELLOW