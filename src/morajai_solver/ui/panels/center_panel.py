import customtkinter as ctk

from morajai_solver.infra.env import IS_DEV_MODE
from morajai_solver.infra.event_dispatcher import EventDispatcher
from morajai_solver.ui.panels.admin_panel import AdminPanel
from morajai_solver.ui.panels.control_panel import ControlPanel
from morajai_solver.ui.ui_colors import UITheme


class CenterPanel(ctk.CTkFrame):
    def __init__(self, parent, ui_bus: EventDispatcher, *args, **kwargs):
        super().__init__(
            parent, fg_color=UITheme.BG_PANEL.value, corner_radius=10, **kwargs
        )

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=15, pady=(10, 0))

        self._section_title = ctk.CTkLabel(
            header_frame, text="Controls & Logs", font=("Arial", 14, "bold")
        )
        self._section_title.pack(side="left")

        if IS_DEV_MODE:
            self._mode_switch = ctk.CTkSwitch(
                header_frame,
                text="Admin",
                font=("Arial", 11),
                command=self._toggle_mode,
            )
            self._mode_switch.pack(side="right")

        self.control_panel = ControlPanel(self, ui_bus, fg_color="transparent")
        self.admin_panel = AdminPanel(self, ui_bus, fg_color="transparent")

        self.control_panel.grid(row=1, column=0, sticky="nsew", pady=(0, 10))
        self.admin_panel.grid(row=1, column=0, sticky="nsew", pady=(0, 10))

        self.admin_panel.grid_remove()

    def _toggle_mode(self):
        if self._mode_switch.get() == 1:
            self.control_panel.grid_remove()
            self.admin_panel.grid()
            self._section_title.configure(text="Admin")
        else:
            self.admin_panel.grid_remove()
            self.control_panel.grid()
            self._section_title.configure(text="Controls & Logs")
