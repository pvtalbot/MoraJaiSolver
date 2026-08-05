from morajai_solver.domain.MovementVisitors import BlackVisitor
from morajai_solver.models.MoraBoard import (
    AbstractMoraBoard,
    BitmaskMoraBoard,
    DictMoraBoard,
)
from morajai_solver.domain.colors import MoraColor


def shift_rows(board: AbstractMoraBoard, r: int):
    board[r, 1] = MoraColor.WHITE
    board[r, 2] = MoraColor.BLACK
    board[r, 3] = MoraColor.RED

    visitor = BlackVisitor()
    board.accept(visitor, (r, 2))

    assert board[r, 1] == MoraColor.RED
    assert board[r, 2] == MoraColor.WHITE
    assert board[r, 3] == MoraColor.BLACK


def test_black_visitor_on_dict_board():
    for r in range(1, 3):
        shift_rows(DictMoraBoard(), r)


def test_black_visitor_on_bitmask_board():
    for r in range(1, 3):
        shift_rows(BitmaskMoraBoard(), r)
