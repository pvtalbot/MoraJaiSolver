# tests/test_green.py
from morajai_solver.core.MovementVisitors import GreenVisitor
from morajai_solver.models.MoraBoard import (
    AbstractMoraBoard,
    BitmaskMoraBoard,
    DictMoraBoard,
)
from morajai_solver.models.MoraColor import MoraColor


def swaps_opposite(board: AbstractMoraBoard):
    board[1, 1] = MoraColor.GREEN
    board[3, 3] = MoraColor.BLACK  # L'opposé de (1, 1)

    visitor = GreenVisitor()
    board.accept(visitor, (1, 1))

    assert board[1, 1] == MoraColor.BLACK
    assert board[3, 3] == MoraColor.GREEN


def test_swaps_opposite_dict():
    swaps_opposite(DictMoraBoard())


def test_swaps_opposite_bitmask():
    swaps_opposite(BitmaskMoraBoard())


def center_does_nothing(board: AbstractMoraBoard):
    board[2, 2] = MoraColor.GREEN

    visitor = GreenVisitor()
    board.accept(visitor, (2, 2))

    assert board[2, 2] == MoraColor.GREEN


def test_center_does_nothing_dict():
    center_does_nothing(DictMoraBoard())


def test_center_does_nothing_bitmask():
    center_does_nothing(BitmaskMoraBoard())
