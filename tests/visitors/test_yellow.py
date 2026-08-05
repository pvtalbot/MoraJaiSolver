from morajai_solver.domain.MovementVisitors import YellowVisitor
from morajai_solver.models.MoraBoard import (
    AbstractMoraBoard,
    BitmaskMoraBoard,
    DictMoraBoard,
)
from morajai_solver.domain.colors import MoraColor


def moves_up(board: AbstractMoraBoard, r, c):
    board[r, c] = MoraColor.YELLOW
    board[r - 1, c] = MoraColor.WHITE

    visitor = YellowVisitor()
    board.accept(visitor, (r, c))

    assert board[r - 1, c] == MoraColor.YELLOW
    assert board[r, c] == MoraColor.WHITE


def test_moves_up_dict():
    for r in (2, 3):
        for c in range(1, 4):
            moves_up(DictMoraBoard(), r, c)


def test_moves_up_bitmaks():
    for r in (2, 3):
        for c in range(1, 4):
            moves_up(BitmaskMoraBoard(), r, c)


def on_edge(board: AbstractMoraBoard, c):
    board = BitmaskMoraBoard()
    board[1, c] = MoraColor.YELLOW

    visitor = YellowVisitor()
    board.accept(visitor, (1, c))

    assert board[1, c] == MoraColor.YELLOW


def test_on_edge_dict():
    for c in range(1, 4):
        on_edge(DictMoraBoard(), c)


def test_on_edge_bitmask():
    for c in range(1, 4):
        on_edge(BitmaskMoraBoard(), c)
