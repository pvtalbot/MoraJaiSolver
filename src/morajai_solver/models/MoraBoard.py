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

    def __contains__(self, pos: Coord):
        r, c = pos
        return 1 <= r <= 3 and 1 <= c <= 3

class DictMoraBoard(AbstractMoraBoard):
    def __init__(self, board_dict: dict):
        self._data = board_dict

    def __getitem__(self, pos: Coord) -> MoraColor:
        return self._data[pos]

    def __setitem__(self, pos: Coord, color: MoraColor):
        self._data[pos] = color

    def items(self):
        for (pos, color) in self._data.items():
            yield pos, color

class BitmaskMoraBoard(AbstractMoraBoard):
    def __init__(self, bitmask: int):
        self._data = bitmask

    def _pos_to_index(self, pos: Coord) -> int:
        r, c = pos
        return (r-1) * 3 + (c-1)

    def __getitem__(self, pos: Coord) -> MoraColor:
        i = self._pos_to_index(pos)
        color = (self._data >> (i * 4)) & 0xF
        return MoraColor(color)

    def __setitem__(self, pos: Coord, color: MoraColor):
        i = self._pos_to_index(pos)
        clear_mask = ~(0xF << (i * 4))
        self._data = (self._data & clear_mask) | (int(color) << (i * 4))

    def items(self):
        for r in range(1, 4):
            for c in range(1, 4):
                yield (r, c), self[(r, c)]