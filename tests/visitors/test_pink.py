from morajai_solver.domain.MovementVisitors import PinkVisitor
from morajai_solver.models.MoraBoard import (
    AbstractMoraBoard,
    BitmaskMoraBoard,
    DictMoraBoard,
)
from morajai_solver.domain.colors import MoraColor


def center_all_neighbors(board: AbstractMoraBoard):
    """Test au milieu (2,2) : les 8 voisins autour tournent d'un cran."""
    board[2, 2] = MoraColor.PINK

    board[1, 2] = MoraColor.WHITE
    board[1, 3] = MoraColor.BLACK
    board[2, 3] = MoraColor.RED
    board[3, 3] = MoraColor.YELLOW
    board[3, 2] = MoraColor.PURPLE
    board[3, 1] = MoraColor.GREEN
    board[2, 1] = MoraColor.ORANGE
    board[1, 1] = MoraColor.BLUE

    visitor = PinkVisitor()
    board.accept(visitor, (2, 2))

    # Vérification après décalage horaire d'un cran
    assert board[1, 2] == MoraColor.BLUE
    assert board[1, 3] == MoraColor.WHITE
    assert board[2, 3] == MoraColor.BLACK
    assert board[3, 3] == MoraColor.RED
    assert board[3, 2] == MoraColor.YELLOW
    assert board[3, 1] == MoraColor.PURPLE
    assert board[2, 1] == MoraColor.GREEN
    assert board[1, 1] == MoraColor.ORANGE


def test_center_all_neighbors_dict():
    center_all_neighbors(DictMoraBoard())


def test_center_all_neighbors_bitmask():
    center_all_neighbors(BitmaskMoraBoard())


def left_edge(board: AbstractMoraBoard):
    """Test sur un côté (2,1) : seuls 5 voisins sont valides et doivent tourner."""
    board[2, 1] = MoraColor.PINK

    board[1, 1] = MoraColor.WHITE
    board[1, 2] = MoraColor.BLACK
    board[2, 2] = MoraColor.RED
    board[3, 2] = MoraColor.YELLOW
    board[3, 1] = MoraColor.PURPLE

    visitor = PinkVisitor()
    board.accept(visitor, (2, 1))

    assert board[1, 1] == MoraColor.PURPLE
    assert board[1, 2] == MoraColor.WHITE
    assert board[2, 2] == MoraColor.BLACK
    assert board[3, 2] == MoraColor.RED
    assert board[3, 1] == MoraColor.YELLOW


def test_left_edge_dict():
    left_edge(DictMoraBoard())


def test_left_edge_bitmask():
    left_edge(BitmaskMoraBoard())


def top_right_corner(board: AbstractMoraBoard):
    """Test dans un angle (1,3) : seuls 3 voisins sont valides et doivent tourner."""
    board[1, 3] = MoraColor.PINK

    board[2, 3] = MoraColor.WHITE
    board[2, 2] = MoraColor.BLACK
    board[1, 2] = MoraColor.RED

    visitor = PinkVisitor()
    board.accept(visitor, (1, 3))

    # Après décalage circulaire des 3 éléments :
    assert board[2, 3] == MoraColor.RED
    assert board[2, 2] == MoraColor.WHITE
    assert board[1, 2] == MoraColor.BLACK


def test_top_right_corner_dict():
    top_right_corner(DictMoraBoard())


def test_top_right_corner_bitmask():
    top_right_corner(BitmaskMoraBoard())
