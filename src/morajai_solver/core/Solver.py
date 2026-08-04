from collections import deque
import logging

from morajai_solver.core.GameEngine import GameEngine
from morajai_solver.core.MovementStrategies import STRATEGY_MAP
from morajai_solver.models.MoraBoard import BitmaskMoraBoard

logger = logging.getLogger(__name__)


class MoraSolver:
    def __init__(self):
        self.engine = GameEngine()

    def solve(self):
        start_dict = self.engine._board.data

        board = BitmaskMoraBoard()
        for (r, c), color in start_dict.items():
            board[r, c] = color

        for (r, c), color in self.engine._board._targets.items():
            board.set_target(r, c, color)

        start_bitmask = board._data

        if board.check_victory():
            return []

        queue = deque([(start_bitmask, [])])

        visited = {start_bitmask}
        logger.info("Début de la recherche de solution")

        while queue:
            current_bitmask, path = queue.popleft()
            logger.debug(f"Queue length : {len(queue)}")

            for r in range(1, 4):
                for c in range(1, 4):
                    board._data = current_bitmask

                    color = board[r, c]
                    strategy = STRATEGY_MAP.get(color)

                    if not strategy:
                        continue
                    strategy.execute(r, c, board)

                    if board.check_victory():
                        final_path = path + [(r, c)]
                        logger.info(f"Solution trouvée en {len(final_path)} coups")
                        return final_path

                    next_bitmask = board._data
                    if next_bitmask not in visited:
                        visited.add(next_bitmask)
                        queue.append((next_bitmask, path + [(r, c)]))

        logger.warning("Aucune solution")
        return None
