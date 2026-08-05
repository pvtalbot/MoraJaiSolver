from morajai_solver.core.MovementVisitors import BlueVisitor
from morajai_solver.models.MoraBoard import (
    AbstractMoraBoard,
    BitmaskMoraBoard,
    DictMoraBoard,
)
from morajai_solver.models.MoraColor import MoraColor


def yellow_center(board: AbstractMoraBoard):
    board[2, 2] = MoraColor.YELLOW  # Centre jaune
    board[3, 2] = MoraColor.BLUE  # Case cliquée

    visitor = BlueVisitor()
    board.accept(visitor, (3, 2))

    # La stratégie jaune s'est exécutée sur (3,2) : l'élément monte en (2,2)
    assert board[2, 2] == MoraColor.BLUE
    assert board[3, 2] == MoraColor.YELLOW


def test_yellow_center_dict():
    yellow_center(DictMoraBoard())


def test_yellow_center_bitmask():
    yellow_center(BitmaskMoraBoard())


def blue_center(board: AbstractMoraBoard):
    board[2, 2] = MoraColor.BLUE  # Centre bleu
    board[3, 3] = MoraColor.BLUE  # Case cliquée

    visitor = BlueVisitor()
    board.accept(visitor, (3, 3))

    # Rien ne doit changer sur le plateau
    assert board[2, 2] == MoraColor.BLUE
    assert board[3, 3] == MoraColor.BLUE


def test_blue_center_dict():
    blue_center(DictMoraBoard())


def test_blue_center_bitmask():
    blue_center(BitmaskMoraBoard())


def orange_center(board: AbstractMoraBoard):
    """Le centre est orange, cliquer sur une case bleue déclenche la majorité orange."""
    board[2, 2] = MoraColor.ORANGE  # Centre orange

    # On clique sur (1,2) qui est bleue
    board[1, 2] = MoraColor.BLUE
    # On donne des voisins orthogonaux à (1,2) majoritairement BLACK : (1,1) et (1,3)
    board[1, 1] = MoraColor.BLACK
    board[1, 3] = MoraColor.BLACK

    visitor = BlueVisitor()
    board.accept(visitor, (1, 2))

    # La stratégie orange s'est exécutée sur (1,2) -> elle prend la majorité (BLACK)
    assert board[1, 2] == MoraColor.BLACK


def test_orange_center_dict():
    orange_center(DictMoraBoard())


def test_orange_center_bitmask():
    orange_center(BitmaskMoraBoard())
