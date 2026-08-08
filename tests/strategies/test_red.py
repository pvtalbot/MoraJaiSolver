from morajai_solver.domain.MovementStrategies import RedStrategy
from morajai_solver.models.MoraBoard import (
    MoraBoard,
)
from morajai_solver.domain.colors import MoraColor


def test_red_strategy():
    board = MoraBoard()
    board[1, 1] = MoraColor.WHITE
    board[1, 2] = MoraColor.BLACK
    board[1, 3] = MoraColor.YELLOW  # Ne doit pas bouger

    board[2, 2] = MoraColor.WHITE
    board[2, 3] = MoraColor.BLACK
    board[2, 1] = MoraColor.YELLOW  # Ne doit pas bouger

    board[3, 3] = MoraColor.WHITE
    board[3, 1] = MoraColor.BLACK
    board[3, 2] = MoraColor.YELLOW  # Ne doit pas bouger

    strategy = RedStrategy()
    board.accept(strategy, (1, 1))

    assert board[1, 1] == MoraColor.BLACK
    assert board[1, 2] == MoraColor.RED
    assert board[1, 3] == MoraColor.YELLOW

    assert board[2, 2] == MoraColor.BLACK
    assert board[2, 3] == MoraColor.RED
    assert board[2, 1] == MoraColor.YELLOW

    assert board[3, 3] == MoraColor.BLACK
    assert board[3, 1] == MoraColor.RED
    assert board[3, 2] == MoraColor.YELLOW
