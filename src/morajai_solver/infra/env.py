from pathlib import Path
import sys


IS_DEV_MODE = not getattr(sys, "frozen", False)


def get_levels_dir() -> Path:
    if not IS_DEV_MODE:
        base_dir = Path(getattr(sys, "_MEIPASS", Path(sys.executable).parent))
    else:
        base_dir = Path(__file__).resolve().parent.parent

    levels_dir = base_dir / "data" / "levels"
    levels_dir.mkdir(parents=True, exist_ok=True)

    return levels_dir
