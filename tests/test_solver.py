# tests/test_solver.py
from morajai_solver.core.solver import MoraSolver
from morajai_solver.models.MoraColor import MoraColor


def test_solver_finds_short_solution():
    solver = MoraSolver()
    engine = solver.engine

    # 1. On configure une cible (les 4 coins)
    engine.target_state = {
        (0, 0): MoraColor.YELLOW,
        (0, 4): MoraColor.GREY,
        (4, 4): MoraColor.GREY,
        (4, 0): MoraColor.GREY,
    }

    # 2. On configure un plateau initial à exactement 1 coup de la victoire
    # Si on clique sur le Jaune en (2,1), il monte en (1,1) et valide le coin (0,0) !
    engine.board_state = {
        (1, 1): MoraColor.WHITE,
        (1, 2): MoraColor.GREY,
        (1, 3): MoraColor.GREY,
        (2, 1): MoraColor.YELLOW,
        (2, 2): MoraColor.GREY,
        (2, 3): MoraColor.GREY,
        (3, 1): MoraColor.GREY,
        (3, 2): MoraColor.GREY,
        (3, 3): MoraColor.GREY,
    }

    # 3. On lance la résolution
    path = solver.solve()

    # 4. Vérifications
    assert path is not None
    assert len(path) == 1
    assert path[0] == (2, 1)  # Le solveur doit avoir trouvé qu'il faut cliquer en (2,1)
