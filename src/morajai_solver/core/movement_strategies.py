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

        color = board_state[r, c]
        other_color = board_state[(other_row, other_col)]

        board_state[(other_row, other_col)] = color
        board_state[(r, c)] = other_color

        super().execute(r, c, board_state, dispatcher)

class PurpleStrategy(MovementStrategy):
    def execute(self, r: int, c: int, board_state: dict, dispatcher: EventDispatcher) -> None:
        other_row = r + 1
        other_col = c

        if (other_row, other_col) not in board_state:
            return

        color = board_state[(r, c)]
        other_color = board_state[(other_row, other_col)]

        board_state[(other_row, other_col)] = color
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
            
        color = board_state[(r, c)]
        opposite_color = board_state[(opposite_r, opposite_c)]

        board_state[(opposite_r, opposite_c)] = color
        board_state[(r, c)] = opposite_color

        super().execute(r, c, board_state, dispatcher)

class BlueStrategy(MovementStrategy):
    def execute(self, r: int, c: int, board_state: dict, dispatcher: EventDispatcher) -> None:
        center_color = board_state.get((2, 2))

        if center_color is None or center_color == MoraColor.BLUE:
            return

        strategy = STRATEGY_MAP.get(center_color)
        if not strategy:
            return
        strategy.execute(r, c, board_state, dispatcher)

        return super().execute(r, c, board_state, dispatcher)

class RedStrategy(MovementStrategy):
    def execute(self, r: int, c: int, board_state: dict, dispatcher: EventDispatcher) -> None:
        changed = False

        for pos, color in board_state.items():
            row, col = pos
            if 1 <= row <= 3 and 1 <= col <= 3:
                if color == MoraColor.WHITE:
                    board_state[pos] = MoraColor.BLACK
                    changed = True
                elif color == MoraColor.BLACK:
                    board_state[pos] = MoraColor.RED
                    changed = True

        if changed:
            super().execute(r, c, board_state, dispatcher)

STRATEGY_MAP: dict[MoraColor, MovementStrategy] = {
    MoraColor.YELLOW: YellowStrategy(),
    MoraColor.PURPLE: PurpleStrategy(),
    MoraColor.BLACK: BlackStrategy(),
    MoraColor.GREEN: GreenStrategy(),
    MoraColor.BLUE: BlueStrategy(),
    MoraColor.RED: RedStrategy(),
}