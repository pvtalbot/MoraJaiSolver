from abc import ABC, abstractmethod
from morajai_solver.components.MoraButton import MoraColor
from morajai_solver.event_dispatcher import EventDispatcher

class MovementStrategy(ABC):
    @abstractmethod
    def execute(self, r: int, c: int, board_state: dict, dispatcher: EventDispatcher) -> None:
        dispatcher.emit('board_updated', board_state=board_state)

class YellowStrategy(MovementStrategy):
    def execute(self, r: int, c: int, board_state: dict, dispatcher: EventDispatcher) -> None:
        other_row = r - 1
        other_col = c

        if (other_row, other_col) not in board_state:
            return

        other_color = board_state[(other_row, other_col)]

        board_state[(other_row, other_col)] = MoraColor.YELLOW
        board_state[(r, c)] = other_color

        super().execute(r, c, board_state, dispatcher)


class PurpleStrategy(MovementStrategy):
    def execute(self, r: int, c: int, board_state: dict, dispatcher: EventDispatcher) -> None:
        other_row = r + 1
        other_col = c

        if (other_row, other_col) not in board_state:
            return

        other_color = board_state[(other_row, other_col)]

        board_state[(other_row, other_col)] = MoraColor.PURPLE
        board_state[(r, c)] = other_color

        super().execute(r, c, board_state, dispatcher)


class BlackStrategy(MovementStrategy):
    def execute(self, r: int, c: int, board_state: dict, dispatcher: EventDispatcher) -> None:
        color_c1 = board_state.get((r, 1))
        color_c2 = board_state.get((r, 2))
        color_c3 = board_state.get((r, 3))

        board_state[(r, 1)] = color_c3
        board_state[(r, 2)] = color_c1
        board_state[(r, 3)] = color_c2

        super().execute(r, c, board_state, dispatcher)

class GreenStrategy(MovementStrategy):
    def execute(self, r: int, c: int, board_state: dict, dispatcher: EventDispatcher) -> None:
        if (r, c) == (2, 2):
            return
        opposite_r, opposite_c = 4-r, 4-c
        if (opposite_r, opposite_c) not in board_state:
            return
        opposite_color = board_state[(opposite_r, opposite_c)]

        board_state[(opposite_r, opposite_c)] = MoraColor.GREEN
        board_state[(r, c)] = opposite_color

        super().execute(r, c, board_state, dispatcher)