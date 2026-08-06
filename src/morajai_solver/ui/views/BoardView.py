import customtkinter as ctk
from itertools import product

from morajai_solver.domain.colors import MoraColor
from morajai_solver.infra.EventDispatcher import EventDispatcher
from morajai_solver.infra.events import MoraEvent
from morajai_solver.ui.components.ColorPalette import ColorPalette
from morajai_solver.ui.components.MoraButton import MoraButton, MoraTargetButton
from morajai_solver.ui.game_modes import MoraMode
from morajai_solver.ui.ui_colors import UITheme


class BoardView(ctk.CTkFrame):
    buttons: list[MoraButton]
    targets: list[MoraTargetButton]
    palette: ColorPalette

    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        self.dispatcher = EventDispatcher()
        self.buttons = []
        self.targets = []

        self.dispatcher.subscribe(MoraEvent.MODE_CHANGED, self._on_mode_changed)
        self.dispatcher.subscribe(MoraEvent.BOARD_UPDATED, self._on_board_updated)

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
                on_color_changed=self._on_tile_color_changed,
                on_tile_clicked=self._on_tile_clicked,
            )
            button.grid(row=r + 1, column=c + 1, padx=6, pady=6)
            self.buttons.append(button)

        # Cibles aux 4 coins (Grille virtuelle 5x5 de 0 à 4)
        CORNER_TARGETS = [
            {"row": 0, "column": 0, "logical_row": 1, "logical_column": 1},
            {"row": 0, "column": 4, "logical_row": 1, "logical_column": 3},
            {"row": 4, "column": 4, "logical_row": 3, "logical_column": 3},
            {"row": 4, "column": 0, "logical_row": 3, "logical_column": 1},
        ]

        for target_pos in CORNER_TARGETS:
            target = MoraTargetButton(
                grid_frame,
                target_pos["logical_row"],
                target_pos["logical_column"],
                on_color_changed=self._on_target_color_changed,
            )
            target.grid(row=target_pos["row"], column=target_pos["column"])
            self.targets.append(target)

        self.palette = ColorPalette(
            outer_frame, on_color_selected=self._on_brush_color_changed
        )
        self.palette.pack(fill="x", padx=15, pady=(0, 15))

        # --- Mount ---
        self._on_mode_changed(MoraMode.CONFIG)
        self._on_brush_color_changed(MoraColor.GREY)

    # --- TRANSMISSION DE l'IHM VERS LE DISPATCHER ---
    def _on_tile_color_changed(self, r: int, c: int, color: MoraColor) -> None:
        self.dispatcher.emit(MoraEvent.TILE_COLOR_CHANGED, r=r, c=c, color=color)

    def _on_target_color_changed(self, r: int, c: int, color: MoraColor) -> None:
        self.dispatcher.emit(MoraEvent.TARGET_COLOR_CHANGED, r=r, c=c, color=color)

    def _on_tile_clicked(self, r: int, c: int, color: MoraColor) -> None:
        self.dispatcher.emit(MoraEvent.TILE_CLICKED, r=r, c=c, color=color)

    # --- RECEPTION DES ÉVÉNEMENTS GLOBAUX & RÉPARTITION VERS LES ENFANTS ---
    def _on_mode_changed(self, new_mode: MoraMode) -> None:
        self.palette.set_mode(new_mode)
        for btn in self.buttons + self.targets:
            btn.set_mode(new_mode)

    def _on_brush_color_changed(self, color: MoraColor) -> None:
        for btn in self.buttons + self.targets:
            btn.set_brush_color(color)

    def _on_board_updated(self, board_state: dict, targets: dict | None = None) -> None:
        for btn in self.buttons:
            if (btn.r, btn.c) in board_state:
                btn.set_color(board_state[btn.r, btn.c])

        if not targets:
            return

        for target in self.targets:
            if (target.r, target.c) in targets:
                target.set_color(targets[target.r, target.c])
