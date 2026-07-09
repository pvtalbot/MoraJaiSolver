from morajai_solver.core.game_engine import GameEngine
from morajai_solver.models.MoraBoard import BitmaskMoraBoard
from morajai_solver.models.MoraColor import MoraColor


def test_check_victory_with_internal_board_state():
    """Vérifie check_victory en mode jeu standard (utilise engine.board_state)."""
    engine = GameEngine()

    # Configuration des objectifs aux 4 coins (positions 0 et 4)
    engine.target_state = {
        (0, 0): MoraColor.YELLOW,
        (0, 4): MoraColor.BLUE,
        (4, 4): MoraColor.RED,
        (4, 0): MoraColor.GREEN,
    }

    # ÉCHEC : Le plateau du moteur est entièrement gris au départ
    engine.board_state = {
        (r, c): MoraColor.GREY for r in range(1, 4) for c in range(1, 4)
    }
    assert engine.check_victory() is False

    # SUCCÈS : On place les bonnes couleurs aux correspondances de la grille interne
    # Le mapping associe : (0,0)->(1,1), (0,4)->(1,3), (4,4)->(3,3), (4,0)->(3,1)
    engine.board_state[(1, 1)] = MoraColor.YELLOW
    engine.board_state[(1, 3)] = MoraColor.BLUE
    engine.board_state[(3, 3)] = MoraColor.RED
    engine.board_state[(3, 1)] = MoraColor.GREEN

    assert engine.check_victory() is True


def test_check_victory_with_external_simulated_board():
    """Vérifie check_victory en mode solveur (reçoit un BitmaskMoraBoard en argument)."""
    engine = GameEngine()

    # Configuration des objectifs
    engine.target_state = {
        (0, 0): MoraColor.YELLOW,
        (0, 4): MoraColor.BLUE,
        (4, 4): MoraColor.RED,
        (4, 0): MoraColor.GREEN,
    }

    # On s'assure que la grille interne du moteur ne gagne pas (Gris partout)
    engine.board_state = {
        (r, c): MoraColor.GREY for r in range(1, 4) for c in range(1, 4)
    }

    # On crée un objet BitmaskMoraBoard indépendant qui contient la combinaison gagnante
    simulated_board = BitmaskMoraBoard(0)
    simulated_board[1, 1] = MoraColor.YELLOW
    simulated_board[1, 3] = MoraColor.BLUE
    simulated_board[3, 3] = MoraColor.RED
    simulated_board[3, 1] = MoraColor.GREEN

    # Le moteur doit analyser l'argument externe grâce au Duck Typing
    assert engine.check_victory(simulated_board) is True