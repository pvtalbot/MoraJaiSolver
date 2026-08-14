from abc import ABC

from morajai_solver.domain.colors import MoraColor
from morajai_solver.models.mora_board import MoraBoard


class MovementStrategy(ABC):
    def visit(self, board: MoraBoard, pos: int) -> None:
        pass


class YellowStrategy(MovementStrategy):
    def visit(self, board: MoraBoard, pos: int) -> None:
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


class PurpleStrategy(MovementStrategy):
    def visit(self, board: MoraBoard, pos: int) -> None:
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


class GreenStrategy(MovementStrategy):
    def visit(self, board: MoraBoard, pos: int) -> None:
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


class BlackStrategy(MovementStrategy):
    def visit(self, board: MoraBoard, pos: int) -> None:
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


class OrangeStrategy(MovementStrategy):
    def visit(self, board: MoraBoard, pos: int) -> None:
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


class GreyStrategy(MovementStrategy):
    pass


class PinkStrategy(MovementStrategy):
    def visit(self, board: MoraBoard, pos: int) -> None:
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


class RedStrategy(MovementStrategy):
    def visit(self, board: MoraBoard, pos: int) -> None:
        for shift in (0, 4, 8, 12, 16, 20, 24, 28, 32):
            color = (board.data >> shift) & 0xF

            if color == MoraColor.BLACK:
                board.data = (board.data & ~(0xF << shift)) | (MoraColor.RED << shift)
            elif color == MoraColor.WHITE:
                board.data = (board.data & ~(0xF << shift)) | (MoraColor.BLACK << shift)


class WhiteStrategy(MovementStrategy):
    def visit(self, board: MoraBoard, pos: int) -> None:
        target_color = (board.data >> (pos * 4)) & 0xF
        for i in ORTHOGONAL_NEIGHBORS[pos]:
            shift = i * 4
            color = (board.data >> shift) & 0xF

            if color == MoraColor.GREY:
                board.data = (board.data & ~(0xF << shift)) | (target_color << shift)
            elif color == target_color:
                board.data = (board.data & ~(0xF << shift)) | (MoraColor.GREY << shift)

        board.data = (board.data & ~(0xF << (pos * 4))) | (MoraColor.GREY << (pos * 4))


class BlueStrategy(MovementStrategy):
    def visit(self, board: MoraBoard, pos: int) -> None:
        center_color = (board.data >> 16) & 0xF

        if center_color == MoraColor.BLUE:
            return

        stragegy = COLOR_STRATEGIES[center_color]
        if stragegy:
            stragegy.visit(board, pos)


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

COLOR_STRATEGIES: tuple[MovementStrategy, ...] = (
    GreyStrategy(),
    WhiteStrategy(),
    BlackStrategy(),
    RedStrategy(),
    YellowStrategy(),
    PurpleStrategy(),
    GreenStrategy(),
    PinkStrategy(),
    OrangeStrategy(),
    BlueStrategy(),
)
