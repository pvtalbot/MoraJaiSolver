from morajai_solver.core.movement_strategies import RedStrategy
from morajai_solver.models.MoraBoard import BitmaskMoraBoard
from morajai_solver.models.MoraColor import MoraColor

def test_red_strategy_evolves_colors():
    board = BitmaskMoraBoard(0)
    board[1, 1] = MoraColor.WHITE
    board[1, 2] = MoraColor.BLACK
    board[2, 2] = MoraColor.YELLOW  # Ne doit pas bouger

    strategy = RedStrategy()
    strategy.execute(1, 1, board)

    assert board[1, 1] == MoraColor.BLACK
    assert board[1, 2] == MoraColor.RED
    assert board[2, 2] == MoraColor.YELLOW