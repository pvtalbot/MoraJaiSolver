from morajai_solver.models.mora_board import MoraBoard

STORED_BOARDS = {
    "Board 1": {"board": "0x919212116", "targets": "0x909000909"},
    "Board 2": {"board": "0x706599997", "targets": "0x909000909"},
    "Board 3": {"board": "0x868561308", "targets": "0x303000303"},
    "Board 4": {"board": "0x338141873", "targets": "0x0"},
    "Board 5": {"board": "0x567119788", "targets": "0x707000707"},
}


def get_board(params: dict[str, str]):
    board = MoraBoard()
    board.data = int(params["board"], 16)
    board.target_state = int(params["targets"], 16)

    return board


PRESET_BOARDS = [(k, get_board(STORED_BOARDS[k])) for k in STORED_BOARDS]
