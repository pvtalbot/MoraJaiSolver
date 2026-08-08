import random

from morajai_solver.domain.colors import MoraColor
from morajai_solver.domain.movement_strategies import COLOR_STRATEGIES
from morajai_solver.models.mora_board import MoraBoard
from morajai_solver.models.types import Coord


class BoardManager:
    board: MoraBoard
    saved_board: int | None

    def __init__(self):
        self.board = MoraBoard()

    def get_state_as_dict(self) -> dict[Coord, MoraColor]:
        result = dict()
        for r in range(1, 4):
            for c in range(1, 4):
                result[r, c] = self.board[r, c]

        return result

    def reset(self):
        if not self.saved_board:
            return
        self.board.data = self.saved_board

    def load_state_from_dict(
        self,
        state: dict[Coord, MoraColor],
        targets: dict[Coord, MoraColor] | None = None,
    ):
        for k, v in state.items():
            self.board[k] = v
        self.saved_board = self.board.data

        if not targets:
            return
        for k, v in targets.items():
            self.board.set_target(k, v)

    def play_move(self, pos: Coord) -> bool:
        color = self.board[pos]
        strategy = COLOR_STRATEGIES[color]

        self.board.accept(strategy, pos)

        return self.board.check_victory()

    def randomize(self):
        available_colors = list(MoraColor)

        for r in range(1, 4):
            for c in range(1, 4):
                random_color = random.choice(available_colors)
                self.board[(r, c)] = random_color
