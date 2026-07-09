from morajai_solver.core.movement_strategies import OrangeStrategy
from morajai_solver.models.MoraBoard import BitmaskMoraBoard
from morajai_solver.models.MoraColor import MoraColor


def test_orange_strategy_takes_strict_majority():
    """Majorité stricte (2 BLACK, 1 WHITE) -> La case devient BLACK."""
    board = BitmaskMoraBoard(0)
    board[2, 2] = MoraColor.ORANGE
    
    # Voisins orthogonaux valides de (2,2)
    board[1, 2] = MoraColor.BLACK
    board[3, 2] = MoraColor.BLACK
    board[2, 3] = MoraColor.WHITE
    board[2, 1] = MoraColor.GREY   # Le gris par défaut (0) ne compte pas s'il est minoritaire

    strategy = OrangeStrategy()
    strategy.execute(2, 2, board)

    assert board[2, 2] == MoraColor.BLACK


def test_orange_strategy_with_equality_does_nothing():
    """Égalité parfaite (2 BLACK, 2 WHITE) -> Pas de majorité, la case reste inchangée."""
    board = BitmaskMoraBoard(0)
    board[2, 2] = MoraColor.ORANGE

    # Voisins orthogonaux de (2,2) en égalité 2 vs 2
    board[1, 2] = MoraColor.BLACK
    board[3, 2] = MoraColor.BLACK
    board[2, 3] = MoraColor.WHITE
    board[2, 1] = MoraColor.WHITE

    strategy = OrangeStrategy()
    strategy.execute(2, 2, board)

    # Aucune couleur ne l'emporte, la case doit rester ORANGE
    assert board[2, 2] == MoraColor.ORANGE