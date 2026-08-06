from abc import ABC
from collections import Counter

from morajai_solver.models.MoraBoard import BitmaskMoraBoard, DictMoraBoard
from morajai_solver.domain.colors import MoraColor
from morajai_solver.models.types import Coord


class MovementVisitor(ABC):
    def visit_dict_board(self, board: DictMoraBoard, pos: Coord) -> None:
        pass

    def visit_bitmask_board(self, board: BitmaskMoraBoard, pos: int) -> None:
        pass


class YellowVisitor(MovementVisitor):
    def visit_dict_board(self, board: DictMoraBoard, pos: Coord) -> None:
        r, c = pos
        if r == 1:
            return

        dest_pos = (r - 1, c)
        board[pos], board[dest_pos] = board[dest_pos], board[pos]

    def visit_bitmask_board(self, board: BitmaskMoraBoard, pos: int) -> None:
        if pos < 3:
            return

        dest = pos - 3
        shift_source, shift_dest = pos * 4, dest * 4

        color_source = (board.data >> shift_source) & 0xF
        color_dest = (board.data >> shift_dest) & 0xF

        clear_mask = ~((0xF << shift_source) | (0xF << shift_dest))
        board.data = (
            (board.data & clear_mask)
            | (color_source << shift_dest)
            | (color_dest << shift_source)
        )


class PurpleVisitor(MovementVisitor):
    def visit_dict_board(self, board: DictMoraBoard, pos: Coord) -> None:
        r, c = pos
        if r == 3:
            return
        dest_pos = (r + 1, c)
        board[pos], board[dest_pos] = board[dest_pos], board[pos]

    def visit_bitmask_board(self, board: BitmaskMoraBoard, pos: int) -> None:
        if pos > 5:
            return
        dest = pos + 3
        shift_source, shift_dest = pos * 4, dest * 4

        color_source = (board.data >> shift_source) & 0xF
        color_dest = (board.data >> shift_dest) & 0xF

        clear_mask = ~((0xF << shift_source) | (0xF << shift_dest))
        board.data = (
            (board.data & clear_mask)
            | (color_source << shift_dest)
            | (color_dest << shift_source)
        )


class GreenVisitor(MovementVisitor):
    def visit_dict_board(self, board: DictMoraBoard, pos: Coord) -> None:
        r, c = pos
        dest_pos = (4 - r, 4 - c)

        if pos == dest_pos:
            return

        board[pos], board[dest_pos] = board[dest_pos], board[pos]

    def visit_bitmask_board(self, board: BitmaskMoraBoard, pos: int) -> None:
        dest = 8 - pos

        if pos == dest:
            return
        shift_source, shift_dest = pos * 4, dest * 4

        color_source = (board.data >> shift_source) & 0xF
        color_dest = (board.data >> shift_dest) & 0xF

        clear_mask = ~((0xF << shift_source) | (0xF << shift_dest))
        board.data = (
            (board.data & clear_mask)
            | (color_source << shift_dest)
            | (color_dest << shift_source)
        )


