import customtkinter as ctk

from morajai_solver.infra.event_dispatcher import EventDispatcher
from morajai_solver.infra.events import (
    ChangeModeCommand,
    HighlightTileCommand,
    StartSolverCommand,
)
from morajai_solver.models.types import Coord
from morajai_solver.ui.game_modes import MoraMode
from morajai_solver.ui.ui_colors import UITheme


class SolutionDisplay(ctk.CTkFrame):
    def __init__(self, master, ui_bus: EventDispatcher, **kwargs):
        super().__init__(
            master,
            fg_color=UITheme.BG_PANEL.value,
            corner_radius=10,
            height=300,
            **kwargs,
        )

        self.dispatcher = ui_bus
        self._steps: list[Coord] | None = list()
        self._current_step_index = 0
        self._step_frames: list[ctk.CTkFrame] = list()
        self._has_error = False
        self._solution_displayed = False

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.empty_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.empty_frame.grid(row=0, column=0, sticky="nsew")
        self._build_empty_state()

        self.result_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.result_frame.grid(row=0, column=0, sticky="nsew")
        self._build_result_state()

        self.show_empty()

    @property
    def solution_displayed(self):
        return self._solution_displayed

    # --- Helpers ---
    def _build_empty_state(self):
        label = ctk.CTkLabel(
            self.empty_frame,
            text="Aucune solution calculée",
            text_color=UITheme.TEXT_MUTED.value,
            font=("Arial", 14, "italic"),
        )
        label.pack(pady=(30, 10))

        self.solve_button = ctk.CTkButton(
            self.empty_frame,
            text="Solve Box",
            fg_color=UITheme.BTN_SOLVE_BG.value,
            hover_color=UITheme.BTN_SOLVE_HOVER.value,
            command=self._on_solve,
        )
        self.solve_button.pack(pady=5)

    def _build_result_state(self):
        self.scroll_frame = ctk.CTkScrollableFrame(
            self.result_frame, fg_color=UITheme.BG_CONSOLE.value, corner_radius=6
        )
        self.scroll_frame.pack(fill="both", expand=True, pady=5)

    def clear_solution(self):
        if not self._solution_displayed:
            return

        self._steps = list()
        self._current_step_index = 1
        self._step_frames = list()
        self._has_error = False
        self._solution_displayed = False

        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        self.show_empty()

    def display_solution(self, steps: list[Coord] | None):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        self._steps = steps
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
            self.show_steps()
            return

        if not self._steps:
            label = ctk.CTkLabel(
                self.scroll_frame,
                text="La grille est déjà résolue !",
                font=("Arial", 13, "bold"),
            )
            label.pack(pady=20)
            self.show_steps()
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

        self.show_steps()
        self._update_steps_highlighting()

    def next_solution_step(self, pos: Coord):
        if not self._steps or self._has_error:
            return
        if self._current_step_index >= len(self._steps):
            return
        if pos == self._steps[self._current_step_index]:
            self._current_step_index += 1
            self._update_steps_highlighting()
        else:
            self._has_error = True
            self._update_steps_highlighting()
            self.dispatcher.emit(HighlightTileCommand(coord=None))

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
                    assert self._steps is not None
                    self.dispatcher.emit(HighlightTileCommand(coord=self._steps[i]))
            else:
                frame.configure(
                    fg_color=UITheme.BG_TILE_CONTAINER.value, border_width=0
                )

    # --- Event handlers ---
    def reset_progress(self):
        self._current_step_index = 0
        self._has_error = False
        self._update_steps_highlighting()

    def _on_solve(self):
        self.dispatcher.emit(ChangeModeCommand(MoraMode.PLAY))
        self.dispatcher.emit(StartSolverCommand())

    def show_empty(self):
        self.result_frame.grid_remove()
        self.empty_frame.grid(row=0, column=0, sticky="nsew")

    def show_steps(self):
        self.empty_frame.grid_remove()
        self.result_frame.grid(row=0, column=0, sticky="nsew")
