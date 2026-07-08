import threading

import customtkinter as ctk
import logging

from morajai_solver.core.solver import MoraSolver
from morajai_solver.event_dispatcher import EventDispatcher
from morajai_solver.models.ColorHexMap import UITheme
from morajai_solver.models.MoraEvent import MoraEvent
from morajai_solver.models.MoraMode import MoraMode

class ControlPanelView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=UITheme.BG_PANEL.value, corner_radius=10, **kwargs)
        self.dispatcher = EventDispatcher()
        self.logger = logging.getLogger(__name__)
        
        panel_title = ctk.CTkLabel(self, text="Controls & Logs", font=('Arial', 14, 'bold'))
        panel_title.pack(pady=10)

        mode_label = ctk.CTkLabel(self, text="Application Mode :", font=('Arial', 11))
        mode_label.pack(anchor="w", padx=20, pady=(5, 2))

        self.mode_selector = ctk.CTkSegmentedButton(
            self,
            values=["Config", "Play"],
            font=('Arial', 12, 'bold'),
            fg_color=UITheme.BTN_CONFIG_BG.value,
            unselected_color=UITheme.BTN_CONFIG_BG.value,
            selected_color=UITheme.BTN_SELECT_SELECTED.value,
            selected_hover_color=UITheme.BTN_SELECT_HOVER.value,
            unselected_hover_color=UITheme.BTN_CONFIG_HOVER.value,
            command=self._on_mode_change
        )
        self.mode_selector.pack(padx=20, pady=(0, 15), fill="x")
        self.mode_selector.set("Config")

        self.random_button = ctk.CTkButton(
            self,
            text="Randomize",
            fg_color=UITheme.BTN_CONFIG_BG.value,
            hover_color=UITheme.BTN_CONFIG_HOVER.value,
            command=self._on_random_click
        )
        self.random_button.pack(pady=5, padx=20, fill="x")

        self.solve_button = ctk.CTkButton(
            self,
            text="Solve Box",
            fg_color=UITheme.BTN_SOLVE_BG.value,
            hover_color=UITheme.BTN_SOLVE_HOVER.value,
            command=self._on_solve
        )
        self.solve_button.pack(pady=10, padx=20, fill="x")

        self.log_box = ctk.CTkTextbox(
            self, 
            height=220, 
            fg_color=UITheme.BG_CONSOLE.value, 
            text_color=UITheme.TEXT_CONSOLE.value, 
            font=("Courier New", 12)
        )
        self.log_box.pack(pady=10, padx=20, fill="both", expand=True)
        self.log_box.insert("0.0", "> Application démarrée.\n> Prêt à résoudre...\n")
        self.log_box.configure(state="disabled")

        self.dispatcher.subscribe(MoraEvent.VICTORY_ACHIEVED, self._on_victory_achieved)

        self.solver = MoraSolver()

    def _on_solve(self):
        self._set_controls_state('disabled')
        self._append_log('Calcul de la solution en cours...')
        self.mode_selector.set('Play')
        self._on_mode_change('Play')

        threading.Thread(target=self._run_solver_async, daemon=True).start()

    def _run_solver_async(self):
        result = self.solver.solve()

        self.after(0, self._update_ui_after_solve, result)

    def _update_ui_after_solve(self, result):
        self._set_controls_state('normal')

        if result is None:
            self._append_log("Aucune solution possible")
            return

        elif len(result) == 0:
            self._append_log("La grille est déjà résolue !")
        else:
            self._append_log(f"Solution trouvée en {len(result)} coups")

        self.dispatcher.emit(MoraEvent.SOLUTION_FOUND, steps=result)


    def _on_mode_change(self, value: str):
        new_mode = MoraMode(value.lower())
        self.dispatcher.emit(MoraEvent.MODE_CHANGED, new_mode=new_mode)
        self.logger.info(f"Nouveau mode : {value}")

        if new_mode == MoraMode.PLAY:
            self.random_button.configure(
                text="Reset",
            )
        else:
            self.random_button.configure(
                text="Randomize",
            )

    def _on_random_click(self):
        if self.mode_selector.get().lower() == MoraMode.PLAY.value:
            self.dispatcher.emit(MoraEvent.RESET_SAVE)
        else:
            self.dispatcher.emit(MoraEvent.RANDOMIZE_BOARD)

    def _on_victory_achieved(self):
        self._append_log("VICTOIRE !")

    def _set_controls_state(self, state: str):
        self.mode_selector.configure(state=state)
        self.random_button.configure(state=state)
        self.solve_button.configure(state=state)

    def _append_log(self, message: str):
        self.log_box.configure(state='normal')
        self.log_box.insert('end', f'> {message}\n')
        self.log_box.see('end')
        self.log_box.configure(state='disabled')