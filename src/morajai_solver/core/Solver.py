from collections import deque
import logging

from morajai_solver.core.MovementStrategies import STRATEGY_MAP
from morajai_solver.models.MoraBoard import BitmaskMoraBoard, DictMoraBoard

logger = logging.getLogger(__name__)


class MoraSolver:
    def __init__(self, board: DictMoraBoard):
        self._board = BitmaskMoraBoard()

        for (r, c), color in board.data.items():
            self._board[r, c] = color

        for (r, c), color in board._targets.items():
            self._board.set_target(r, c, color)

    def solve(self):
        start_bitmask = self._board._data

        if self._board.check_victory():
            return []

        queue = deque([(start_bitmask, [])])

        visited = {start_bitmask}
        logger.info("Début de la recherche de solution")

        while queue:
            current_bitmask, path = queue.popleft()
            logger.debug(f"Queue length : {len(queue)}")

            for r in range(1, 4):
                for c in range(1, 4):
                    self._board._data = current_bitmask

                    color = self._board[r, c]
                    strategy = STRATEGY_MAP.get(color)

                    if not strategy:
                        continue
                    strategy.execute(r, c, self._board)

                    if self._board.check_victory():
                        final_path = path + [(r, c)]
                        logger.info(f"Solution trouvée en {len(final_path)} coups")
                        return final_path

                    next_bitmask = self._board._data
                    if next_bitmask not in visited:
                        visited.add(next_bitmask)
                        queue.append((next_bitmask, path + [(r, c)]))

        logger.warning("Aucune solution")
        return None
