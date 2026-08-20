import customtkinter as ctk
import pytest

from morajai_solver.domain.game_engine import GameEngine
from morajai_solver.infra.event_dispatcher import EventDispatcher
from morajai_solver.infra.events import (
    ChangeModeCommand,
    ModeChangedEvent,
)
from morajai_solver.ui.game_modes import MoraMode
from morajai_solver.ui.modules.board_panel import BoardPanel
from morajai_solver.ui.modules.top_bar import TopBar


@pytest.fixture
def integration_env():
    root = ctk.CTk()
    bus = EventDispatcher()

    engine = GameEngine(ui_bus=bus)
    top_bar = TopBar(root, ui_bus=bus)
    BoardPanel(root, ui_bus=bus)

    yield bus, engine, top_bar

    root.destroy()


@pytest.fixture
def event_spy(integration_env):
    bus, _, _ = integration_env
    emitted_events = list()
    original_emit = bus.emit

    def spy_emit(event):
        emitted_events.append(event)
        original_emit(event)

    bus.emit = spy_emit
    return emitted_events


def test_mode_changes(integration_env, event_spy):
    bus, engine, top_bar = integration_env
    top_bar.edit_switch.select()

    assert engine.board_manager.moves == []
    bus.emit(ChangeModeCommand(MoraMode.PLAY))

    assert top_bar.edit_switch.get() == MoraMode.PLAY.value
    assert ModeChangedEvent in [type(e) for e in event_spy]
    assert engine.board_manager.moves == [0]
