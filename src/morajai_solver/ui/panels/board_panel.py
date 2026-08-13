import customtkinter as ctk

from morajai_solver.domain.colors import MoraColor
from morajai_solver.infra.event_dispatcher import EventDispatcher
from morajai_solver.infra.events import (
    SubmitBoardCommand,
    BoardUpdatedEvent,
    ModeChangedEvent,
    SolutionFoundEvent,
    SolutionInvalidatedEvent,
    PlayTileCommand,
    SubmitRequiredEvent,
)
from morajai_solver.models.types import Coord
from morajai_solver.ui.components.color_palette import ColorPalette
from morajai_solver.ui.components.mora_button import (
    AbstractMoraButton,
    MoraTileButton,
    MoraTargetButton,
)
from morajai_solver.ui.game_modes import MoraMode
from morajai_solver.ui.ui_colors import UITheme


class BoardPanel(ctk.CTkFrame):
    buttons: dict[Coord, MoraTileButton]
    targets: dict[Coord, MoraTargetButton]
    palette: ColorPalette
    mode: MoraMode
    color_selected: MoraColor

    def __init__(self, master, ui_bus: EventDispatcher, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        self.dispatcher = ui_bus
        self._solution_found = False
        self.color_selected = MoraColor.GREY
        self.buttons = dict()
        self.targets = dict()

        self._setup_ui()

        self.dispatcher.subscribe(ModeChangedEvent, self._on_mode_changed)
        self.dispatcher.subscribe(BoardUpdatedEvent, self._on_board_updated)
        self.dispatcher.subscribe(SolutionFoundEvent, self._on_solution_found)
        self.dispatcher.subscribe(SubmitRequiredEvent, self._on_submit_required)

        # --- Mount ---
        self._on_mode_changed(ModeChangedEvent(mode=MoraMode.CONFIG))

    # --- UI setup ---
    def _setup_ui(self):
        outer_frame = ctk.CTkFrame(
            self, fg_color=UITheme.BG_PANEL.value, corner_radius=10
        )
        outer_frame.pack(anchor="center", pady=10)

        grid_frame = ctk.CTkFrame(outer_frame, fg_color="transparent")
        grid_frame.pack(padx=10, pady=10)

        self._create_tiles(grid_frame)
        self._create_targets(grid_frame)

        self.palette = ColorPalette(
            outer_frame,
            on_color_selected=self._on_brush_color_changed,
            initial_color=self.color_selected,
        )
        self.palette.pack(fill="x", padx=15, pady=(0, 15))

    def _create_tiles(self, frame):
        for r in range(1, 4):
            for c in range(1, 4):
                button = MoraTileButton(
                    frame,
                    r,
                    c,
                    on_tile_clicked=self._on_tile_clicked,
                )
                button.grid(row=r, column=c, padx=6, pady=6)
                self.buttons[r, c] = button

    def _create_targets(self, frame):
        CORNER_TARGETS = [
            {"row": 0, "column": 0, "logical_row": 1, "logical_column": 1},
            {"row": 0, "column": 4, "logical_row": 1, "logical_column": 3},
            {"row": 4, "column": 4, "logical_row": 3, "logical_column": 3},
            {"row": 4, "column": 0, "logical_row": 3, "logical_column": 1},
        ]

        for target_pos in CORNER_TARGETS:
            r, c, lr, lc = target_pos.values()
            target = MoraTargetButton(frame, lr, lc, self._on_target_clicked)
            target.grid(row=r, column=c)
            self.targets[lr, lc] = target

    # --- Click handlers ---
    def _on_tile_clicked(self, r: int, c: int) -> None:
        self._on_element_clicked(self.buttons[r, c])
        if self.mode == MoraMode.PLAY:
            self.dispatcher.emit(PlayTileCommand((r, c)))

    def _on_target_clicked(self, r: int, c: int) -> None:
        self._on_element_clicked(self.targets[r, c])

    def _on_element_clicked(self, element: AbstractMoraButton) -> None:
        if self.mode != MoraMode.CONFIG:
            return

        element.set_color(self.color_selected)
        if self._solution_found:
            self.dispatcher.emit(SolutionInvalidatedEvent())
            self._solution_found = False

    def _on_brush_color_changed(self, color: MoraColor) -> None:
        self.color_selected = color

    # --- Event handlers ---
    def _on_mode_changed(self, event: ModeChangedEvent) -> None:
        self.mode = event.mode
        self.palette.set_mode(event.mode)

    def _on_submit_required(self) -> None:
        board_state = {k: btn._current_color for k, btn in self.buttons.items()}
        targets_state = {k: btn._current_color for k, btn in self.targets.items()}
        self.dispatcher.emit(
            SubmitBoardCommand(board=board_state, targets=targets_state)
        )

    def _on_board_updated(self, event: BoardUpdatedEvent) -> None:
        for btn in self.buttons:
            self.buttons[btn].set_color(event.board[btn])

        if not event.targets:
            return

        for target in self.targets:
            self.targets[target].set_color(event.targets[target])

    def _on_solution_found(self):
        self._solution_found = True
