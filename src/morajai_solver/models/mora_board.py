from __future__ import annotations

from typing import TYPE_CHECKING

from morajai_solver.domain.colors import MoraColor
from morajai_solver.models.types import Coord

if TYPE_CHECKING:
    from morajai_solver.domain.movement_strategies import MovementStrategy


class MoraBoard:
    data: int
    target_state: int

    TARGET_MASK: int = 0xF0F_000_F0F

    def __init__(self, bitmask: int = 0):
        self.data = bitmask
        self.target_state: int = 0

    def _pos_to_shift(self, pos: Coord) -> int:
        r, c = pos
        return ((r - 1) * 3 + (c - 1)) * 4

    def set_target(self, pos: Coord, color: MoraColor) -> None:
        shift = self._pos_to_shift(pos)

        self.target_state &= ~(0xF << shift)
        self.target_state |= color.value << shift

    def get_target(self, pos: Coord) -> MoraColor:
        shift = self._pos_to_shift(pos)

        return MoraColor((self.target_state >> shift) & 0xF)

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

    def __contains__(self, pos: Coord):
        r, c = pos
        return 1 <= r <= 3 and 1 <= c <= 3

    # Should not be used for computation, only for tests
    def items(self):
        for r in range(1, 4):
            for c in range(1, 4):
                yield (r, c), self[(r, c)]

    def accept(self, strategy: MovementStrategy, pos: Coord) -> None:
        r, c = pos
        strategy.visit(self, (r - 1) * 3 + c - 1)

    def copy(self):
        result = MoraBoard()
        result.data = self.data
        result.target_state = self.target_state

        return result
