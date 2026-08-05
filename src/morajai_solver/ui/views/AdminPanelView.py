import customtkinter as ctk
import logging

from morajai_solver.infra.EventDispatcher import EventDispatcher
from morajai_solver.infra.events import MoraEvent
from morajai_solver.ui.ui_colors import UITheme


class AdminPanelView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.dispatcher = EventDispatcher()
        self.logger = logging.getLogger(__name__)

        self.random_button = ctk.CTkButton(
            self,
            text="Randomize",
            corner_radius=6,
            fg_color=UITheme.BTN_CONFIG_BG.value,
            hover_color=UITheme.BTN_CONFIG_HOVER.value,
            command=self._on_random_click,
        )
        self.random_button.pack(pady=(15, 10), padx=20, fill="x")

    def _on_random_click(self):
        self.dispatcher.emit(MoraEvent.RANDOMIZE_BOARD)
