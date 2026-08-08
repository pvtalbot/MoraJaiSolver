import customtkinter as ctk
from itertools import product

from morajai_solver.domain.colors import MoraColor
from morajai_solver.infra.event_dispatcher import EventDispatcher
from morajai_solver.infra.events import MoraEvent
from morajai_solver.models.types import Coord
from morajai_solver.ui.components.color_palette import ColorPalette
from morajai_solver.ui.components.mora_button import MoraButton, MoraTargetButton
from morajai_solver.ui.game_modes import MoraMode
from morajai_solver.ui.ui_colors import UITheme


class BoardPanel(ctk.CTkFrame):
    buttons: dict[Coord, MoraButton]
    targets: dict[Coord, MoraTargetButton]
    palette: ColorPalette
    mode: MoraMode
    color_selected: MoraColor

    def __init__(self, master, ui_bus: EventDispatcher, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        self.dispatcher = ui_bus
        self.buttons = dict()
        self.targets = dict()
        self.mode = MoraMode.CONFIG
        self.color_selected = MoraColor.GREY
        self._solution_found = False

        self.dispatcher.subscribe(MoraEvent.MODE_CHANGED, self._on_mode_changed)
        self.dispatcher.subscribe(MoraEvent.BOARD_UPDATED, self._on_board_updated)
        self.dispatcher.subscribe(MoraEvent.SOLUTION_FOUND, self._on_solution_found)

        outer_frame = ctk.CTkFrame(
            self, fg_color=UITheme.BG_PANEL.value, corner_radius=10
        )
        outer_frame.pack(anchor="center", pady=10)

        grid_frame = ctk.CTkFrame(
            outer_frame, fg_color=UITheme.BG_PANEL.value, corner_radius=10
        )
        grid_frame.pack(padx=10, pady=10)

        # Grille 3x3 : on passe les coordonnées row/column aux boutons
        for r, c in product(range(3), range(3)):
            button = MoraButton(
                grid_frame,
                r + 1,
                c + 1,
                on_tile_clicked=self._on_tile_clicked,
            )
            button.grid(row=r + 1, column=c + 1, padx=6, pady=6)
            self.buttons[r + 1, c + 1] = button

        # Cibles aux 4 coins (Grille virtuelle 5x5 de 0 à 4)
        CORNER_TARGETS = [
            {"row": 0, "column": 0, "logical_row": 1, "logical_column": 1},
            {"row": 0, "column": 4, "logical_row": 1, "logical_column": 3},
            {"row": 4, "column": 4, "logical_row": 3, "logical_column": 3},
            {"row": 4, "column": 0, "logical_row": 3, "logical_column": 1},
        ]

        for target_pos in CORNER_TARGETS:
            r, c, lr, lc = target_pos.values()
            target = MoraTargetButton(grid_frame, lr, lc, self._on_target_clicked)
            target.grid(row=r, column=c)
            self.targets[lr, lc] = target

        initial_color = MoraColor.GREY
        self.palette = ColorPalette(
            outer_frame,
            on_color_selected=self._on_brush_color_changed,
            initial_color=initial_color,
        )
        self.palette.pack(fill="x", padx=15, pady=(0, 15))

        # --- Mount ---
        self._on_mode_changed(MoraMode.CONFIG)
        self._on_brush_color_changed(initial_color)

    # --- TRANSMISSION DE l'IHM VERS LE DISPATCHER ---
    def _on_tile_clicked(self, r: int, c: int) -> None:
        if self.mode == MoraMode.CONFIG:
            self.buttons[r, c].set_color(self.color_selected)

            if self._solution_found:
                self.dispatcher.emit(MoraEvent.SOLUTION_INVALIDATED)
                self._solution_found = False
        else:
            self.dispatcher.emit(MoraEvent.TILE_CLICKED, r=r, c=c)

    def _on_target_clicked(self, r: int, c: int) -> None:
        if self.mode == MoraMode.CONFIG:
            self.targets[r, c].set_color(self.color_selected)

            if self._solution_found:
                self.dispatcher.emit(MoraEvent.SOLUTION_INVALIDATED)
                self._solution_found = False

    def _board_ready(self) -> None:
        board_state = {k: btn._current_color for k, btn in self.buttons.items()}
        targets_state = {k: btn._current_color for k, btn in self.targets.items()}
        self.dispatcher.emit(
            MoraEvent.BOARD_READY, board_state=board_state, targets=targets_state
        )

    # --- RECEPTION DES ÉVÉNEMENTS GLOBAUX & RÉPARTITION VERS LES ENFANTS ---
    def _on_mode_changed(self, new_mode: MoraMode) -> None:
        self.mode = new_mode
        self.palette.set_mode(new_mode)
        if new_mode == MoraMode.PLAY:
            self._board_ready()

    def _on_brush_color_changed(self, color: MoraColor) -> None:
        self.color_selected = color

    def _on_board_updated(self, board_state: dict, targets: dict | None = None) -> None:
        for btn in self.buttons:
            self.buttons[btn].set_color(board_state[btn])

        if not targets:
            return

        for target in self.targets:
            self.targets[target].set_color(targets[target])

    def _on_solution_found(self, steps):
        self._solution_found = True
