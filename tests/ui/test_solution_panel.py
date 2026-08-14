import customtkinter as ctk
import pytest

from morajai_solver.infra.event_dispatcher import EventDispatcher
from morajai_solver.infra.events import SolutionFoundEvent
from morajai_solver.ui.panels.solution_panel import SolutionPanel


@pytest.fixture
def solution_panel_env():
    root = ctk.CTk()
    bus = EventDispatcher()
    panel = SolutionPanel(root, ui_bus=bus)

    yield panel, root

    root.destroy()


def test_solution_found(solution_panel_env):
    panel, root = solution_panel_env
    steps = [(1, 1), (2, 2), (3, 3)]

    panel._on_solution_found(SolutionFoundEvent(result=steps))
    root.update()

    assert len(panel._step_frames) == 3
