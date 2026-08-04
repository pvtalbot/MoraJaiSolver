from abc import ABC, abstractmethod
from typing import Generator

from morajai_solver.models.MoraColor import MoraColor

type Coord = tuple[int, int]


class AbstractMoraBoard(ABC):
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
        """Vérifie si l'état actuelle de la grille satisfait l'ensemble des cibles"""
        pass

    def __contains__(self, pos: Coord):
        r, c = pos
        return 1 <= r <= 3 and 1 <= c <= 3


class DictMoraBoard(AbstractMoraBoard):
    def __init__(self, board_dict: dict[Coord, MoraColor] | None = None):
        self._data: dict[Coord, MoraColor] = (
            board_dict if board_dict is not None else {}
        )
        self._targets: dict[Coord, MoraColor] = {}

    def __getitem__(self, pos: Coord) -> MoraColor:
        return self._data[pos]

    def __setitem__(self, pos: Coord, color: MoraColor):
        self._data[pos] = color

    def items(self):
        for pos, color in self._data.items():
            yield pos, color

    def set_target(self, row: int, col: int, color: MoraColor) -> None:
        self._targets[(row, col)] = color

    def check_victory(self) -> bool:
        return all(self._data[x] == self._targets[x] for x in self._targets)

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value: dict[Coord, MoraColor]) -> None:
        self._data = value


class BitmaskMoraBoard(AbstractMoraBoard):
    def __init__(self, bitmask: int = 0):
        self._data = bitmask
        self._target_state: int = 0
        self._target_mask: int = 0

    def _pos_to_shift(self, pos: Coord) -> int:
        r, c = pos
        return ((r - 1) * 3 + (c - 1)) * 4

    def set_target(self, row: int, col: int, color: MoraColor) -> None:
        shift = self._pos_to_shift((row, col))

        self._target_state &= ~(0xF << shift)
        self._target_state |= color.value << shift
        self._target_mask |= 0xF << shift

    def check_victory(self) -> bool:
        if self._target_mask == 0:
            return False

        return (self._data & self._target_mask) == self._target_state

    def __getitem__(self, pos: Coord) -> MoraColor:
        i = self._pos_to_shift(pos)
        color = (self._data >> i) & 0xF
        return MoraColor(color)

    def __setitem__(self, pos: Coord, color: MoraColor):
        i = self._pos_to_shift(pos)
        clear_mask = ~(0xF << i)
        self._data = (self._data & clear_mask) | (int(color) << i)

    def items(self):
        for r in range(1, 4):
            for c in range(1, 4):
                yield (r, c), self[(r, c)]
