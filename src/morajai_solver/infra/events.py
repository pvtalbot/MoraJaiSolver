from __future__ import annotations
from abc import ABC
from dataclasses import dataclass
from enum import Enum, auto

from morajai_solver.domain.colors import MoraColor
from morajai_solver.models.types import Coord
from morajai_solver.ui.game_modes import MoraMode


class MoraEvent(ABC):
    pass


@dataclass(frozen=True)
class ModeChangedEvent(MoraEvent):
    mode: MoraMode


@dataclass(frozen=True)
class ChangeModeCommand(MoraEvent):
    mode: MoraMode


@dataclass(frozen=True)
class SubmitRequiredEvent(MoraEvent):
    pass


@dataclass(frozen=True)
class RegisterBoardCommand(MoraEvent):
    board: dict[Coord, MoraColor]
    targets: dict[Coord, MoraColor]


@dataclass(frozen=True)
class JumpToStepCommand(MoraEvent):
    step: int


@dataclass(frozen=True)
class RandomizeBoardCommand(MoraEvent):
    pass


@dataclass(frozen=True)
class SolutionInvalidatedEvent(MoraEvent):
    pass


@dataclass(frozen=True)
class BoardLoadedEvent(MoraEvent):
    board: dict[Coord, MoraColor]
    targets: dict[Coord, MoraColor]


@dataclass(frozen=True)
class PlayTileCommand(MoraEvent):
    position: Coord


@dataclass(frozen=True)
class BoardUpdatedEvent(MoraEvent):
    board: dict[Coord, MoraColor]


@dataclass(frozen=True)
class MoveEvaluatedEvent(BoardUpdatedEvent):
    last_move: Coord


@dataclass(frozen=True)
class StepUpdatedEvent(BoardUpdatedEvent):
    current_index: int


@dataclass(frozen=True)
class StartSolverCommand(MoraEvent):
    pass


@dataclass(frozen=True)
class SolutionFoundEvent(MoraEvent):
    result: list[Coord] | None


@dataclass(frozen=True)
class HighlightTileCommand(MoraEvent):
    coord: Coord | None


@dataclass(frozen=True)
class VictoryAchievedEvent(MoraEvent):
    pass


@dataclass(frozen=True)
class ListLevelsQuery(MoraEvent):
    pass


@dataclass(frozen=True)
class ListLevelsEvent(MoraEvent):
    levels: list[str] | None


@dataclass(frozen=True)
class SaveLevelCommand(MoraEvent):
    id: str


@dataclass(frozen=True)
class LoadLevelCommand(MoraEvent):
    id: str


class NavAction(Enum):
    FIRST = auto()
    PREVIOUS = auto()
    NEXT = auto()
    LAST = auto()
