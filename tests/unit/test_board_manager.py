from morajai_solver.domain.board_manager import BoardManager


def test_truncates_history():
    board_manager = BoardManager()
    board_manager.load_state_from_dict({}, {})
    assert len(board_manager.moves) == 1
    board_manager.play_move((1, 1))
    board_manager.play_move((1, 2))
    board_manager.play_move((1, 3))
    assert len(board_manager.moves) == 4

    board_manager.force_move(1)
    assert board_manager.index == 1

    board_manager.play_move((2, 2))
    assert len(board_manager.moves) == 3
    assert board_manager.index == 2


def test_negative_indexes():
    board_manager = BoardManager()
    board_manager.load_state_from_dict({}, {})

    board_manager.play_move((1, 1))
    board_manager.play_move((1, 2))
    board_manager.force_move(0)
    board_manager.force_move(-1)
    assert board_manager.index == 2

    board_manager.force_move(-len(board_manager.moves))
    assert board_manager.index == 0


def test_reset_action():
    board_manager = BoardManager()
    board_manager.load_state_from_dict({}, {})

    board_manager.play_move((1, 1))
    board_manager.play_move((1, 2))

    board_manager.reset()
    assert board_manager.index == 0
    assert len(board_manager.moves) == 1


def test_randomize_action():
    board_manager = BoardManager()
    board_manager.load_state_from_dict({}, {})

    board_manager.play_move((1, 1))
    board_manager.play_move((1, 2))

    board_manager.randomize()
    assert board_manager.index == 0
    assert len(board_manager.moves) == 1
