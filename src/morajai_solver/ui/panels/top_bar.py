import logging

import customtkinter as ctk

from morajai_solver.infra.event_dispatcher import EventDispatcher
from morajai_solver.infra.events import (
    ChangeModeCommand,
    ListLevelsEvent,
    ListLevelsQuery,
    LoadLevelCommand,
    ModeChangedEvent,
    SubmitRequiredEvent,
)
from morajai_solver.ui.game_modes import MoraMode
from morajai_solver.ui.ui_colors import UITheme

logger = logging.getLogger(__name__)


class TopBar(ctk.CTkFrame):
    def __init__(self, master, ui_bus: EventDispatcher, **kwargs):
        super().__init__(
            master, fg_color=UITheme.BG_PANEL.value, corner_radius=10, **kwargs
        )
        self.dispatcher = ui_bus

        self._setup_ui()

        self.dispatcher.subscribe(ListLevelsEvent, self._on_list_levels_event)
        self.dispatcher.subscribe(ChangeModeCommand, self._on_change_mode_command)

        # --- Mounted ---
        self.dispatcher.emit(ListLevelsQuery())

    def _setup_ui(self):
        self.preset_dropdown = ctk.CTkOptionMenu(
            self,
            values=["Sélectionner"],
            command=self._on_preset_selected,
            width=200,
            fg_color=UITheme.BG_CONSOLE.value,
            button_color=UITheme.BTN_CONFIG_BG.value,
            button_hover_color=UITheme.BTN_CONFIG_HOVER.value,
        )
        self.preset_dropdown.pack(side="left", padx=10, pady=10)

        self.edit_switch = ctk.CTkSwitch(
            self,
            text="Mode édition",
            command=self._on_edit_toggled,
            onvalue=MoraMode.CONFIG.value,
            offvalue=MoraMode.PLAY.value,
        )
        self.edit_switch.select()
        self.edit_switch.pack(side="left", padx=15, pady=10)

        self.admin_btn = ctk.CTkButton(
            self,
            text="Admin",
            width=80,
            fg_color="transparent",
            border_width=1,
            command=self._on_admin_clicked,
        )

    def _on_list_levels_event(self, event: ListLevelsEvent):
        self.preset_dropdown.configure(values=event.levels)

    def _on_preset_selected(self, choice: str):
        self.dispatcher.emit(LoadLevelCommand(id=choice))

    def _on_edit_toggled(self):
        mode = str(self.edit_switch.get()).lower()
        self.dispatcher.emit(ModeChangedEvent(mode=MoraMode(mode)))
        logger.info(f"Nouveau mode : {mode}")

        if mode == MoraMode.PLAY.value:
            self.dispatcher.emit(SubmitRequiredEvent())

    def _on_change_mode_command(self, event: ChangeModeCommand):
        if event.mode == MoraMode.PLAY:
            self.edit_switch.deselect()
        else:
            self.edit_switch.select()

        self._on_edit_toggled()

    def _on_admin_clicked(self):
        pass
