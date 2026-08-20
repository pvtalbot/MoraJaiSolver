import customtkinter as ctk
import pytest

from morajai_solver.infra.event_dispatcher import EventDispatcher
from morajai_solver.infra.events import SolutionFoundEvent, StartSolverCommand
from morajai_solver.ui.modules.control_panel import ControlPanel


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
    emitted_events = list()
    original_emit = bus.emit

    def spy_emit(event):
        emitted_events.append(event)
        original_emit(event)

    bus.emit = spy_emit
    return emitted_events


def test_solve_button_disables_controls_and_emits_start(control_panel_env, event_spy):
    panel, bus, _ = control_panel_env
    bus.subscribe(StartSolverCommand, lambda _: None)

    panel.solution_display.solve_button._command()
    assert panel.solution_display.solve_button.cget("state") == "disabled"
    assert panel.nav_bar.btn_first.cget("state") == "disabled"
    assert panel.nav_bar.btn_prev.cget("state") == "disabled"
    assert panel.nav_bar.btn_next.cget("state") == "disabled"
    assert panel.nav_bar.btn_last.cget("state") == "disabled"

    assert StartSolverCommand in [type(e) for e in event_spy]


def test_solution_found(control_panel_env):
    panel, _, root = control_panel_env
    panel.solution_display.solve_button.configure(state="disabled")
    panel.nav_bar.change_state("disabled")
    steps = [(1, 1), (1, 2)]

    panel._on_solution_found(SolutionFoundEvent(result=steps))
    root.update()

    console_text = panel.log_box.get("1.0", "end")
    # Log box displays the right message
    assert "Solution trouvée en 2 coups" in console_text

    # No button is disabled
    assert panel.solution_display.solve_button.cget("state") == "normal"
    assert panel.nav_bar.btn_first.cget("state") == "normal"
    assert panel.nav_bar.btn_prev.cget("state") == "normal"
    assert panel.nav_bar.btn_next.cget("state") == "normal"
    assert panel.nav_bar.btn_last.cget("state") == "normal"

    # There is the right number of steps displayed
    assert len(panel.solution_display._step_frames) == 2
