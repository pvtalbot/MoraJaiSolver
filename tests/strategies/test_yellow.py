from morajai_solver.domain.MovementStrategies import YellowStrategy
from morajai_solver.models.MoraBoard import (
    MoraBoard,
)
from morajai_solver.domain.colors import MoraColor


def test_moves_up():
    for r in (2, 3):
        for c in range(1, 4):
            board = MoraBoard()
            board[r, c] = MoraColor.YELLOW
            board[r - 1, c] = MoraColor.WHITE

            strategy = YellowStrategy()
            board.accept(strategy, (r, c))

            assert board[r - 1, c] == MoraColor.YELLOW
            assert board[r, c] == MoraColor.WHITE


def test_on_edge():
    for c in range(1, 4):
        board = MoraBoard()
        board[1, c] = MoraColor.YELLOW

        strategy = YellowStrategy()
        board.accept(strategy, (1, c))

        assert board[1, c] == MoraColor.YELLOW
