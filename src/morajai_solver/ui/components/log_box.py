import customtkinter as ctk

from morajai_solver.ui.ui_colors import UITheme


class LogBox(ctk.CTkTextbox):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(
            height=130,
            fg_color=UITheme.BG_CONSOLE.value,
            text_color=UITheme.TEXT_CONSOLE.value,
            font=("Courier New", 12),
            state="disabled",
        )

    def append_log(self, message: str):
        self.configure(state="normal")
        self.insert("end", f"> {message}\n")
        self.see("end")
        self.configure(state="disabled")
