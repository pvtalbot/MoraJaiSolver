# tests/test_white.py
from morajai_solver.core.movement_strategies import WhiteStrategy
from morajai_solver.models.MoraBoard import BitmaskMoraBoard
from morajai_solver.models.MoraColor import MoraColor


def test_white_strategy_toggles_grey():
    board = BitmaskMoraBoard(0)
    # On remplit tout en WHITE pour le test
    for r in range(1, 4):
        for c in range(1, 4):
            board[r, c] = MoraColor.WHITE

    # Sauf le voisin du dessus qu'on met en GREY
    board[1, 2] = MoraColor.GREY

    strategy = WhiteStrategy()
    # On clique sur (2, 2) qui est WHITE
    strategy.execute(2, 2, board)

    # (2,2) et ses voisins orthogonaux qui étaient WHITE doivent devenir GREY
    assert board[2, 2] == MoraColor.GREY
    assert board[2, 3] == MoraColor.GREY  # Voisin de droite (était WHITE -> GREY)

    # Le voisin du dessus (1,2) qui était GREY doit s'inverser et devenir WHITE !
    assert board[1, 2] == MoraColor.WHITE


def test_white_strategy_on_corner_ignores_outside():
    board = BitmaskMoraBoard(0)
    # On clique dans le coin supérieur gauche (1, 1) qui est WHITE
    board[1, 1] = MoraColor.WHITE
    board[1, 2] = MoraColor.WHITE  # Voisin de droite
    board[2, 1] = MoraColor.WHITE  # Voisin du dessous

    strategy = WhiteStrategy()
    strategy.execute(1, 1, board)

    # Seuls (1,1), (1,2) et (2,1) doivent être devenus GREY.
    # Les positions virtuelles (0,1) ou (1,0) hors-limites n'ont pas dû planter.
    assert board[1, 1] == MoraColor.GREY
    assert board[1, 2] == MoraColor.GREY
    assert board[2, 1] == MoraColor.GREY
