from collections import deque
import logging

from morajai_solver.core.game_engine import GameEngine
from morajai_solver.core.movement_strategies import STRATEGY_MAP

logger = logging.getLogger(__name__)

class MoraSolver:
    def __init__(self):
        self.engine = GameEngine()

    def _dict_to_tuple(self, board_state: dict) -> tuple:
        return tuple(sorted((pos, color) for pos, color in board_state.items()))

    def _tuple_to_dict(self, board_tuple: tuple) -> dict:
        return dict(board_tuple)

    def solve(self):
        start_dict = self.engine.board_state

        start_tuple = self._dict_to_tuple(start_dict)
        queue = deque([(start_tuple, [])])

        visited = {start_tuple}
        logger.info("Début de la recherche de solution")

        while queue:
            current_tuple, path = queue.popleft()
            logger.debug(f"Queue length : {len(queue)}")

            for r in range(1, 4):
                for c in range(1, 4):
                    simulated_board = self._tuple_to_dict(current_tuple)

                    color = simulated_board.get((r, c))
                    assert color is not None
                    strategy = STRATEGY_MAP.get(color)

                    if not strategy:
                        continue
                    strategy.execute(r, c, simulated_board)

                    if self.engine.check_victory(simulated_board):
                        final_path = path + [(r, c)]
                        logger.info(f"Solution trouvée en {len(final_path)} coups")
                        return final_path

                    next_tuple = self._dict_to_tuple(simulated_board)
                    if next_tuple not in visited:
                        visited.add(next_tuple)
                        queue.append((next_tuple, path + [(r, c)]))

        logger.warning("Aucune solution")
        return None
