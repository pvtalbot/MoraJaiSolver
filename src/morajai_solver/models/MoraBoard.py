from __future__ import annotations
from typing import TYPE_CHECKING
from abc import ABC, abstractmethod
from typing import Generator

from morajai_solver.domain.colors import MoraColor
from morajai_solver.models.types import Coord

if TYPE_CHECKING:
    from morajai_solver.domain.MovementVisitors import MovementVisitor


class AbstractMoraBoard(ABC):
    @abstractmethod
    def accept(self, visitor: MovementVisitor, pos: Coord) -> None:
        pass

    @abstractmethod
    def __getitem__(self, pos: Coord) -> MoraColor:
        pass

    @abstractmethod
    def __setitem__(self, pos: Coord, color: MoraColor):
        pass

    def swap(self, pos1: Coord, pos2: Coord):
        color1 = self[pos1]
        color2 = self[pos2]
        self[pos1] = color2
        self[pos2] = color1

    def get(self, pos: Coord, default=None) -> MoraColor | None:
        if pos in self:
            return self[pos]
        return default

    @abstractmethod
    def items(self) -> Generator[tuple[Coord, MoraColor], None, None]:
        pass

    @abstractmethod
    def set_target(self, row: int, col: int, color: MoraColor) -> None:
        pass

    @abstractmethod
    def check_victory(self) -> bool:
        pass

    def __contains__(self, pos: Coord):
        r, c = pos
        return 1 <= r <= 3 and 1 <= c <= 3


class DictMoraBoard(AbstractMoraBoard):
    data: dict[Coord, MoraColor]
    targets: dict[Coord, MoraColor]

    def __init__(self, board_dict: dict[Coord, MoraColor] | None = None):
        self.data: dict[Coord, MoraColor] = board_dict if board_dict is not None else {}
        self.targets: dict[Coord, MoraColor] = {}

    def __getitem__(self, pos: Coord) -> MoraColor:
        return self.data[pos]

    def __setitem__(self, pos: Coord, color: MoraColor):
        self.data[pos] = color

    def items(self):
        for pos, color in self.data.items():
            yield pos, color

    def set_target(self, row: int, col: int, color: MoraColor) -> None:
        self.targets[(row, col)] = color

    def check_victory(self) -> bool:
        return all(self.data[x] == self.targets[x] for x in self.targets)

    def accept(self, visitor: MovementVisitor, pos: Coord) -> None:
        visitor.visit_dict_board(self, pos)

    def get_bitmask_board(self):
        result = BitmaskMoraBoard()
        for k, v in self.data.items():
            result[k] = v
        for (r, c), v in self.targets.items():
            result.set_target(r, c, v)
        return result


class BitmaskMoraBoard(AbstractMoraBoard):
    data: int
    target_state: int

    TARGET_MASK: int = 0xF0F_000_F0F

    def __init__(self, bitmask: int = 0):
        self.data = bitmask
        self.target_state: int = 0

    def _pos_to_shift(self, pos: Coord) -> int:
        r, c = pos
        return ((r - 1) * 3 + (c - 1)) * 4

    def set_target(self, row: int, col: int, color: MoraColor) -> None:
        shift = self._pos_to_shift((row, col))

        self.target_state &= ~(0xF << shift)
        self.target_state |= color.value << shift

    def check_victory(self) -> bool:
        return (self.data & self.TARGET_MASK) == self.target_state

    # Should not be used for computation, only for tests
    def __getitem__(self, pos: Coord) -> MoraColor:
        i = self._pos_to_shift(pos)
        color = (self.data >> i) & 0xF
        return MoraColor(color)

    # Should not be used for computation, only for tests
    def __setitem__(self, pos: Coord, color: MoraColor):
        i = self._pos_to_shift(pos)
        clear_mask = ~(0xF << i)
        self.data = (self.data & clear_mask) | (int(color) << i)

    # Should not be used for computation, only for tests
    def items(self):
        for r in range(1, 4):
            for c in range(1, 4):
                yield (r, c), self[(r, c)]

    def accept(self, visitor: MovementVisitor, pos: Coord) -> None:
        r, c = pos
        visitor.visit_bitmask_board(self, (r - 1) * 3 + c - 1)
