import pytest
import customtkinter as ctk

from morajai_solver.domain.game_engine import GameEngine
from morajai_solver.infra.event_dispatcher import EventDispatcher
from morajai_solver.ui.panels.board_panel import BoardPanel
from morajai_solver.ui.panels.control_panel import ControlPanel


@pytest.fixture
def integration_env():
    root = ctk.CTk()
    bus = EventDispatcher()

    engine = GameEngine(ui_bus=bus)
    control_panel = ControlPanel(root, ui_bus=bus)
    BoardPanel(root, ui_bus=bus)

    yield control_panel, engine

    root.destroy()


def test_mode_changes(integration_env):
    control_panel, engine = integration_env

    assert not hasattr(engine.board_manager, "saved_board")
    control_panel.mode_selector._command("Play")
    assert hasattr(engine.board_manager, "saved_board")
    assert engine.board_manager.saved_board == 0
