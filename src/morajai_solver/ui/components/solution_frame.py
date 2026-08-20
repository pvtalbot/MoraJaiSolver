import customtkinter as ctk

from morajai_solver.ui.ui_colors import UITheme


class SolutionFrame(ctk.CTkFrame):
    def __init__(self, master, index, position, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(
            fg_color=UITheme.BG_TILE_CONTAINER.value,
            corner_radius=6,
            height=35,
        )

        num_lbl = ctk.CTkLabel(
            self,
            text=f" {index} ",
            font=("Arial", 12, "bold"),
            fg_color=UITheme.STEP_NUMBER_BG.value,
            text_color=UITheme.TEXT_WHITE.value,
            corner_radius=4,
        )
        num_lbl.pack(side="left", padx=8, pady=5)

        r, c = position
        text_lbl = ctk.CTkLabel(
            self, text=f"Cliquer sur la case {r}, {c}", font=("Arial", 12)
        )
        text_lbl.pack(side="left", padx=5)

    def mark_as_active(self):
        self.configure(
            fg_color=UITheme.STEP_ACTIVE_BG.value,
            border_width=2,
            border_color=UITheme.STEP_ACTIVE_BORDER.value,
        )

    def mark_as_error(self):
        self.configure(
            fg_color=UITheme.STEP_ERROR_BG.value,
            border_width=2,
            border_color=UITheme.STEP_ERROR_BORDER.value,
        )

    def mark_validated(self):
        self.configure(fg_color=UITheme.STEP_SUCCESS_BG.value, border_width=0)

    def mark_as_upcoming(self):
        self.configure(fg_color=UITheme.BG_TILE_CONTAINER.value, border_width=0)
