from morajai_solver.core.movement_strategies import PurpleStrategy
from morajai_solver.models.MoraBoard import BitmaskMoraBoard
from morajai_solver.models.MoraColor import MoraColor


def test_purple_strategy_moves_down():
    board = BitmaskMoraBoard(0)
    board[2, 2] = MoraColor.PURPLE
    board[3, 2] = MoraColor.WHITE  # La case du dessous

    strategy = PurpleStrategy()
    strategy.execute(2, 2, board)

    # La couleur violette doit être descendue en (3, 2)
    assert board[3, 2] == MoraColor.PURPLE
    assert board[2, 2] == MoraColor.WHITE


def test_purple_strategy_on_bottom_edge():
    board = BitmaskMoraBoard(0)
    board[3, 2] = MoraColor.PURPLE

    strategy = PurpleStrategy()
    strategy.execute(3, 2, board)

    # Sur le bord inférieur, rien ne doit bouger
    assert board[3, 2] == MoraColor.PURPLE
