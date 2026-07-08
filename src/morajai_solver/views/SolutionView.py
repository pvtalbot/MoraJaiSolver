import customtkinter as ctk

from morajai_solver.event_dispatcher import EventDispatcher
from morajai_solver.models.MoraColor import MoraColor
from morajai_solver.models.MoraEvent import MoraEvent

class SolutionView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            fg_color="#1E1E1E",
            corner_radius=10,
            **kwargs
        )

        self.dispatcher = EventDispatcher()

        self._steps = []
        self._current_step_index = 0
        self._step_frames = []
        self._has_error = False
        self._solution_displayed = False

        title = ctk.CTkLabel(
            self,
            text="Solution",
            font=('Arial', 14, 'bold')
        )
        title.pack(pady=10, padx=10)

        self.scroll_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="#101010",
            corner_radius=6
        )
        self.scroll_frame.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0,15)
        )

        self.create_placeholder()

        self.dispatcher.subscribe(MoraEvent.SOLUTION_FOUND, self.display_solution)
        self.dispatcher.subscribe(MoraEvent.RANDOMIZE_BOARD, self.clear_solution)
        self.dispatcher.subscribe(MoraEvent.TILE_COLOR_CHANGED, lambda *args, **kwargs: self.clear_solution())
        self.dispatcher.subscribe(MoraEvent.TARGET_COLOR_CHANGED, lambda *args, **kwargs: self.clear_solution())

        self.dispatcher.subscribe(MoraEvent.RESET_SAVE, self._reset_progress)
        self.dispatcher.subscribe(MoraEvent.TILE_CLICKED, self._on_tile_clicked)

    def create_placeholder(self):
        self.placeholder = ctk.CTkLabel(
            self.scroll_frame,
            text="Aucune solution calculée.",
            font=('Arial', 12, 'italic'),
            text_color="#666666"
        )
        self.placeholder.pack(expand=True, pady=40)

    def clear_solution(self):
        if not self._solution_displayed:
            return

        self._steps = []
        self._current_step_index = 0
        self._step_frames = []
        self._has_error = False
        self._solution_displayed = False

        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        self.create_placeholder()

    def _reset_progress(self):
        self._current_step_index = 0
        self._has_error = False
        self._update_steps_highlighting()

    def display_solution(self, steps: list):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        self._steps = steps
        self._current_step_index = 0
        self._step_frames = []
        self._has_error = False
        self._solution_displayed = True

        if not self._steps:
            label = ctk.CTkLabel(
                self.scroll_frame,
                text="La grille est déjà résolue !",
                font=('Arial', 13, 'bold'),
            )
            label.pack(pady=20)
            return

        for i, (r, c) in enumerate(self._steps, 1):
            step_frame = ctk.CTkFrame(
                self.scroll_frame,
                fg_color="#1A1A1A",
                corner_radius=6,
                height=35
            )
            step_frame.pack(fill="x", padx=5, pady=4)
            step_frame.pack_propagate(False)

            num_lbl = ctk.CTkLabel(
                step_frame,
                text=f" {i} ",
                font=('Arial', 12, 'bold'),
                fg_color="#1E88E5",
                text_color="white",
                corner_radius=4
            )
            num_lbl.pack(side="left", padx=8, pady=5)

            text_lbl = ctk.CTkLabel(
                step_frame,
                text=f"Cliquer sur la case {r}, {c}",
                font=('Arial', 12)
            )
            text_lbl.pack(side='left', padx=5)

            self._step_frames.append(step_frame)

        self._update_steps_highlighting()

    def _on_tile_clicked(self, r: int, c: int, color: MoraColor):
        if not self._steps or self._has_error:
            return
        if self._current_step_index < len(self._steps):
            next_r, next_c = self._steps[self._current_step_index]
            if r == next_r and c == next_c:
                self._current_step_index += 1
                self._update_steps_highlighting()
            else:
                self._has_error = True
                self._update_steps_highlighting()

    def _update_steps_highlighting(self):
        for i, frame in enumerate(self._step_frames):
            if i < self._current_step_index:
                frame.configure(fg_color="#1B5E20", border_width=0)
            elif i == self._current_step_index:
                if self._has_error:
                    frame.configure(fg_color="#421515", border_width=1, border_color="#E53935")
                else:
                    frame.configure(fg_color="#152535", border_width=1, border_color="#1E88E5")
                    self.scroll_frame._parent_canvas.yview_moveto(max(0, i-2)/len(self._step_frames) * 0.8)
            else:
                frame.configure(fg_color="#1A1A1A", border_width=0)