class BlackVisitor(MovementVisitor):
    def visit_dict_board(self, board: DictMoraBoard, pos: Coord) -> None:
        r, _ = pos
        board[(r, 1)], board[(r, 3)] = board[(r, 3)], board[(r, 1)]
        board[(r, 2)], board[(r, 3)] = board[(r, 3)], board[(r, 2)]

    def visit_bitmask_board(self, board: BitmaskMoraBoard, pos: int) -> None:
        first_pos = (pos // 3) * 3
        clear_mask = ~(
            (0xF << (4 * first_pos))
            | (0xF << (4 * first_pos + 4))
            | (0xF << (4 * first_pos + 8))
        )

        c0 = (board.data >> 4 * first_pos) & 0xF
        c1 = (board.data >> (4 * first_pos + 4)) & 0xF
        c2 = (board.data >> (4 * first_pos + 8)) & 0xF

        board.data = (
            (board.data & clear_mask)
            | (c1 << (4 * first_pos + 8))
            | (c2 << (4 * first_pos))
            | (c0 << (4 * first_pos + 4))
        )


class OrangeVisitor(MovementVisitor):
    def visit_dict_board(self, board: DictMoraBoard, pos: Coord) -> None:
        r, c = pos
        neighbors = [(r - 1, c), (r, c - 1), (r + 1, c), (r, c + 1)]
        valid_neighbors = [n for n in neighbors if n in board]
        color_counts = Counter(board[pos] for pos in valid_neighbors)
        most_common = color_counts.most_common(2)

        if len(most_common) == 1:
            board[pos] = most_common[0][0]
        elif len(most_common) == 2 and most_common[0][1] > most_common[1][1]:
            board[pos] = most_common[0][0]

    def visit_bitmask_board(self, board: BitmaskMoraBoard, pos: int) -> None:
        neighbors_indices = ORTHOGONAL_NEIGHBORS[pos]
        counts = [0] * 10
        for n in neighbors_indices:
            color = (board.data >> (n * 4)) & 0xF
            counts[color] += 1

        max_count = 0
        winning_color = None
        is_tie = False

        for color, count in enumerate(counts):
            if count > max_count:
                max_count = count
                winning_color = color
                is_tie = False
            elif count == max_count and count > 0:
                is_tie = True

        if winning_color and not is_tie:
            shift = pos * 4
            board.data = (board.data & ~(0xF << shift)) | (winning_color << shift)


class GreyVisitor(MovementVisitor):
    pass


class PinkVisitor(MovementVisitor):
    def visit_dict_board(self, board: DictMoraBoard, pos: Coord) -> None:
        r, c = pos
        index = (r - 1) * 3 + c - 1
        ring = PINK_ROTATION_RINGS[index]

        ring_coords = [(i // 3 + 1, i % 3 + 1) for i in ring]
        values = [board[coord] for coord in ring_coords]
        rotated = [values[-1]] + values[:-1]
        for coord, val in zip(ring_coords, rotated):
            board[coord] = val

    def visit_bitmask_board(self, board: BitmaskMoraBoard, pos: int) -> None:
        ring = PINK_ROTATION_RINGS[pos]

        last_pos = ring[-1]
        prev_color = (board.data >> (last_pos * 4)) & 0xF

        clear_mask = 0
        write_mask = 0

        for curr_pos in ring:
            shift = curr_pos * 4
            curr_color = (board.data >> shift) & 0xF

            clear_mask |= 0xF << shift
            write_mask |= prev_color << shift

            prev_color = curr_color

        board.data = (board.data & ~clear_mask) | write_mask


class RedVisitor(MovementVisitor):
    def visit_dict_board(self, board: DictMoraBoard, pos: Coord) -> None:
        for pos, color in board.items():
            if color == MoraColor.BLACK:
                board[pos] = MoraColor.RED
            elif color == MoraColor.WHITE:
                board[pos] = MoraColor.BLACK

    def visit_bitmask_board(self, board: BitmaskMoraBoard, pos: int) -> None:
        for shift in (0, 4, 8, 12, 16, 20, 24, 28, 32):
            color = (board.data >> shift) & 0xF

            if color == MoraColor.BLACK:
                board.data = (board.data & ~(0xF << shift)) | (MoraColor.RED << shift)
            elif color == MoraColor.WHITE:
                board.data = (board.data & ~(0xF << shift)) | (MoraColor.BLACK << shift)


class WhiteVisitor(MovementVisitor):
    def visit_dict_board(self, board: DictMoraBoard, pos: Coord) -> None:
        r, c = pos
        candidates = [(r, c), (r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]
        valid_candidates = [c for c in candidates if c in board]
        color = board[pos]

        for candidate in valid_candidates:
            if board[candidate] == MoraColor.GREY:
                board[candidate] = color
            elif board[candidate] == color:
                board[candidate] = MoraColor.GREY

    def visit_bitmask_board(self, board: BitmaskMoraBoard, pos: int) -> None:
        target_color = (board.data >> (pos * 4)) & 0xF
        for i in ORTHOGONAL_NEIGHBORS[pos]:
            shift = i * 4
            color = (board.data >> shift) & 0xF

            if color == MoraColor.GREY:
                board.data = (board.data & ~(0xF << shift)) | (target_color << shift)
            elif color == target_color:
                board.data = (board.data & ~(0xF << shift)) | (MoraColor.GREY << shift)

        board.data = (board.data & ~(0xF << (pos * 4))) | (MoraColor.GREY << (pos * 4))


class BlueVisitor(MovementVisitor):
    def visit_dict_board(self, board: DictMoraBoard, pos: Coord) -> None:
        center_color = board[(2, 2)]
        if center_color == MoraColor.BLUE:
            return

        visitor = COLOR_VISITORS[center_color]
        if visitor:
            visitor.visit_dict_board(board, pos)

    def visit_bitmask_board(self, board: BitmaskMoraBoard, pos: int) -> None:
        center_color = (board.data >> 16) & 0xF

        if center_color == MoraColor.BLUE:
            return

        visitor = COLOR_VISITORS[center_color]
        if visitor:
            visitor.visit_bitmask_board(board, pos)


ORTHOGONAL_NEIGHBORS = (
    (1, 3),
    (0, 2, 4),
    (1, 5),
    (0, 4, 6),
    (1, 3, 5, 7),
    (2, 4, 8),
    (3, 7),
    (4, 6, 8),
    (5, 7),
)

PINK_ROTATION_RINGS = [
    (1, 4, 3),
    (2, 5, 4, 3, 0),
    (5, 4, 1),
    (0, 1, 4, 7, 6),
    (0, 1, 2, 5, 8, 7, 6, 3),
    (2, 8, 7, 4, 1),
    (3, 4, 7),
    (4, 5, 8, 6, 3),
    (4, 7, 5),
]

COLOR_VISITORS: tuple[MovementVisitor, ...] = (
    GreyVisitor(),
    WhiteVisitor(),
    BlackVisitor(),
    RedVisitor(),
    YellowVisitor(),
    PurpleVisitor(),
    GreenVisitor(),
    PinkVisitor(),
    OrangeVisitor(),
    BlueVisitor(),
)
