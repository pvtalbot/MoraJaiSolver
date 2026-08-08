import json
from pathlib import Path

from morajai_solver.infra.env import IS_DEV_MODE, get_levels_dir
from morajai_solver.models.mora_board import MoraBoard


class JsonBoardRepository:
    def __init__(self) -> None:
        self._levels_dir = get_levels_dir()

    def load(self, board_id: str) -> MoraBoard | None:
        file_path = self._levels_dir / f"{board_id}.json"
        if not file_path.exists():
            return None

        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        board = (
            int(data["board"], 16) if isinstance(data["board"], str) else data["board"]
        )
        target = (
            int(data["target"], 16)
            if isinstance(data["target"], str)
            else data["target"]
        )

        result = MoraBoard(board)
        result.target_state = target

        return result

    def save(self, board_id: str, board: MoraBoard) -> Path:
        if not IS_DEV_MODE:
            raise PermissionError("Forbidden")

        file_path = self._levels_dir / f"{board_id}.json"
        payload = {
            "id": board_id,
            "board": hex(board.data),
            "target": hex(board.target_state),
        }

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(payload, file, indent=2)

        return file_path

    def list_available_boards(self) -> list[str]:
        if not self._levels_dir.exists():
            return []
        return [f.stem for f in self._levels_dir.glob("*.json")]
