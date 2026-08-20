import pytest

from morajai_solver.domain.colors import MoraColor
from morajai_solver.domain.game_engine import GameEngine
from morajai_solver.infra.event_dispatcher import EventDispatcher
from morajai_solver.infra.events import (
    JumpToStepCommand,
    RegisterBoardCommand,
    SolutionFoundEvent,
    StartSolverCommand,
    VictoryAchievedEvent,
)
from morajai_solver.ui.gui import launch_gui
from morajai_solver.ui.ui_colors import UITheme


@pytest.fixture
def app_env(monkeypatch):
    bus = EventDispatcher()

    # No multithreading during testing.
    # The event will start the solver synchronously.
    def mock_solver_start(self, _):
        self._run_solver()

    monkeypatch.setattr(GameEngine, "_on_solver_start", mock_solver_start)

    engine = GameEngine(bus)

    app = launch_gui(ui_bus=bus)
    bus.configure_ctk_root(app)
    app.withdraw()
    app.update()

    yield app, bus, engine

    app.destroy()


@pytest.fixture
def event_spy(app_env):
    _, bus, _ = app_env
    emitted_events = list()
    original_emit = bus.emit

    def spy_emit(event):
        emitted_events.append(event)
        original_emit(event)

    bus.emit = spy_emit
    return emitted_events


def test_full_game_scenario(app_env, event_spy):
    app, bus, engine = app_env

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
    app.top_bar.edit_switch.deselect()
    app.top_bar.edit_switch._command()
    app.update()

    # VALIDATION 1
    # - BOARD_READY was emitted
    # - Tiles are of the expected color
    assert RegisterBoardCommand in [type(e) for e in event_spy]
    for coord, color in initial_grid.items():
        assert engine.board_manager.board[coord] == color

    # --- 4. switch back to Config mode, and solver execution ---
    event_spy.clear()
    app.top_bar.edit_switch.deselect()
    app.control_panel.solution_display.solve_button._command()
    app.update()

    # VALIDATION 2
    # - The three expected events have been emitted
    # - The solver found the expected solution
    event_types = [type(e) for e in event_spy]
    assert RegisterBoardCommand in event_types
    assert StartSolverCommand in event_types

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
    assert SolutionFoundEvent in event_types
    steps = None
    for e in event_spy:
        if isinstance(e, SolutionFoundEvent):
            steps = e.result
            break

    assert steps == expected_solution

    bus._flush_async_queue(None)

    # VALIDATION 3
    # - The first step is active
    app.update()
    assert (
        app.control_panel.solution_display._step_frames[0].cget("fg_color")
        == UITheme.STEP_ACTIVE_BG.value
    )

    # --- 5. Click on the first correct tile ---
    app.board_panel.buttons[(1, 1)]._command()
    app.update()

    # VALIDATION 4
    # - First step has been validated
    # - Second step is now active
    assert (
        app.control_panel.solution_display._step_frames[0].cget("fg_color")
        == UITheme.STEP_SUCCESS_BG.value
    )
    assert (
        app.control_panel.solution_display._step_frames[1].cget("fg_color")
        == UITheme.STEP_ACTIVE_BG.value
    )

    # --- 6. Click on the second correct tile ---
    app.board_panel.buttons[(1, 2)]._command()
    app.update()

    # VALIDATION 5
    # - Second step has been validated
    # - Third step is now active
    assert (
        app.control_panel.solution_display._step_frames[1].cget("fg_color")
        == UITheme.STEP_SUCCESS_BG.value
    )
    assert (
        app.control_panel.solution_display._step_frames[2].cget("fg_color")
        == UITheme.STEP_ACTIVE_BG.value
    )

    # --- 7. Click on incorrect tile ---
    app.board_panel.buttons[(3, 3)]._command()
    app.update()

    # VALIDATION 6
    # - Third step is now in error
    assert (
        app.control_panel.solution_display._step_frames[2].cget("fg_color")
        == UITheme.STEP_ERROR_BG.value
    )

    # --- 8. Reset board ---
    event_spy.clear()
    assert (
        app.control_panel.nav_bar.btn_first.cget("fg_color")
        == UITheme.BTN_WARN_BG.value
    )
    app.control_panel.nav_bar.btn_first._command()
    assert (
        app.control_panel.nav_bar.btn_first.cget("fg_color")
        == UITheme.BTN_CONFIG_BG.value
    )
    app.control_panel.nav_bar.btn_first._command()
    app.update()

    # VALIDATION 7
    # - The event RESET_SAVE has been emitted
    # - All steps have been reinitialised
    assert JumpToStepCommand in [type(e) for e in event_spy]
    assert (
        app.control_panel.solution_display._step_frames[0].cget("fg_color")
        == UITheme.STEP_ACTIVE_BG.value
    )
    assert (
        app.control_panel.solution_display._step_frames[1].cget("fg_color")
        == UITheme.BG_TILE_CONTAINER.value
    )
    assert (
        app.control_panel.solution_display._step_frames[2].cget("fg_color")
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
    for step in app.control_panel.solution_display._step_frames:
        assert step.cget("fg_color") == UITheme.STEP_SUCCESS_BG.value
    assert VictoryAchievedEvent in [type(e) for e in event_spy]

    console_text = app.control_panel.log_box.get("1.0", "end")
    assert "> VICTOIRE !" in console_text
