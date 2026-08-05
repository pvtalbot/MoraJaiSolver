from morajai_solver.core.MovementVisitors import OrangeVisitor
from morajai_solver.models.MoraBoard import (
    AbstractMoraBoard,
    BitmaskMoraBoard,
    DictMoraBoard,
)
from morajai_solver.models.MoraColor import MoraColor


def strict_majority(board: AbstractMoraBoard):
    """Majorité stricte (2 BLACK, 1 WHITE) -> La case devient BLACK."""
    board[2, 2] = MoraColor.ORANGE

    # Voisins orthogonaux valides de (2,2)
    board[1, 2] = MoraColor.BLACK
    board[3, 2] = MoraColor.BLACK
    board[2, 3] = MoraColor.WHITE
    board[2, 1] = MoraColor.GREY

    visitor = OrangeVisitor()
    board.accept(visitor, (2, 2))

    assert board[2, 2] == MoraColor.BLACK


def test_strict_majority_dict():
    strict_majority(DictMoraBoard())


def test_strict_majority_bitmask():
    strict_majority(BitmaskMoraBoard())


def equality_does_nothing(board: AbstractMoraBoard):
    """Égalité parfaite (2 BLACK, 2 WHITE) -> Pas de majorité, la case reste inchangée."""
    board[2, 2] = MoraColor.ORANGE

    # Voisins orthogonaux de (2,2) en égalité 2 vs 2
    board[1, 2] = MoraColor.BLACK
    board[3, 2] = MoraColor.BLACK
    board[2, 3] = MoraColor.WHITE
    board[2, 1] = MoraColor.WHITE

    visitor = OrangeVisitor()
    board.accept(visitor, (2, 2))

    # Aucune couleur ne l'emporte, la case doit rester ORANGE
    assert board[2, 2] == MoraColor.ORANGE


def test_equality_does_nothing_dict():
    equality_does_nothing(DictMoraBoard())


def test_equality_does_nothing_bitmask():
    equality_does_nothing(BitmaskMoraBoard())
