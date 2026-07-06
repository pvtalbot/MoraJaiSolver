from abc import ABC, abstractmethod
from morajai_solver.event_dispatcher import EventDispatcher
from morajai_solver.logger import get_logger
from logging import DEBUG
import customtkinter as ctk

PINK = "#FF69B4"
YELLOW = "#FFD700"
PURPLE = "#8A2BE2"
DARK_GRAY = "#2B2B2B"

COLORS = [DARK_GRAY, PINK, YELLOW, PURPLE]

class AbstractMoraButton(ctk.CTkButton, ABC):
    @abstractmethod
    def _get_init_parameters(self) -> dict:
        pass

    def __init__(self, master, row: int, column: int):
        super().__init__(master, **self._get_init_parameters())
        self._logger = get_logger(DEBUG, __name__)
        self.row = row
        self.column = column
        self.color_index = 0
        self._current_mode = "config"

        self.dispatcher = EventDispatcher()
        self.dispatcher.subscribe("mode_changed", self._on_mode_changed)

        self.configure(command=self._on_click)

    def _on_mode_changed(self, new_mode: str):
        self._current_mode = new_mode

    @abstractmethod
    def _on_click(self):
        self.color_index = (self.color_index + 1) % len(COLORS)
        new_color = COLORS[self.color_index]
        self.configure(fg_color=new_color, hover_color=new_color)

class MoraButton(AbstractMoraButton):
    def _on_click(self):
        if self._current_mode == 'config':
            super()._on_click()
        else:
            self.dispatcher.emit("tile_clicked", row=self.row, column=self.column)

    def _get_init_parameters(self) -> dict:
        return {
            "text": "",
            "width": 95,
            "height": 95,
            "corner_radius": 6,
            "border_width": 1,
            "border_color": "#1E1E1E"
        }

class MoraTargetButton(AbstractMoraButton):
    def _on_click(self):
        if self._current_mode == 'config':
            super()._on_click()
        else:
            self._logger.warning(f"Ne peut pas être modifié en mode PLAY")

    def _get_init_parameters(self) -> dict:
        return {
            "text": "",
            "width": 24,
            "height": 24,
            "corner_radius": 8,
            "border_width": 1,
            "border_color": "#1E1E1E"
        }
