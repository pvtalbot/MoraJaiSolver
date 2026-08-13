import customtkinter as ctk
import logging

from morajai_solver.infra.event_dispatcher import EventDispatcher
from morajai_solver.infra.events import (
    ListLevelsEvent,
    ListLevelsQuery,
    LoadLevelCommand,
    RandomizeBoardCommand,
    SaveLevelCommand,
    SubmitRequiredEvent,
)
from morajai_solver.ui.factory import create_button
from morajai_solver.ui.ui_colors import UITheme


class AdminPanel(ctk.CTkFrame):
    def __init__(self, master, ui_bus: EventDispatcher, **kwargs):
        super().__init__(master, **kwargs)

        self.dispatcher = ui_bus
        self.logger = logging.getLogger(__name__)

        self._setup_ui()

        self.dispatcher.subscribe(ListLevelsEvent, self._on_list_levels)
        self.dispatcher.emit(ListLevelsQuery())

    # --- UI Setup ---
    def _setup_ui(self):
        self.random_button = create_button(self, "Randomize", self._on_random_click)
        self.random_button.pack(pady=(15, 5), padx=20, fill="x")

        self.save_button = create_button(self, "Save", self._on_save_click)
        self.save_button.pack(pady=5, padx=20, fill="x")

        levels_frame = ctk.CTkFrame(self, fg_color="transparent")
        levels_frame.pack(pady=10, padx=20, fill="x")
        levels_label = ctk.CTkLabel(levels_frame, text="Levels:", font=("Arial", 11))
        levels_label.pack(side="left", padx=(0, 5))

        self.load_button = create_button(levels_frame, "Load", self._on_load_click)
        self.load_button.pack(side="right")

        self.levels_dropdown = ctk.CTkOptionMenu(
            levels_frame,
            values=["Aucun niveau"],
            fg_color=UITheme.BG_CONSOLE.value,
            button_color=UITheme.BTN_CONFIG_BG.value,
            button_hover_color=UITheme.BTN_CONFIG_HOVER.value,
        )
        self.levels_dropdown.pack(side="left", fill="x", expand=True)

    # --- Click handlers & helpers ---
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
        self.dispatcher.emit(SubmitRequiredEvent())
        self.dispatcher.emit(SaveLevelCommand(id=board_id))

    def _on_load_click(self):
        level_id = self.get_selected_level()

        if not level_id:
            return

        self.dispatcher.emit(LoadLevelCommand(id=level_id))

    # --- Events handlers ---
    def _on_list_levels(self, event: ListLevelsEvent):
        if not event.levels:
            self.levels_dropdown.configure(values=["Aucun niveau"])
            self.levels_dropdown.set("Aucun niveau")
        else:
            self.levels_dropdown.configure(values=event.levels)
            self.levels_dropdown.set(event.levels[0])
