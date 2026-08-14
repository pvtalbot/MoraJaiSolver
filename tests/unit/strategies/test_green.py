# tests/test_green.py
from morajai_solver.domain.colors import MoraColor
from morajai_solver.domain.movement_strategies import GreenStrategy
from morajai_solver.models.mora_board import (
    MoraBoard,
)


def test_swaps_opposite():
    board = MoraBoard()
    board[1, 1] = MoraColor.GREEN
    board[3, 3] = MoraColor.BLACK  # L'opposé de (1, 1)

    strategy = GreenStrategy()
    board.accept(strategy, (1, 1))

    assert board[1, 1] == MoraColor.BLACK
    assert board[3, 3] == MoraColor.GREEN


def test_center_does_nothing():
    board = MoraBoard()
    board[2, 2] = MoraColor.GREEN

    strategy = GreenStrategy()
    board.accept(strategy, (2, 2))

    assert board[2, 2] == MoraColor.GREEN
