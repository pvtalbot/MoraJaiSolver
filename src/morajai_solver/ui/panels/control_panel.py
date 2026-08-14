import logging
import queue

import customtkinter as ctk

from morajai_solver.infra.event_dispatcher import EventDispatcher
from morajai_solver.infra.events import (
    ModeChangedEvent,
    ResetGameCommand,
    SolutionFoundEvent,
    StartSolverCommand,
    SubmitRequiredEvent,
    VictoryAchievedEvent,
)
from morajai_solver.ui.factory import create_button
from morajai_solver.ui.game_modes import MoraMode
from morajai_solver.ui.ui_colors import UITheme


class ControlPanel(ctk.CTkFrame):
    def __init__(self, master, ui_bus: EventDispatcher, **kwargs):
        super().__init__(master, **kwargs)
        self.dispatcher = ui_bus
        self.logger = logging.getLogger(__name__)

        self.queue: queue.Queue = queue.Queue()

        self._setup_ui()

        self._append_log("Application démarrée.")
        self._append_log("Prêt à résoudre...")
        self.log_box.configure(state="disabled")

        self.dispatcher.subscribe(VictoryAchievedEvent, self._on_victory_achieved)
        self.dispatcher.subscribe(SolutionFoundEvent, self._on_solution_found)

    # --- UI Setup ---
    def _setup_ui(self):
        mode_label = ctk.CTkLabel(self, text="Application Mode :", font=("Arial", 11))
        mode_label.pack(anchor="w", padx=20, pady=(5, 2))

        self.mode_selector = ctk.CTkSegmentedButton(
            self,
            values=["Config", "Play"],
            font=("Arial", 12, "bold"),
            fg_color=UITheme.BTN_CONFIG_BG.value,
            unselected_color=UITheme.BTN_CONFIG_BG.value,
            selected_color=UITheme.BTN_SELECT_SELECTED.value,
            selected_hover_color=UITheme.BTN_SELECT_HOVER.value,
            unselected_hover_color=UITheme.BTN_CONFIG_HOVER.value,
            command=self._on_mode_change,
        )
        self.mode_selector.pack(padx=20, pady=(0, 15), fill="x")
        self.mode_selector.set("Config")

        self.reset_button = create_button(
            self, text="Reset", callback=self._on_reset_click
        )
        self.reset_button.configure(state="disabled")
        self.reset_button.pack(pady=5, padx=20, fill="x")

        self.solve_button = ctk.CTkButton(
            self,
            text="Solve Box",
            fg_color=UITheme.BTN_SOLVE_BG.value,
            hover_color=UITheme.BTN_SOLVE_HOVER.value,
            command=self._on_solve,
        )
        self.solve_button.pack(pady=10, padx=20, fill="x")

        self.log_box = ctk.CTkTextbox(
            self,
            height=220,
            fg_color=UITheme.BG_CONSOLE.value,
            text_color=UITheme.TEXT_CONSOLE.value,
            font=("Courier New", 12),
        )
        self.log_box.pack(pady=10, padx=20, fill="both", expand=True)

    # --- Click handlers & helpers ---
    def _on_solve(self):
        self._set_controls_state("disabled")
        self._append_log("Calcul de la solution en cours...")
        self.mode_selector.set("Play")
        self._on_mode_change("Play")

        self.dispatcher.emit(StartSolverCommand())

    def _on_solution_found(self, event: SolutionFoundEvent):
        self._set_controls_state("normal")

        if event.result is None:
            self._append_log("Aucune solution possible")
        elif len(event.result) == 0:
            self._append_log("La grille est déjà résolue !")
        else:
            self._append_log(f"Solution trouvée en {len(event.result)} coups")

    def _on_mode_change(self, value: str):
        new_mode = MoraMode(value.lower())
        self.dispatcher.emit(ModeChangedEvent(mode=new_mode))
        self.logger.info(f"Nouveau mode : {value}")

        if new_mode == MoraMode.PLAY:
            self.reset_button.configure(state="normal")
            self.dispatcher.emit(SubmitRequiredEvent())
        else:
            self.reset_button.configure(state="disabled")

    def _set_controls_state(self, state: str):
        self.mode_selector.configure(state=state)
        self.reset_button.configure(state=state)
        self.solve_button.configure(state=state)

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
