import customtkinter as ctk

from morajai_solver.infra.event_dispatcher import EventDispatcher
from morajai_solver.infra.events import JumpToStepCommand, NavAction
from morajai_solver.ui.factory import create_button


class StepNavigationBar(ctk.CTkFrame):
    def __init__(self, master, ui_bus: EventDispatcher, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.dispatcher = ui_bus

        self._setup_ui()

    def _setup_ui(self):
        self.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="nav_btns")
        self.btn_first = create_button(
            self,
            "«",
            lambda: self._emit_jump_to_step(NavAction.FIRST),
            font=("Arial", 20),
        )
        self.btn_first.grid(row=0, column=0, padx=2, sticky="ew")

        self.btn_prev = create_button(
            self,
            "‹",
            lambda: self._emit_jump_to_step(NavAction.PREVIOUS),
            font=("Arial", 20),
        )
        self.btn_prev.grid(row=0, column=1, padx=2, sticky="ew")

        self.btn_next = create_button(
            self,
            "›",
            lambda: self._emit_jump_to_step(NavAction.NEXT),
            font=("Arial", 20),
        )
        self.btn_next.grid(row=0, column=2, padx=2, sticky="ew")

        self.btn_last = create_button(
            self,
            "»",
            lambda: self._emit_jump_to_step(NavAction.LAST),
            font=("Arial", 20),
        )
        self.btn_last.grid(row=0, column=3, padx=2, sticky="ew")

    def _emit_jump_to_step(self, action: NavAction):
        self.dispatcher.emit(JumpToStepCommand(action=action))
