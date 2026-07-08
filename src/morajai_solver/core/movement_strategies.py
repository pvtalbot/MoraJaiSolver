from abc import ABC, abstractmethod
from collections import Counter
from morajai_solver.components.MoraButton import MoraColor
from morajai_solver.event_dispatcher import EventDispatcher
from morajai_solver.models.MoraEvent import MoraEvent

class MovementStrategy(ABC):
    @abstractmethod
    def execute(self, r: int, c: int, board_state: dict, dispatcher: EventDispatcher|None = None) -> None:
        if dispatcher:
            dispatcher.emit(MoraEvent.BOARD_UPDATED, board_state=board_state)

class YellowStrategy(MovementStrategy):
    def execute(self, r: int, c: int, board_state: dict, dispatcher: EventDispatcher|None = None) -> None:
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
    def execute(self, r: int, c: int, board_state: dict, dispatcher: EventDispatcher|None = None) -> None:
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
    def execute(self, r: int, c: int, board_state: dict, dispatcher: EventDispatcher|None = None) -> None:
        color_c1 = board_state.get((r, 1))
        color_c2 = board_state.get((r, 2))
        color_c3 = board_state.get((r, 3))

        board_state[(r, 1)] = color_c3
        board_state[(r, 2)] = color_c1
        board_state[(r, 3)] = color_c2

        super().execute(r, c, board_state, dispatcher)

class GreenStrategy(MovementStrategy):
    def execute(self, r: int, c: int, board_state: dict, dispatcher: EventDispatcher|None = None) -> None:
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

class PinkStrategy(MovementStrategy):
    def execute(self, r: int, c: int, board_state: dict, dispatcher: EventDispatcher|None = None) -> None:
        all_neighbors = [
            (r-1, c),
            (r-1, c+1),
            (r, c+1),
            (r+1, c+1),
            (r+1, c),
            (r+1, c-1),
            (r, c-1),
            (r-1, c-1)
        ]

        valid_positions = [pos for pos in all_neighbors if pos in board_state]

        if len(valid_positions) < 2:
            return

        current_colors = [board_state[pos] for pos in valid_positions]
        rotated_colors = [current_colors[-1]] + current_colors[:-1]

        for pos, new_color in zip(valid_positions, rotated_colors):
            board_state[pos] = new_color

        return super().execute(r, c, board_state, dispatcher)

class BlueStrategy(MovementStrategy):
    def execute(self, r: int, c: int, board_state: dict, dispatcher: EventDispatcher|None = None) -> None:
        center_color = board_state.get((2, 2))

        if center_color is None or center_color == MoraColor.BLUE:
            return

        strategy = STRATEGY_MAP.get(center_color)
        if not strategy:
            return
        strategy.execute(r, c, board_state, dispatcher)

        return super().execute(r, c, board_state, dispatcher)

class RedStrategy(MovementStrategy):
    def execute(self, r: int, c: int, board_state: dict, dispatcher: EventDispatcher|None = None) -> None:
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

class OrangeStrategy(MovementStrategy):
    def execute(self, r: int, c: int, board_state: dict, dispatcher: EventDispatcher|None = None) -> None:
        ortho_neighbors = [
            (r-1, c),
            (r+1, c),
            (r, c+1),
            (r, c-1)
        ]

        valid_neighbors = [pos for pos in ortho_neighbors if pos in board_state]

        if not valid_neighbors:
            return

        neighbors_colors = [board_state[pos] for pos in valid_neighbors]
        color_counts = Counter(neighbors_colors)
        top_colors = color_counts.most_common(2)

        if len(top_colors) == 1:
            majority_color = top_colors[0][0]
        else:
            (color1, c1), (_, c2) = top_colors[0], top_colors[1]
            if c1 > c2:
                majority_color = color1
            else:
                return

        board_state[(r, c)] = majority_color

        super().execute(r, c, board_state, dispatcher)

class GreyStragery(MovementStrategy):
    def execute(self, r: int, c: int, board_state: dict, dispatcher: EventDispatcher|None = None) -> None:
        pass

class WhiteStragegy(MovementStrategy):
    def execute(self, r: int, c: int, board_state: dict, dispatcher: EventDispatcher|None = None) -> None:
        candidates = [
            (r, c),
            (r+1,c),
            (r-1,c),
            (r,c+1),
            (r,c-1)
        ]
        start_color = board_state[(r, c)]

        valid_candidates = [pos for pos in candidates if pos in board_state]

        for candidate in valid_candidates:
            if board_state[candidate] == start_color:
                board_state[candidate] = MoraColor.GREY
            elif board_state[candidate] == MoraColor.GREY:
                board_state[candidate] = start_color

        super().execute(r, c, board_state, dispatcher)


STRATEGY_MAP: dict[MoraColor, MovementStrategy] = {
    MoraColor.YELLOW: YellowStrategy(),
    MoraColor.PURPLE: PurpleStrategy(),
    MoraColor.BLACK: BlackStrategy(),
    MoraColor.GREEN: GreenStrategy(),
    MoraColor.PINK: PinkStrategy(),
    MoraColor.BLUE: BlueStrategy(),
    MoraColor.RED: RedStrategy(),
    MoraColor.ORANGE: OrangeStrategy(),
    MoraColor.GREY: GreyStragery(),
    MoraColor.WHITE: WhiteStragegy()
}