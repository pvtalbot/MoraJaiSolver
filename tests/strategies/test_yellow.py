from morajai_solver.core.movement_strategies import YellowStrategy
from morajai_solver.models.MoraBoard import BitmaskMoraBoard
from morajai_solver.models.MoraColor import MoraColor


def test_yellow_strategy_moves_up():
    board = BitmaskMoraBoard(0)
    board[2, 2] = MoraColor.YELLOW
    board[1, 2] = MoraColor.WHITE

    strategy = YellowStrategy()
    strategy.execute(2, 2, board)

    assert board[1, 2] == MoraColor.YELLOW
    assert board[2, 2] == MoraColor.WHITE


def test_yellow_strategy_on_edge():
    board = BitmaskMoraBoard(0)
    board[1, 2] = MoraColor.YELLOW

    strategy = YellowStrategy()
    strategy.execute(1, 2, board)

    assert board[1, 2] == MoraColor.YELLOW
