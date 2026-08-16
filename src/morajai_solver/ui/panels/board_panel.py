import customtkinter as ctk

from morajai_solver.domain.colors import MoraColor
from morajai_solver.infra.event_dispatcher import EventDispatcher
from morajai_solver.infra.events import (
    BoardLoadedEvent,
    BoardUpdatedEvent,
    HighlightTileCommand,
    ModeChangedEvent,
    PlayTileCommand,
    SolutionFoundEvent,
    SolutionInvalidatedEvent,
    SubmitBoardCommand,
    SubmitRequiredEvent,
    VictoryAchievedEvent,
)
from morajai_solver.models.types import Coord
from morajai_solver.ui.components.color_palette import ColorPalette
from morajai_solver.ui.components.mora_button import (
    AbstractMoraButton,
    MoraTargetButton,
    MoraTileButton,
)
from morajai_solver.ui.game_modes import MoraMode
from morajai_solver.ui.ui_colors import UITheme


class BoardPanel(ctk.CTkFrame):
    buttons: dict[Coord, MoraTileButton]
    targets: dict[Coord, MoraTargetButton]
    palette: ColorPalette
    mode: MoraMode
    color_selected: MoraColor
    _highlighted: Coord | None

    def __init__(self, master, ui_bus: EventDispatcher, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        self.dispatcher = ui_bus
        self._solution_found = False
        self.color_selected = MoraColor.GREY
        self.buttons = dict()
        self.targets = dict()
        self._highlighted = None

        self._setup_ui()

        self.dispatcher.subscribe(ModeChangedEvent, self._on_mode_changed)
        self.dispatcher.subscribe(BoardUpdatedEvent, self._on_board_updated)
        self.dispatcher.subscribe(BoardLoadedEvent, self._on_board_loaded)
        self.dispatcher.subscribe(SolutionFoundEvent, self._on_solution_found)
        self.dispatcher.subscribe(SubmitRequiredEvent, self._on_submit_required)
        self.dispatcher.subscribe(HighlightTileCommand, self._on_highlight_tile)
        self.dispatcher.subscribe(VictoryAchievedEvent, self._on_victory_achieved)

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

    # --- Click handlers & helpers ---
    def _on_tile_clicked(self, r: int, c: int) -> None:
        self._on_element_clicked(self.buttons[r, c])
        if self.mode == MoraMode.PLAY:
            self.dispatcher.emit(PlayTileCommand((r, c)))
        elif self._highlighted is not None:
            self._clean_highlighted()

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

    def _clean_highlighted(self):
        if self._highlighted:
            self.buttons[self._highlighted].unhighlight()
            self._highlighted = None

    # --- Event handlers ---
    def _on_mode_changed(self, event: ModeChangedEvent) -> None:
        self.mode = event.mode
        self.palette.set_mode(event.mode)

    def _on_submit_required(self, _) -> None:
        board_state = {k: btn._current_color for k, btn in self.buttons.items()}
        targets_state = {k: btn._current_color for k, btn in self.targets.items()}
        self.dispatcher.emit(
            SubmitBoardCommand(board=board_state, targets=targets_state)
        )

    def _on_board_updated(self, event: BoardUpdatedEvent) -> None:
        for btn in self.buttons:
            self.buttons[btn].set_color(event.board[btn])

    def _on_board_loaded(self, event: BoardLoadedEvent) -> None:
        for btn in self.buttons:
            self.buttons[btn].set_color(event.board[btn])
        for target in self.targets:
            self.targets[target].set_color(event.targets[target])
        self._clean_highlighted()

    def _on_solution_found(self, _):
        self._solution_found = True

    def _on_highlight_tile(self, event: HighlightTileCommand):
        if self._highlighted:
            self.buttons[self._highlighted].unhighlight()
            self._higlighted = None

        if not event.coord:
            return
        self.buttons[event.coord].hightlight()
        self._highlighted = event.coord

    def _on_victory_achieved(self, _):
        self._clean_highlighted()
