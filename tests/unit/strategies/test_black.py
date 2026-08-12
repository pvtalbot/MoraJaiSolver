from morajai_solver.domain.movement_strategies import BlackStrategy
from morajai_solver.models.mora_board import (
    MoraBoard,
)
from morajai_solver.domain.colors import MoraColor


def test_shift_rows():
    board = MoraBoard()
    for r in range(1, 3):
        board[r, 1] = MoraColor.WHITE
        board[r, 2] = MoraColor.BLACK
        board[r, 3] = MoraColor.RED

        strategy = BlackStrategy()
        board.accept(strategy, (r, 2))

        assert board[r, 1] == MoraColor.RED
        assert board[r, 2] == MoraColor.WHITE
        assert board[r, 3] == MoraColor.BLACK
