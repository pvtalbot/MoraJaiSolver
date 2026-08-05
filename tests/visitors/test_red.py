from morajai_solver.domain.MovementVisitors import RedVisitor
from morajai_solver.models.MoraBoard import (
    AbstractMoraBoard,
    BitmaskMoraBoard,
    DictMoraBoard,
)
from morajai_solver.domain.colors import MoraColor


def red_visitor(board: AbstractMoraBoard):
    board[1, 1] = MoraColor.WHITE
    board[1, 2] = MoraColor.BLACK
    board[1, 3] = MoraColor.YELLOW  # Ne doit pas bouger

    board[2, 2] = MoraColor.WHITE
    board[2, 3] = MoraColor.BLACK
    board[2, 1] = MoraColor.YELLOW  # Ne doit pas bouger

    board[3, 3] = MoraColor.WHITE
    board[3, 1] = MoraColor.BLACK
    board[3, 2] = MoraColor.YELLOW  # Ne doit pas bouger

    visitor = RedVisitor()
    board.accept(visitor, (1, 1))

    assert board[1, 1] == MoraColor.BLACK
    assert board[1, 2] == MoraColor.RED
    assert board[1, 3] == MoraColor.YELLOW

    assert board[2, 2] == MoraColor.BLACK
    assert board[2, 3] == MoraColor.RED
    assert board[2, 1] == MoraColor.YELLOW

    assert board[3, 3] == MoraColor.BLACK
    assert board[3, 1] == MoraColor.RED
    assert board[3, 2] == MoraColor.YELLOW


def test_red_visitor_dict():
    red_visitor(DictMoraBoard())


def test_red_visitor_bitmask():
    red_visitor(BitmaskMoraBoard())
