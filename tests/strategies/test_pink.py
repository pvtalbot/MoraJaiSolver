from morajai_solver.domain.movement_strategies import PinkStrategy
from morajai_solver.models.mora_board import (
    MoraBoard,
)
from morajai_solver.domain.colors import MoraColor


def test_center_all_neighbors():
    """Test au milieu (2,2) : les 8 voisins autour tournent d'un cran."""
    board = MoraBoard()
    board[2, 2] = MoraColor.PINK

    board[1, 2] = MoraColor.WHITE
    board[1, 3] = MoraColor.BLACK
    board[2, 3] = MoraColor.RED
    board[3, 3] = MoraColor.YELLOW
    board[3, 2] = MoraColor.PURPLE
    board[3, 1] = MoraColor.GREEN
    board[2, 1] = MoraColor.ORANGE
    board[1, 1] = MoraColor.BLUE

    strategy = PinkStrategy()
    board.accept(strategy, (2, 2))

    # Vérification après décalage horaire d'un cran
    assert board[1, 2] == MoraColor.BLUE
    assert board[1, 3] == MoraColor.WHITE
    assert board[2, 3] == MoraColor.BLACK
    assert board[3, 3] == MoraColor.RED
    assert board[3, 2] == MoraColor.YELLOW
    assert board[3, 1] == MoraColor.PURPLE
    assert board[2, 1] == MoraColor.GREEN
    assert board[1, 1] == MoraColor.ORANGE


def test_left_edge():
    """Test sur un côté (2,1) : seuls 5 voisins sont valides et doivent tourner."""
    board = MoraBoard()
    board[2, 1] = MoraColor.PINK

    board[1, 1] = MoraColor.WHITE
    board[1, 2] = MoraColor.BLACK
    board[2, 2] = MoraColor.RED
    board[3, 2] = MoraColor.YELLOW
    board[3, 1] = MoraColor.PURPLE

    strategy = PinkStrategy()
    board.accept(strategy, (2, 1))

    assert board[1, 1] == MoraColor.PURPLE
    assert board[1, 2] == MoraColor.WHITE
    assert board[2, 2] == MoraColor.BLACK
    assert board[3, 2] == MoraColor.RED
    assert board[3, 1] == MoraColor.YELLOW


def test_top_right_corner():
    """Test dans un angle (1,3) : seuls 3 voisins sont valides et doivent tourner."""
    board = MoraBoard()
    board[1, 3] = MoraColor.PINK

    board[2, 3] = MoraColor.WHITE
    board[2, 2] = MoraColor.BLACK
    board[1, 2] = MoraColor.RED

    strategy = PinkStrategy()
    board.accept(strategy, (1, 3))

    # Après décalage circulaire des 3 éléments :
    assert board[2, 3] == MoraColor.RED
    assert board[2, 2] == MoraColor.WHITE
    assert board[1, 2] == MoraColor.BLACK
