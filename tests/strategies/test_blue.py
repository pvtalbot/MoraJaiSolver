from morajai_solver.core.movement_strategies import BlueStrategy
from morajai_solver.models.MoraBoard import BitmaskMoraBoard
from morajai_solver.models.MoraColor import MoraColor


def test_blue_strategy_with_yellow_center():
    """Le centre est jaune, cliquer sur une case bleue déclenche le mouvement jaune (monte)."""
    board = BitmaskMoraBoard(0)
    board[2, 2] = MoraColor.YELLOW  # Centre jaune
    board[3, 2] = MoraColor.BLUE    # Case cliquée

    strategy = BlueStrategy()
    strategy.execute(3, 2, board)

    # La stratégie jaune s'est exécutée sur (3,2) : l'élément monte en (2,2)
    assert board[2, 2] == MoraColor.BLUE
    assert board[3, 2] == MoraColor.YELLOW


def test_blue_strategy_with_blue_center():
    """Le centre est bleu, la stratégie doit s'arrêter pour éviter une boucle infinie."""
    board = BitmaskMoraBoard(0)
    board[2, 2] = MoraColor.BLUE  # Centre bleu
    board[3, 2] = MoraColor.BLUE  # Case cliquée

    strategy = BlueStrategy()
    strategy.execute(3, 2, board)

    # Rien ne doit changer sur le plateau
    assert board[2, 2] == MoraColor.BLUE
    assert board[3, 2] == MoraColor.BLUE


def test_blue_strategy_with_orange_center():
    """Le centre est orange, cliquer sur une case bleue déclenche la majorité orange."""
    board = BitmaskMoraBoard(0)
    board[2, 2] = MoraColor.ORANGE  # Centre orange

    # On clique sur (1,2) qui est bleue
    board[1, 2] = MoraColor.BLUE
    # On donne des voisins orthogonaux à (1,2) majoritairement BLACK : (1,1) et (1,3)
    board[1, 1] = MoraColor.BLACK
    board[1, 3] = MoraColor.BLACK
    board[2, 2] = MoraColor.ORANGE  # (Le centre reste orange pour le test)

    strategy = BlueStrategy()
    strategy.execute(1, 2, board)

    # La stratégie orange s'est exécutée sur (1,2) -> elle prend la majorité (BLACK)
    assert board[1, 2] == MoraColor.BLACK