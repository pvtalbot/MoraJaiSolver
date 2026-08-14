import queue

import customtkinter as ctk

from morajai_solver.infra.event_dispatcher import EventDispatcher
from morajai_solver.infra.events import (
    PlayTileCommand,
    RandomizeBoardCommand,
    ResetGameCommand,
    SolutionFoundEvent,
    SolutionInvalidatedEvent,
)
from morajai_solver.models.types import Coord
from morajai_solver.ui.ui_colors import UITheme


class SolutionPanel(ctk.CTkFrame):
    def __init__(self, master, ui_bus: EventDispatcher, **kwargs):
        super().__init__(
            master, fg_color=UITheme.BG_PANEL.value, corner_radius=10, **kwargs
        )

        self.dispatcher = ui_bus
        self.queue: queue.Queue = queue.Queue()

        self._steps: list[Coord] | None = list()
        self._current_step_index = 0
        self._step_frames: list[ctk.CTkFrame] = list()
        self._has_error = False
        self._solution_displayed = False

        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=15, pady=(10, 5))
        title = ctk.CTkLabel(header_frame, text="Solution", font=("Arial", 14, "bold"))
        title.pack(side="left")

        self.scroll_frame = ctk.CTkScrollableFrame(
            self, fg_color=UITheme.BG_CONSOLE.value, corner_radius=6
        )
        self.scroll_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        self._create_placeholder()

        self.dispatcher.subscribe(SolutionFoundEvent, self._on_solution_found)
        self.dispatcher.subscribe(RandomizeBoardCommand, self._clear_solution)
        self.dispatcher.subscribe(ResetGameCommand, self._reset_progress)
        self.dispatcher.subscribe(PlayTileCommand, self._on_tile_clicked)
        self.dispatcher.subscribe(SolutionInvalidatedEvent, self._clear_solution)

    # --- Helpers ---
    def _create_placeholder(self):
        self.placeholder = ctk.CTkLabel(
            self.scroll_frame,
            text="Aucune solution calculée.",
            font=("Arial", 12, "italic"),
            text_color=UITheme.TEXT_MUTED.value,
        )
        self.placeholder.pack(expand=True, pady=40)

    def _clear_solution(self, _):
        if not self._solution_displayed:
            return

        self._steps = list()
        self._current_step_index = 0
        self._step_frames = list()
        self._has_error = False
        self._solution_displayed = False

        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        self._create_placeholder()

    def _on_solution_found(self, event: SolutionFoundEvent):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        self._steps = event.result
        self._current_step_index = 0
        self._step_frames = []
        self._has_error = False
        self._solution_displayed = True

        if self._steps is None:
            label = ctk.CTkLabel(
                self.scroll_frame,
                text="Pas de solution possible",
                font=("Arial", 13, "bold"),
            )
            label.pack(pady=20)
            return

        if not self._steps:
            label = ctk.CTkLabel(
                self.scroll_frame,
                text="La grille est déjà résolue !",
                font=("Arial", 13, "bold"),
            )
            label.pack(pady=20)
            return

        for i, (r, c) in enumerate(self._steps, 1):
            step_frame = ctk.CTkFrame(
                self.scroll_frame,
                fg_color=UITheme.BG_TILE_CONTAINER.value,
                corner_radius=6,
                height=35,
            )
            step_frame.pack(fill="x", padx=5, pady=4)
            step_frame.pack_propagate(False)

            num_lbl = ctk.CTkLabel(
                step_frame,
                text=f" {i} ",
                font=("Arial", 12, "bold"),
                fg_color=UITheme.STEP_NUMBER_BG.value,
                text_color=UITheme.TEXT_WHITE.value,
                corner_radius=4,
            )
            num_lbl.pack(side="left", padx=8, pady=5)

            text_lbl = ctk.CTkLabel(
                step_frame, text=f"Cliquer sur la case {r}, {c}", font=("Arial", 12)
            )
            text_lbl.pack(side="left", padx=5)

            self._step_frames.append(step_frame)

        self._update_steps_highlighting()

    def _on_tile_clicked(self, event: PlayTileCommand):
        if not self._steps or self._has_error:
            return
        if self._current_step_index >= len(self._steps):
            return
        if event.position == self._steps[self._current_step_index]:
            self._current_step_index += 1
            self._update_steps_highlighting()
        else:
            self._has_error = True
            self._update_steps_highlighting()

    def _update_steps_highlighting(self):
        for i, frame in enumerate(self._step_frames):
            if i < self._current_step_index:
                frame.configure(fg_color=UITheme.STEP_SUCCESS_BG.value, border_width=0)
            elif i == self._current_step_index:
                if self._has_error:
                    frame.configure(
                        fg_color=UITheme.STEP_ERROR_BG.value,
                        border_width=2,
                        border_color=UITheme.STEP_ERROR_BORDER.value,
                    )
                else:
                    frame.configure(
                        fg_color=UITheme.STEP_ACTIVE_BG.value,
                        border_width=2,
                        border_color=UITheme.STEP_ACTIVE_BORDER.value,
                    )
                    self.scroll_frame._parent_canvas.yview_moveto(
                        max(0, i - 2) / len(self._step_frames) * 0.8
                    )
            else:
                frame.configure(
                    fg_color=UITheme.BG_TILE_CONTAINER.value, border_width=0
                )

    # --- Event handlers ---
    def _reset_progress(self, _):
        self._current_step_index = 0
        self._has_error = False
        self._update_steps_highlighting()
