from morajai_solver.domain.colors import MoraColor
from morajai_solver.domain.movement_strategies import OrangeStrategy
from morajai_solver.models.mora_board import (
    MoraBoard,
)


def test_strict_majority():
    """Majorité stricte (2 BLACK, 1 WHITE) -> La case devient BLACK."""
    board = MoraBoard()
    board[2, 2] = MoraColor.ORANGE

    # Voisins orthogonaux valides de (2,2)
    board[1, 2] = MoraColor.BLACK
    board[3, 2] = MoraColor.BLACK
    board[2, 3] = MoraColor.WHITE
    board[2, 1] = MoraColor.GREY

    strategy = OrangeStrategy()
    board.accept(strategy, (2, 2))

    assert board[2, 2] == MoraColor.BLACK


def test_equality_does_nothing():
    """Égalité parfaite (2 BLACK, 2 WHITE) -> Pas de majorité, la case reste inchangée."""
    board = MoraBoard()
    board[2, 2] = MoraColor.ORANGE

    # Voisins orthogonaux de (2,2) en égalité 2 vs 2
    board[1, 2] = MoraColor.BLACK
    board[3, 2] = MoraColor.BLACK
    board[2, 3] = MoraColor.WHITE
    board[2, 1] = MoraColor.WHITE

    strategy = OrangeStrategy()
    board.accept(strategy, (2, 2))

    # Aucune couleur ne l'emporte, la case doit rester ORANGE
    assert board[2, 2] == MoraColor.ORANGE
