from collections import deque
import logging

from morajai_solver.core.game_engine import GameEngine
from morajai_solver.core.movement_strategies import STRATEGY_MAP
from morajai_solver.models.MoraBoard import BitmaskMoraBoard

logger = logging.getLogger(__name__)


class MoraSolver:
    def __init__(self):
        self.engine = GameEngine()

    def solve(self):
        start_dict = self.engine.board_state

        initial_board = BitmaskMoraBoard()
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
