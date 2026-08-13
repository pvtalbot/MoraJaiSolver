import customtkinter as ctk
import logging

from morajai_solver.infra.event_dispatcher import EventDispatcher
from morajai_solver.infra.events import (
    ListLevelsEvent,
    ListLevelsQuery,
    RandomizeBoardCommand,
    SaveLevelCommand,
)
from morajai_solver.ui.ui_colors import UITheme


class AdminPanel(ctk.CTkFrame):
    def __init__(self, master, ui_bus: EventDispatcher, **kwargs):
        super().__init__(master, **kwargs)
        self.dispatcher = ui_bus
        self.logger = logging.getLogger(__name__)

        self.random_button = ctk.CTkButton(
            self,
            text="Randomize",
            corner_radius=6,
            fg_color=UITheme.BTN_CONFIG_BG.value,
            hover_color=UITheme.BTN_CONFIG_HOVER.value,
            command=self._on_random_click,
        )
        self.random_button.pack(pady=(15, 5), padx=20, fill="x")

        self.save_button = ctk.CTkButton(
            self,
            text="Save",
            corner_radius=6,
            fg_color=UITheme.BTN_CONFIG_BG.value,
            hover_color=UITheme.BTN_CONFIG_HOVER.value,
            command=self._on_save_click,
            width=0,
        )
        self.save_button.pack(pady=5, padx=20, fill="x")

        levels_frame = ctk.CTkFrame(self, fg_color="transparent")
        levels_frame.pack(pady=10, padx=20, fill="x")
        levels_label = ctk.CTkLabel(levels_frame, text="Levels:", font=("Arial", 11))
        levels_label.pack(side="left", padx=(0, 5))

        self.levels_dropdown = ctk.CTkOptionMenu(
            levels_frame,
            values=["Aucun niveau"],
            fg_color=UITheme.BG_CONSOLE.value,
            button_color=UITheme.BTN_CONFIG_BG.value,
            button_hover_color=UITheme.BTN_CONFIG_HOVER.value,
        )
        self.levels_dropdown.pack(side="right", fill="x", expand=True)

        self.dispatcher.subscribe(ListLevelsEvent, self._on_list_levels)
        self.dispatcher.emit(ListLevelsQuery())

    def _on_list_levels(self, event: ListLevelsEvent):
        if not event.levels:
            self.levels_dropdown.configure(values=["Aucun niveau"])
            self.levels_dropdown.set("Aucun niveau")
        else:
            self.levels_dropdown.configure(values=event.levels)
            self.levels_dropdown.set(event.levels[0])

    def get_selected_level(self) -> str | None:
        selected = self.levels_dropdown.get()
        if selected == "Aucun niveau":
            return None
        return selected

    def _on_random_click(self):
        self.dispatcher.emit(RandomizeBoardCommand())

    def _on_save_click(self):
        dialog = ctk.CTkInputDialog(text="Nom :", title="Save")
        board_id = dialog.get_input()

        if not board_id:
            return

        board_id = board_id.strip()
        self.dispatcher.emit(SaveLevelCommand(id=board_id))
