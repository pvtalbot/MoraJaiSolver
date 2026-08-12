import time

import pytest

from morajai_solver.domain.colors import MoraColor
from morajai_solver.domain.game_engine import GameEngine
from morajai_solver.infra.event_dispatcher import EventDispatcher
from morajai_solver.infra.events import MoraEvent
from morajai_solver.ui.gui import launch_gui
from morajai_solver.ui.ui_colors import UITheme


@pytest.fixture
def app_env():
    bus = EventDispatcher()
    engine = GameEngine(bus)

    app = launch_gui(ui_bus=bus)
    app.withdraw()
    app.update()

    yield app, bus, engine

    app.destroy()


@pytest.fixture
def event_spy(app_env):
    _, bus, _ = app_env
    emitted_events = []
    original_emit = bus.emit

    def spy_emit(event, **kwargs):
        emitted_events.append((event, kwargs))
        original_emit(event, **kwargs)

    bus.emit = spy_emit
    return emitted_events


def test_full_game_scenario(app_env, event_spy):
    app, _, engine = app_env

    initial_grid = {
        (1, 1): MoraColor.GREEN,
        (1, 2): MoraColor.WHITE,
        (1, 3): MoraColor.WHITE,
        (2, 1): MoraColor.BLACK,
        (2, 2): MoraColor.WHITE,
        (2, 3): MoraColor.BLACK,
        (3, 1): MoraColor.BLUE,
        (3, 2): MoraColor.WHITE,
        (3, 3): MoraColor.BLUE,
    }

    # --- 1. Tiles color selection ---
    for coord, color in initial_grid.items():
        app.board_panel.palette.buttons[color]._command()
        app.board_panel.buttons[coord]._command()
        app.update()
    app.board_panel.palette.buttons[MoraColor.BLUE]._command()
    app.update()

    # --- 2. Targets color selection ---
    for coord in ((1, 1), (1, 3), (3, 1), (3, 3)):
        app.board_panel.targets[coord]._command()
        app.update()

    # --- 3. switch to Play mode ---
    app.center_panel.control_panel.mode_selector._command("Play")
    app.update()

    # VALIDATION 1
    # - BOARD_READY was emitted
    # - Tiles are of the expected color
    assert event_spy[-1][0] == MoraEvent.BOARD_READY
    for coord, color in initial_grid.items():
        assert engine.board_manager.board[coord] == color

    # --- 4. switch back to Config mode, and solver execution ---
    event_spy.clear()
    app.center_panel.control_panel.mode_selector._command("Config")
    app.center_panel.control_panel.solve_button._command()
    app.update()

    # Wait for solver to find solution
    time.sleep(0.3)

    # VALIDATION 2
    # - The three expected events have been emitted
    # - The solver found the expected solution
    assert event_spy[-3][0] == MoraEvent.BOARD_READY
    assert event_spy[-2][0] == MoraEvent.SOLVER_START

    expected_solution = [
        (1, 1),
        (1, 2),
        (3, 2),
        (1, 1),
        (1, 2),
        (1, 1),
        (3, 1),
        (3, 3),
        (3, 2),
        (2, 1),
        (1, 2),
    ]
    assert event_spy[-1][0] == MoraEvent.SOLUTION_FOUND
    assert event_spy[-1][1]["steps"] == expected_solution

    # VALIDATION 3
    # - The first step is active
    app.update()
    assert (
        app.solution_panel._step_frames[0].cget("fg_color")
        == UITheme.STEP_ACTIVE_BG.value
    )

    # --- 5. Click on the first correct tile ---
    app.board_panel.buttons[(1, 1)]._command()
    app.update()

    # VALIDATION 4
    # - First step has been validated
    # - Second step is now active
    assert (
        app.solution_panel._step_frames[0].cget("fg_color")
        == UITheme.STEP_SUCCESS_BG.value
    )
    assert (
        app.solution_panel._step_frames[1].cget("fg_color")
        == UITheme.STEP_ACTIVE_BG.value
    )

    # --- 6. Click on the second correct tile ---
    app.board_panel.buttons[(1, 2)]._command()
    app.update()

    # VALIDATION 5
    # - Second step has been validated
    # - Third step is now active
    assert (
        app.solution_panel._step_frames[1].cget("fg_color")
        == UITheme.STEP_SUCCESS_BG.value
    )
    assert (
        app.solution_panel._step_frames[2].cget("fg_color")
        == UITheme.STEP_ACTIVE_BG.value
    )

    # --- 7. Click on incorrect tile ---
    app.board_panel.buttons[(3, 3)]._command()
    app.update()

    # VALIDATION 6
    # - Third step is now in error
    assert (
        app.solution_panel._step_frames[2].cget("fg_color")
        == UITheme.STEP_ERROR_BG.value
    )

    # --- 8. Reset board ---
    event_spy.clear()
    app.center_panel.control_panel.reset_button._command()
    app.update()

    # VALIDATION 7
    # - The event RESET_SAVE has been emitted
    # - All steps have been reinitialised
    assert event_spy[-2][0] == MoraEvent.RESET_SAVE
    assert (
        app.solution_panel._step_frames[0].cget("fg_color")
        == UITheme.STEP_ACTIVE_BG.value
    )
    assert (
        app.solution_panel._step_frames[1].cget("fg_color")
        == UITheme.BG_TILE_CONTAINER.value
    )
    assert (
        app.solution_panel._step_frames[2].cget("fg_color")
        == UITheme.BG_TILE_CONTAINER.value
    )

    # --- 9. Play all correct moves
    event_spy.clear()
    for move in expected_solution:
        app.board_panel.buttons[move]._command()
        app.update()

    # VALIDATION 8
    # - All steps are in success
    # - The event VICTORY_ACHIEVED was emitted
    # - The VICTOIRE message is in the console
    for step in app.solution_panel._step_frames:
        assert step.cget("fg_color") == UITheme.STEP_SUCCESS_BG.value
    assert event_spy[-1][0] == MoraEvent.VICTORY_ACHIEVED

    console_text = app.center_panel.control_panel.log_box.get("1.0", "end")
    assert "> VICTOIRE !" in console_text
