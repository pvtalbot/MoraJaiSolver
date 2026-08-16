import customtkinter as ctk

from morajai_solver.infra.event_dispatcher import EventDispatcher
from morajai_solver.infra.events import ResetGameCommand
from morajai_solver.ui.factory import create_button


class StepNavigationBar(ctk.CTkFrame):
    def __init__(self, master, ui_bus: EventDispatcher, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.dispatcher = ui_bus

        self._setup_ui()

    def _setup_ui(self):
        self.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="nav_btns")
        self.btn_first = create_button(self, "«", self._on_first, font=("Arial", 20))
        self.btn_first.grid(row=0, column=0, padx=2, sticky="ew")

        self.btn_prev = create_button(self, "‹", self._on_prev, font=("Arial", 20))
        self.btn_prev.grid(row=0, column=1, padx=2, sticky="ew")

        self.btn_next = create_button(self, "›", self._on_next, font=("Arial", 20))
        self.btn_next.grid(row=0, column=2, padx=2, sticky="ew")

        self.btn_last = create_button(self, "»", self._on_last, font=("Arial", 20))
        self.btn_last.grid(row=0, column=3, padx=2, sticky="ew")

    def _on_first(self):
        self.dispatcher.emit(ResetGameCommand())

    def _on_prev(self):
        pass

    def _on_next(self):
        pass

    def _on_last(self):
        pass
