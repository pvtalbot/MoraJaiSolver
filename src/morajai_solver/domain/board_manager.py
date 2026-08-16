import random

from morajai_solver.domain.colors import MoraColor
from morajai_solver.domain.movement_strategies import COLOR_STRATEGIES
from morajai_solver.models.mora_board import MoraBoard
from morajai_solver.models.types import Coord


class BoardManager:
    board: MoraBoard
    _play_index: int
    moves: list[int]

    def __init__(self):
        self.board = MoraBoard()
        self._play_index = 0
        self.moves = list()

    @property
    def index(self):
        return self._play_index - 1

    def get_state_as_dict(self) -> dict[Coord, MoraColor]:
        result = dict()
        for r in range(1, 4):
            for c in range(1, 4):
                result[r, c] = self.board[r, c]

        return result

    def get_targets_as_dict(self) -> dict[Coord, MoraColor]:
        result = dict()
        for pos in ((1, 1), (3, 1), (1, 3), (3, 3)):
            result[pos] = self.board.get_target(pos)
        return result

    def reset(self):
        self._play_index = 1
        self.moves = [self.board.data]

    def initial_board(self) -> bool:
        self._play_index = 1
        return self._update_board()

    def next_move(self) -> bool:
        self._play_index = min(len(self.moves), self._play_index + 1)
        return self._update_board()

    def previous_move(self) -> bool:
        self._play_index = max(1, self._play_index - 1)
        return self._update_board()

    def last_move(self) -> bool:
        self._play_index = len(self.moves)
        return self._update_board()

    def _update_board(self) -> bool:
        self.board.data = self.moves[self._play_index - 1]
        return self.board.check_victory()

    def load_state_from_dict(
        self,
        state: dict[Coord, MoraColor],
        targets: dict[Coord, MoraColor] | None = None,
    ):
        for k, v in state.items():
            self.board[k] = v

        if not targets:
            return
        for k, v in targets.items():
            self.board.set_target(k, v)

        self._push_move()

    def play_move(self, pos: Coord) -> bool:
        color = self.board[pos]
        strategy = COLOR_STRATEGIES[color]

        self.board.accept(strategy, pos)
        self._push_move()

        return self.board.check_victory()

    def randomize(self):
        available_colors = list(MoraColor)

        for r in range(1, 4):
            for c in range(1, 4):
                random_color = random.choice(available_colors)
                self.board[(r, c)] = random_color

        self._push_move()

    def _push_move(self):
        if self._play_index < len(self.moves):
            self.moves = self.moves[: self._play_index]

        self.moves.append(self.board.data)
        self._play_index += 1
