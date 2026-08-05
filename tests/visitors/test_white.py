# tests/test_white.py
from morajai_solver.domain.MovementVisitors import WhiteVisitor
from morajai_solver.models.MoraBoard import (
    AbstractMoraBoard,
    BitmaskMoraBoard,
    DictMoraBoard,
)
from morajai_solver.domain.colors import MoraColor


def toggles_grey(board: AbstractMoraBoard):
    # On remplit tout en WHITE pour le test
    for r in range(1, 4):
        for c in range(1, 4):
            board[r, c] = MoraColor.WHITE

    # Sauf le voisin du dessus qu'on met en GREY
    board[1, 2] = MoraColor.GREY

    visitor = WhiteVisitor()
    board.accept(visitor, (2, 2))

    assert board[2, 2] == MoraColor.GREY
    assert board[2, 3] == MoraColor.GREY  # Voisin de droite (était WHITE -> GREY)
    assert board[1, 2] == MoraColor.WHITE


def test_toggles_grey_dict():
    toggles_grey(DictMoraBoard())


def test_toggles_grey_bitmask():
    toggles_grey(BitmaskMoraBoard())


def on_corner(board: AbstractMoraBoard):
    # On clique dans le coin supérieur gauche (1, 1) qui est WHITE
    board[1, 1] = MoraColor.WHITE
    board[1, 2] = MoraColor.WHITE  # Voisin de droite
    board[2, 1] = MoraColor.WHITE  # Voisin du dessous

    visitor = WhiteVisitor()
    board.accept(visitor, (1, 1))

    assert board[1, 1] == MoraColor.GREY
    assert board[1, 2] == MoraColor.GREY
    assert board[2, 1] == MoraColor.GREY


def test_on_corner_dict():
    on_corner(DictMoraBoard())


def test_on_corner_bitmask():
    on_corner(BitmaskMoraBoard())
