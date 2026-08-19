from enum import Enum, auto
from typing import Callable

import customtkinter as ctk

from morajai_solver.infra.event_dispatcher import EventDispatcher
from morajai_solver.infra.events import NavAction
from morajai_solver.ui.factory import create_button
from morajai_solver.ui.ui_colors import UITheme


class NavBarState(Enum):
    HIGHLIGHT_FIRST = auto()
    HIGHLIGHT_LAST = auto()
    NO_HIGHLIGHT = auto()


class StepNavigationBar(ctk.CTkFrame):
    def __init__(
        self,
        master,
        ui_bus: EventDispatcher,
        on_click: Callable[[NavAction], None],
        **kwargs,
    ):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.dispatcher = ui_bus
        self._on_click = on_click

        self._setup_ui()

    def _setup_ui(self):
        self.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="nav_btns")
        self.btn_first = create_button(
            self,
            "«",
            lambda: self._on_click(NavAction.FIRST),
            font=("Arial", 20),
        )
        self.btn_first.grid(row=0, column=0, padx=2, sticky="ew")

        self.btn_prev = create_button(
            self,
            "‹",
            lambda: self._on_click(NavAction.PREVIOUS),
            font=("Arial", 20),
        )
        self.btn_prev.grid(row=0, column=1, padx=2, sticky="ew")

        self.btn_next = create_button(
            self,
            "›",
            lambda: self._on_click(NavAction.NEXT),
            font=("Arial", 20),
        )
        self.btn_next.grid(row=0, column=2, padx=2, sticky="ew")

        self.btn_last = create_button(
            self,
            "»",
            lambda: self._on_click(NavAction.LAST),
            font=("Arial", 20),
        )
        self.btn_last.grid(row=0, column=3, padx=2, sticky="ew")

    def _highlight_btn(self, btn: ctk.CTkButton):
        btn.configure(
            fg_color=UITheme.BTN_WARN_BG.value,
            hover_color=UITheme.BTN_WARN_HOVER.value,
        )

    def _unhighlight_btn(self, btn: ctk.CTkButton):
        btn.configure(
            fg_color=UITheme.BTN_CONFIG_BG.value,
            hover_color=UITheme.BTN_CONFIG_HOVER.value,
        )

    def update_state(self, state: NavBarState):
        match state:
            case NavBarState.HIGHLIGHT_FIRST:
                self._highlight_btn(self.btn_first)
                self._unhighlight_btn(self.btn_last)
            case NavBarState.HIGHLIGHT_LAST:
                self._highlight_btn(self.btn_last)
                self._unhighlight_btn(self.btn_first)
            case NavBarState.NO_HIGHLIGHT:
                self._unhighlight_btn(self.btn_first)
                self._unhighlight_btn(self.btn_last)
