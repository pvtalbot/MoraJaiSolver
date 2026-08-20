import math

import customtkinter as ctk

from morajai_solver.infra.event_dispatcher import EventDispatcher
from morajai_solver.infra.events import (
    BoardLoadedEvent,
    JumpToStepCommand,
    MoveEvaluatedEvent,
    NavAction,
    SolutionFoundEvent,
    SolutionInvalidatedEvent,
    StartSolverCommand,
    StepUpdatedEvent,
    VictoryAchievedEvent,
)
from morajai_solver.ui.components.log_box import LogBox
from morajai_solver.ui.components.step_navigation_bar import (
    NavBarState,
    StepNavigationBar,
)
from morajai_solver.ui.modules.solution_display import SolutionDisplay
from morajai_solver.ui.ui_colors import UITheme


class ControlPanel(ctk.CTkFrame):
    def __init__(self, master, ui_bus: EventDispatcher, **kwargs):
        super().__init__(
            master, fg_color=UITheme.BG_PANEL.value, corner_radius=10, **kwargs
        )
        self.dispatcher = ui_bus
        self.current_step = 0
        self.divergence_index = math.inf
        self.nav_bar_state = NavBarState.NO_HIGHLIGHT

        self._setup_ui()

        self.log_box.append_log("Application démarrée.")
        self.log_box.append_log("Prêt à résoudre...")

        self.dispatcher.subscribe(StepUpdatedEvent, self._on_step_updated)
        self.dispatcher.subscribe(MoveEvaluatedEvent, self._on_move_evaluated)
        self.dispatcher.subscribe(VictoryAchievedEvent, self._on_victory_achieved)
        self.dispatcher.subscribe(SolutionFoundEvent, self._on_solution_found)
        self.dispatcher.subscribe(
            SolutionInvalidatedEvent, self._on_solution_invalidated
        )
        self.dispatcher.subscribe(BoardLoadedEvent, self._on_solution_invalidated)
        self.dispatcher.subscribe(StartSolverCommand, self._on_start_solver)

    @property
    def has_error(self):
        return self.divergence_index is not math.inf

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
        self.solution_display.set_on_state_callback(self._on_solution_state_updated)

        self.nav_bar = StepNavigationBar(
            self, ui_bus=self.dispatcher, on_click=self._on_navbar_clicked
        )
        self.nav_bar.grid(row=1, column=0, sticky="ew", padx=10, pady=5)

        self.log_box = LogBox(self)
        self.log_box.grid(row=2, column=0, pady=(5, 10), padx=10, sticky="nsew")

    # --- Event handlers ---
    def _on_victory_achieved(self, _):
        self.log_box.append_log("VICTOIRE !")

    def _on_solution_invalidated(self, _):
        self.solution_display.clear_solution()

    def _on_move_evaluated(self, event: MoveEvaluatedEvent):
        if not self.solution_display.solution_displayed:
            return

        self.solution_display.go_to_next_step(event.last_move)

    def _on_step_updated(self, event: StepUpdatedEvent):
        self.solution_display.jump_to_step(event.current_index)

    def _on_start_solver(self, _):
        self.nav_bar.change_state("disabled")
        self.solution_display.solve_button.configure(state="disabled")

    def _on_solution_found(self, event: SolutionFoundEvent):
        if event.result is None:
            self.log_box.append_log("Aucune solution possible")
        elif len(event.result) == 0:
            self.log_box.append_log("La grille est déjà résolue !")
        else:
            self.log_box.append_log(f"Solution trouvée en {len(event.result)} coups")

        self.solution_display.solve_button.configure(state="normal")
        self.nav_bar.change_state("normal")
        self.solution_display.display_solution(event.result)

    def _on_navbar_clicked(self, action: NavAction):
        match action:
            case NavAction.FIRST:
                if (
                    self.divergence_index < self.current_step
                    and action == NavAction.FIRST
                ):
                    assert isinstance(self.divergence_index, int)
                    self.dispatcher.emit(JumpToStepCommand(self.divergence_index))
                else:
                    self.dispatcher.emit(JumpToStepCommand(0))
            case NavAction.PREVIOUS:
                self.dispatcher.emit(JumpToStepCommand(self.current_step - 1))
            case NavAction.NEXT:
                self.dispatcher.emit(JumpToStepCommand(self.current_step + 1))
            case NavAction.LAST:
                if (
                    self.has_error
                    and self.divergence_index > self.current_step
                    and action == NavAction.LAST
                ):
                    assert isinstance(self.divergence_index, int)
                    self.dispatcher.emit(JumpToStepCommand(self.divergence_index))
                else:
                    self.dispatcher.emit(JumpToStepCommand(-1))

    def _on_solution_state_updated(self, state: tuple[int, int | float]):
        idx, divergence = state
        self.current_step = idx
        self.divergence_index = divergence

        if self.divergence_index is math.inf:
            new_navbar_state = NavBarState.NO_HIGHLIGHT
        elif self.divergence_index < self.current_step:
            new_navbar_state = NavBarState.HIGHLIGHT_FIRST
        elif self.divergence_index > self.current_step:
            new_navbar_state = NavBarState.HIGHLIGHT_LAST
        else:
            new_navbar_state = NavBarState.NO_HIGHLIGHT

        if new_navbar_state != self.nav_bar_state:
            self.nav_bar_state = new_navbar_state
            self.nav_bar.update_state(self.nav_bar_state)
