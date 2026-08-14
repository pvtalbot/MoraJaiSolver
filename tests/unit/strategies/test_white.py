# tests/test_white.py
from morajai_solver.domain.colors import MoraColor
from morajai_solver.domain.movement_strategies import WhiteStrategy
from morajai_solver.models.mora_board import (
    MoraBoard,
)


def test_toggles_grey():
    board = MoraBoard()
    # On remplit tout en WHITE pour le test
    for r in range(1, 4):
        for c in range(1, 4):
            board[r, c] = MoraColor.WHITE

    # Sauf le voisin du dessus qu'on met en GREY
    board[1, 2] = MoraColor.GREY

    strategy = WhiteStrategy()
    board.accept(strategy, (2, 2))

    assert board[2, 2] == MoraColor.GREY
    assert board[2, 3] == MoraColor.GREY  # Voisin de droite (était WHITE -> GREY)
    assert board[1, 2] == MoraColor.WHITE


def test_on_corner():
    # On clique dans le coin supérieur gauche (1, 1) qui est WHITE
    board = MoraBoard()
    board[1, 1] = MoraColor.WHITE
    board[1, 2] = MoraColor.WHITE  # Voisin de droite
    board[2, 1] = MoraColor.WHITE  # Voisin du dessous

    strategy = WhiteStrategy()
    board.accept(strategy, (1, 1))

    assert board[1, 1] == MoraColor.GREY
    assert board[1, 2] == MoraColor.GREY
    assert board[2, 1] == MoraColor.GREY
