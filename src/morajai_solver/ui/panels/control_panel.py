import logging

import customtkinter as ctk

from morajai_solver.infra.event_dispatcher import EventDispatcher
from morajai_solver.infra.events import (
    BoardLoadedEvent,
    PlayTileCommand,
    ResetGameCommand,
    SolutionFoundEvent,
    SolutionInvalidatedEvent,
    VictoryAchievedEvent,
)
from morajai_solver.ui.components.solution_display import SolutionDisplay
from morajai_solver.ui.components.step_navigation_bar import StepNavigationBar
from morajai_solver.ui.ui_colors import UITheme


class ControlPanel(ctk.CTkFrame):
    def __init__(self, master, ui_bus: EventDispatcher, **kwargs):
        super().__init__(master, **kwargs)
        self.dispatcher = ui_bus
        self.logger = logging.getLogger(__name__)

        self._setup_ui()

        self._append_log("Application démarrée.")
        self._append_log("Prêt à résoudre...")
        self.log_box.configure(state="disabled")

        self.dispatcher.subscribe(VictoryAchievedEvent, self._on_victory_achieved)
        self.dispatcher.subscribe(SolutionFoundEvent, self._on_solution_found)
        self.dispatcher.subscribe(
            SolutionInvalidatedEvent, self._on_solution_invalidated
        )
        self.dispatcher.subscribe(BoardLoadedEvent, self._on_solution_invalidated)
        self.dispatcher.subscribe(ResetGameCommand, self._on_reset_game)
        self.dispatcher.subscribe(PlayTileCommand, self._on_tile_clicked)

    # --- UI Setup ---
    def _setup_ui(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_columnconfigure(0, weight=1)

        self.solution_display = SolutionDisplay(self, ui_bus=self.dispatcher)
        self.solution_display.grid(
            row=0, column=0, sticky="nsew", pady=(10, 5), padx=10
        )

        self.nav_bar = StepNavigationBar(self, ui_bus=self.dispatcher)
        self.nav_bar.grid(row=1, column=0, sticky="ew", padx=10, pady=5)

        self.log_box = ctk.CTkTextbox(
            self,
            height=130,
            fg_color=UITheme.BG_CONSOLE.value,
            text_color=UITheme.TEXT_CONSOLE.value,
            font=("Courier New", 12),
        )
        self.log_box.grid(row=2, column=0, pady=(5, 10), padx=10, sticky="nsew")

    # --- Click handlers & helpers ---
    def _on_solution_found(self, event: SolutionFoundEvent):
        if event.result is None:
            self._append_log("Aucune solution possible")
        elif len(event.result) == 0:
            self._append_log("La grille est déjà résolue !")
        else:
            self._append_log(f"Solution trouvée en {len(event.result)} coups")

        self.solution_display.display_solution(event.result)

    def _append_log(self, message: str):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", f"> {message}\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    # --- Event handlers ---
    def _on_reset_click(self):
        self.dispatcher.emit(ResetGameCommand())

    def _on_victory_achieved(self, _):
        self._append_log("VICTOIRE !")

    def _on_solution_invalidated(self, _):
        self.solution_display.clear_solution()

    def _on_reset_game(self, _):
        self.solution_display.reset_progress()

    def _on_tile_clicked(self, event: PlayTileCommand):
        if not self.solution_display.solution_displayed:
            return

        self.solution_display.next_solution_step(event.position)
