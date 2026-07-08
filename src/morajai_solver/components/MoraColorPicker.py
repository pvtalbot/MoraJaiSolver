import customtkinter as ctk

from morajai_solver.models.ColorHexMap import COLOR_HEX_MAP
from morajai_solver.models.MoraColor import MoraColor

class MoraColorPicker(ctk.CTkToplevel):
    def __init__(self, master, callback):
        super().__init__(master)
        self.callback = callback

        self.title('Choisir une couleur')
        self.geometry('240x110')
        self.resizable(False, False)

        self.overrideredirect(True)

        self.transient(master)
        self.grab_set()

        pointer_x = self.winfo_pointerx()
        pointer_y = self.winfo_pointery()
        self.geometry(f"+{pointer_x-120}+{pointer_y-55}")

        container = ctk.CTkFrame(
            self,
            fg_color="#1E1E1E",
            border_width=1,
            border_color="#1E88E5",
            corner_radius=0
        )
        container.pack(fill="both", expand=True)

        for col_idx in range(5):
            self.grid_columnconfigure(col_idx, weight=1, uniform="group_cols")
        for row_idx in range(2):
            self.grid_rowconfigure(row_idx, weight=1, uniform="group_rows")

        for i, color in enumerate(MoraColor):
            row = i // 5
            col = i % 5

            btn = ctk.CTkButton(
                container,
                text="",
                width=36,
                height=36,
                fg_color=COLOR_HEX_MAP[color],
                hover_color=COLOR_HEX_MAP[color],
                corner_radius=4,
                border_width=1,
                border_color="#333333",
                command=lambda c=color: self._select_color(c)
            )
            btn.grid(row=row, column=col, padx=5, pady=5, sticky='nsew')

    def _select_color(self, color: MoraColor):
        self.callback(color)
        self.destroy()