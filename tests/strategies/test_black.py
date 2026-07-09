from morajai_solver.core.movement_strategies import BlackStrategy
from morajai_solver.models.MoraBoard import BitmaskMoraBoard
from morajai_solver.models.MoraColor import MoraColor


def test_black_strategy_shifts_row():
    board = BitmaskMoraBoard(0)
    board[1, 1] = MoraColor.WHITE
    board[1, 2] = MoraColor.BLACK
    board[1, 3] = MoraColor.RED

    strategy = BlackStrategy()
    strategy.execute(1, 2, board)

    assert board[1, 1] == MoraColor.RED
    assert board[1, 2] == MoraColor.WHITE
    assert board[1, 3] == MoraColor.BLACK
