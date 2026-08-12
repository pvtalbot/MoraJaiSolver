import pytest
import customtkinter as ctk

from morajai_solver.infra.event_dispatcher import EventDispatcher
from morajai_solver.infra.events import MoraEvent
from morajai_solver.ui.panels.control_panel import ControlPanel


@pytest.fixture
def control_panel_env():
    root = ctk.CTk()
    bus = EventDispatcher()
    panel = ControlPanel(root, bus)

    yield panel, bus, root

    root.destroy()


@pytest.fixture
def event_spy(control_panel_env):
    _, bus, _ = control_panel_env
    emitted_events = []
    original_emit = bus.emit

    def spy_emit(event, **kwargs):
        emitted_events.append((event, kwargs))
        original_emit(event, **kwargs)

    bus.emit = spy_emit
    return emitted_events


def test_solve_button_disables_controls_and_emits_start(control_panel_env, event_spy):
    panel, bus, _ = control_panel_env
    bus.subscribe(MoraEvent.SOLVER_START, lambda: None)

    panel.solve_button._command()
    assert panel.solve_button.cget("state") == "disabled"
    assert panel.mode_selector.cget("state") == "disabled"
    assert event_spy[-1][0] == MoraEvent.SOLVER_START


def test_solution_found(control_panel_env):
    panel, _, root = control_panel_env
    panel.solve_button.configure(state="disabled")
    steps = [(1, 1), (1, 2)]

    panel._on_solution_found(steps)
    panel._check_queue()
    root.update()

    console_text = panel.log_box.get("1.0", "end")
    assert "Solution trouvée en 2 coups" in console_text
    assert panel.solve_button.cget("state") == "normal"
