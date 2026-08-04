from morajai_solver.models.MoraBoard import DictMoraBoard
from morajai_solver.models.MoraColor import MoraColor


board_1 = DictMoraBoard()
board_1[(1, 1)] = MoraColor.GREEN
board_1[(1, 2)] = MoraColor.WHITE
board_1[(1, 3)] = MoraColor.WHITE
board_1[(2, 1)] = MoraColor.BLACK
board_1[(2, 2)] = MoraColor.WHITE
board_1[(2, 3)] = MoraColor.BLACK
board_1[(3, 1)] = MoraColor.BLUE
board_1[(3, 2)] = MoraColor.WHITE
board_1[(3, 3)] = MoraColor.BLUE
board_1.set_target(1, 1, MoraColor.BLUE)
board_1.set_target(1, 3, MoraColor.BLUE)
board_1.set_target(3, 3, MoraColor.BLUE)
board_1.set_target(3, 1, MoraColor.BLUE)

PRESET_BOARDS = [("Board 1", board_1)]
