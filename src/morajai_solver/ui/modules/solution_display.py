import math
from collections.abc import Callable

import customtkinter as ctk

from morajai_solver.infra.event_dispatcher import EventDispatcher
from morajai_solver.infra.events import (
    ChangeModeCommand,
    HighlightTileCommand,
    StartSolverCommand,
)
from morajai_solver.models.types import Coord
from morajai_solver.ui.components.solution_frame import SolutionFrame
from morajai_solver.ui.game_modes import MoraMode
from morajai_solver.ui.ui_colors import UITheme


class SolutionDisplay(ctk.CTkFrame):
    _current_step_index: int
    _divergence_index: int | float
    _steps: list[Coord] | None
    _step_frames: list[SolutionFrame]
    _solution_displayed: bool
    _on_state_updated: Callable[[tuple[int, int | float]], None] | None

    def __init__(self, master, ui_bus: EventDispatcher, **kwargs):
        super().__init__(
            master,
            fg_color=UITheme.BG_PANEL.value,
            corner_radius=10,
            height=300,
            **kwargs,
        )

        self.dispatcher = ui_bus
        self._on_state_updated = None
        self._init_values()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.empty_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.empty_frame.grid(row=0, column=0, sticky="nsew")
        self._build_empty_state()

        self.result_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.result_frame.grid(row=0, column=0, sticky="nsew")
        self._build_result_state()

        self.show_empty_state()

    def _init_values(self, steps=None):
        self._steps = steps
        self.current_step = 0
        self._step_frames = list()
        self.divergence_index = math.inf
        self._solution_displayed = False

    @property
    def solution_displayed(self):
        return self._solution_displayed

    @property
    def has_error(self):
        return self.divergence_index is not math.inf

    @property
    def current_step(self):
        return self._current_step_index

    @current_step.setter
    def current_step(self, value):
        self._current_step_index = value
        if self._on_state_updated:
            self._on_state_updated((self.current_step, self.divergence_index))

    @property
    def divergence_index(self):
        return self._divergence_index

    @divergence_index.setter
    def divergence_index(self, value):
        self._divergence_index = value
        if self._on_state_updated:
            self._on_state_updated((self.current_step, self.divergence_index))

    def set_on_state_callback(
        self, callback: Callable[[tuple[int, int | float]], None] | None
    ):
        self._on_state_updated = callback

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
        if not self.solution_displayed:
            return

        self._init_values()

        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        self.show_empty_state()

    def display_solution(self, steps: list[Coord] | None):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        self._init_values(steps)
        self._solution_displayed = True

        no_solution = "Pas de solution possible"
        already_solved = "La grille est déjà résolue !"
        if not self._steps:
            label = ctk.CTkLabel(
                self.scroll_frame,
                text=no_solution if self._steps is None else already_solved,
                font=("Arial", 13, "bold"),
            )
            label.pack(pady=20)
            self.show_steps()
            return

        for i, pos in enumerate(self._steps, 1):
            step_frame = SolutionFrame(self.scroll_frame, i, pos)
            step_frame.pack(fill="x", padx=5, pady=4)
            step_frame.pack_propagate(False)
            self._step_frames.append(step_frame)

        self.show_steps()
        self._update_steps_highlighting()

    def go_to_next_step(self, pos: Coord):
        if (
            not self._steps
            or self.current_step >= len(self._steps)
            or self.has_error
            and self.current_step > self.divergence_index
        ):
            pass
        elif pos == self._steps[self.current_step]:
            if self.has_error and self.current_step == self.divergence_index:
                self.divergence_index = math.inf
        else:
            self.divergence_index = self.current_step
        self.current_step += 1
        self._update_steps_highlighting()

    def jump_to_step(self, step):
        if not self._steps:
            return
        self.current_step = step
        self._update_steps_highlighting()

    def _update_steps_highlighting(self):
        break_point = min(self.divergence_index, self.current_step)
        for i, frame in enumerate(self._step_frames):
            if i < break_point:
                frame.mark_validated()
            elif i == break_point:
                if self.has_error and i == self.divergence_index:
                    frame.mark_as_error()
                else:
                    frame.mark_as_active()
                    self.scroll_frame._parent_canvas.yview_moveto(
                        max(0, i - 2) / len(self._step_frames) * 0.8
                    )
            else:
                frame.mark_as_upcoming()

        self._emit_highlight_command()

    def _emit_highlight_command(self):
        if not self._steps:
            return

        assert self._steps is not None
        if (
            self.has_error
            and self.current_step <= self.divergence_index
            or not self.has_error
            and self.current_step < len(self._steps)
        ):
            self.dispatcher.emit(
                HighlightTileCommand(coord=self._steps[self.current_step])
            )
        else:
            self.dispatcher.emit(HighlightTileCommand(coord=None))

    # --- Event handlers ---
    def _on_solve(self):
        self.dispatcher.emit(ChangeModeCommand(MoraMode.PLAY))
        self.dispatcher.emit(StartSolverCommand())

    def show_empty_state(self):
        self.result_frame.grid_remove()
        self.empty_frame.grid(row=0, column=0, sticky="nsew")

    def show_steps(self):
        self.empty_frame.grid_remove()
        self.result_frame.grid(row=0, column=0, sticky="nsew")
