from collections import deque
import logging

from morajai_solver.domain.MovementVisitors import COLOR_VISITORS
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
        start_bitmask = self._board.data

        if self._board.check_victory():
            return []

        queue = deque([start_bitmask])

        visited = {start_bitmask}
        logger.info("Début de la recherche de solution")

        COORDS = (
            (1, 1),
            (1, 2),
            (1, 3),
            (2, 1),
            (2, 2),
            (2, 3),
            (3, 1),
            (3, 2),
            (3, 3),
        )
        parent_map = dict()

        while queue:
            current_bitmask = queue.popleft()

            for i in range(9):
                self._board.data = current_bitmask

                color = (self._board.data >> (i * 4)) & 0xF

                visitor = COLOR_VISITORS[color]
                visitor.visit_bitmask_board(self._board, i)
                next_bitmask = self._board.data

                if next_bitmask in visited:
                    continue

                visited.add(next_bitmask)
                rc = COORDS[i]
                parent_map[next_bitmask] = (current_bitmask, rc)

                if self._board.check_victory():
                    path = []
                    curr = next_bitmask
                    while curr in parent_map:
                        prev, move = parent_map[curr]
                        path.append(move)
                        curr = prev
                    path.reverse()
                    logger.info(f"Solution trouvée en {len(path)} coups")
                    return path

                queue.append(next_bitmask)

        logger.warning("Aucune solution")
        return None
