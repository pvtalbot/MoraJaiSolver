# tests/test_green.py
from morajai_solver.core.movement_strategies import GreenStrategy
from morajai_solver.models.MoraBoard import BitmaskMoraBoard
from morajai_solver.models.MoraColor import MoraColor


def test_green_strategy_swaps_opposite():
    board = BitmaskMoraBoard(0)
    board[1, 1] = MoraColor.GREEN
    board[3, 3] = MoraColor.BLACK  # L'opposé de (1, 1)

    strategy = GreenStrategy()
    strategy.execute(1, 1, board)

    assert board[1, 1] == MoraColor.BLACK
    assert board[3, 3] == MoraColor.GREEN


def test_green_strategy_on_center_does_nothing():
    board = BitmaskMoraBoard(0)
    board[2, 2] = MoraColor.GREEN

    strategy = GreenStrategy()
    strategy.execute(2, 2, board)

    assert board[2, 2] == MoraColor.GREEN
