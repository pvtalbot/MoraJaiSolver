from collections.abc import Callable

import customtkinter as ctk

from morajai_solver.ui.ui_colors import UITheme


def create_button(frame: ctk.CTkFrame, text: str, callback: Callable[[], None]):
    return ctk.CTkButton(
        frame,
        text=text,
        corner_radius=6,
        fg_color=UITheme.BTN_CONFIG_BG.value,
        hover_color=UITheme.BTN_CONFIG_HOVER.value,
        command=callback,
        width=0,
    )
