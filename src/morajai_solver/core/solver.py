from collections import deque
import logging

from morajai_solver.core.game_engine import GameEngine
from morajai_solver.core.movement_strategies import STRATEGY_MAP
from morajai_solver.models.MoraBoard import BitmaskMoraBoard

logger = logging.getLogger(__name__)

class MoraSolver:
    def __init__(self):
        self.engine = GameEngine()

    def _dict_to_tuple(self, board_state: dict) -> tuple:
        return tuple(sorted((pos, color) for pos, color in board_state.items()))

    def _tuple_to_dict(self, board_tuple: tuple) -> dict:
        return dict(board_tuple)

    def dict_to_bitmask(self, board_state: dict) -> int:
        bitmask = 0
        index = 0
        for r in range(1, 4):
            for c in range(1, 4):
                color_val = int(board_state[(r, c)])
                bitmask |= (color_val << (index * 4))
                index += 1
        return bitmask

    def bitmask_get_color(self, bitmask: int, index: int) -> int:
        return (bitmask >> (index * 4)) & 0xF

    def bitmask_set_color(self, bitmask: int, index: int, new_color: int) -> int:
        clear_mask = ~(0xF << (index * 4))
        bitmask_cleared = bitmask & clear_mask
        return bitmask_cleared | (new_color << (index * 4))

    def solve(self):
        start_dict = self.engine.board_state

        initial_board = BitmaskMoraBoard(0)
        for (r, c), color in start_dict.items():
            initial_board[r, c] = color

        start_bitmask = initial_board._data

        if self.engine.check_victory(initial_board):
            return []

        queue = deque([(start_bitmask, [])])

        visited = {start_bitmask}
        logger.info("Début de la recherche de solution")

        while queue:
            current_bitmask, path = queue.popleft()
            logger.debug(f"Queue length : {len(queue)}")

            for r in range(1, 4):
                for c in range(1, 4):
                    simulated_board = BitmaskMoraBoard(current_bitmask)

                    color = simulated_board[r, c]
                    strategy = STRATEGY_MAP.get(color)

                    if not strategy:
                        continue
                    strategy.execute(r, c, simulated_board)

                    if self.engine.check_victory(simulated_board):
                        final_path = path + [(r, c)]
                        logger.info(f"Solution trouvée en {len(final_path)} coups")
                        return final_path

                    next_bitmask = simulated_board._data
                    if next_bitmask not in visited:
                        visited.add(next_bitmask)
                        queue.append((next_bitmask, path + [(r, c)]))

        logger.warning("Aucune solution")
        return None
