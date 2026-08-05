from morajai_solver.core.MovementVisitors import PurpleVisitor
from morajai_solver.models.MoraBoard import (
    AbstractMoraBoard,
    BitmaskMoraBoard,
    DictMoraBoard,
)
from morajai_solver.models.MoraColor import MoraColor


def moves_down(board: AbstractMoraBoard, r, c):
    board = BitmaskMoraBoard()
    board[r, c] = MoraColor.PURPLE
    board[r + 1, c] = MoraColor.WHITE  # La case du dessous

    visitor = PurpleVisitor()
    board.accept(visitor, (r, c))

    # La couleur violette doit être descendue en (3, 2)
    assert board[r + 1, c] == MoraColor.PURPLE
    assert board[r, c] == MoraColor.WHITE


def test_moves_down_dict():
    for r in (1, 2):
        for c in range(1, 4):
            moves_down(DictMoraBoard(), r, c)


def test_moves_down_bitmask():
    for r in (1, 2):
        for c in range(1, 4):
            moves_down(BitmaskMoraBoard(), r, c)


def bottom_edge(board: AbstractMoraBoard, c):
    board[3, c] = MoraColor.PURPLE

    visitor = PurpleVisitor()
    board.accept(visitor, (3, c))

    # Sur le bord inférieur, rien ne doit bouger
    assert board[3, c] == MoraColor.PURPLE


def test_bottom_edge_dict():
    for c in range(1, 4):
        bottom_edge(DictMoraBoard(), c)


def test_bottom_edge_bitmask():
    for c in range(1, 4):
        bottom_edge(BitmaskMoraBoard(), c)
