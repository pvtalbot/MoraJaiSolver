from morajai_solver.domain.colors import MoraColor
from morajai_solver.models.mora_board import (
    MoraBoard,
)


def test_check_victory():
    # Configuration des objectifs aux 4 coins (positions 0 et 4)
    board = MoraBoard()
    board.set_target((1, 1), MoraColor.YELLOW)
    board.set_target((1, 3), MoraColor.BLUE)
    board.set_target((3, 3), MoraColor.RED)
    board.set_target((3, 1), MoraColor.GREEN)

    # ÉCHEC : Le plateau du moteur est entièrement gris au départ
    for r in range(1, 4):
        for c in range(1, 4):
            board[(r, c)] = MoraColor.GREY
    assert board.check_victory() is False

    # SUCCÈS : On place les bonnes couleurs aux correspondances de la grille interne
    board[(1, 1)] = MoraColor.YELLOW
    board[(1, 3)] = MoraColor.BLUE
    board[(3, 3)] = MoraColor.RED
    board[(3, 1)] = MoraColor.GREEN

    assert board.check_victory() is True
