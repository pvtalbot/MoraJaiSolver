from morajai_solver.domain.MovementStrategies import PurpleStrategy
from morajai_solver.models.MoraBoard import (
    MoraBoard,
)
from morajai_solver.domain.colors import MoraColor


def test_moves_down():
    for r in (1, 2):
        for c in range(1, 4):
            board = MoraBoard()
            board[r, c] = MoraColor.PURPLE
            board[r + 1, c] = MoraColor.WHITE  # La case du dessous

            strategy = PurpleStrategy()
            board.accept(strategy, (r, c))

            # La couleur violette doit être descendue en (3, 2)
            assert board[r + 1, c] == MoraColor.PURPLE
            assert board[r, c] == MoraColor.WHITE


def test_bottom_edge():
    for c in range(1, 4):
        board = MoraBoard()
        board[3, c] = MoraColor.PURPLE

        strategy = PurpleStrategy()
        board.accept(strategy, (3, c))

        # Sur le bord inférieur, rien ne doit bouger
        assert board[3, c] == MoraColor.PURPLE
