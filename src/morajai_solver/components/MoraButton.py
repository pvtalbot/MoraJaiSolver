from abc import ABC, abstractmethod
from enum import IntEnum
from morajai_solver.event_dispatcher import EventDispatcher
from morajai_solver.logger import get_logger
from logging import DEBUG, Logger
import customtkinter as ctk

class MoraColor(IntEnum):
    GREY = 0
    WHITE = 1
    BLACK = 2
    RED = 3
    YELLOW = 4
    PURPLE = 5
    GREEN = 6
    PINK = 7
    ORANGE = 8
    BLUE = 9

COLOR_HEX_MAP = {
    MoraColor.GREY: "#2B2B2B",
    MoraColor.WHITE: "#FFFFFF",
    MoraColor.BLACK: "#111111",
    MoraColor.RED: "#E53935",
    MoraColor.YELLOW: "#FFD700",
    MoraColor.PURPLE: "#8A2BE2",
    MoraColor.GREEN: "#2E7D32",
    MoraColor.PINK: "#FF69B4",
    MoraColor.ORANGE: "#FF8C00",
    MoraColor.BLUE: "#1E88E5",
}

class AbstractMoraButton(ctk.CTkButton, ABC):
    _logger: Logger
    row: int
    column: int
    current_color: MoraColor
    _current_mode: str
    dispatcher: EventDispatcher

    @abstractmethod
    def _get_init_parameters(self) -> dict:
        pass

    def __init__(self, master, row: int, column: int):
        super().__init__(master, **self._get_init_parameters())

        self._logger = get_logger(DEBUG, __name__)
        self.row = row
        self.column = column

        self._set_color(MoraColor.GREY)
        self._current_mode = "config"

        self.dispatcher = EventDispatcher()
        self.dispatcher.subscribe("mode_changed", self._on_mode_changed)

        self.configure(command=self._on_click)

    def _on_mode_changed(self, new_mode: str):
        self._current_mode = new_mode

    @abstractmethod
    def _on_click(self):
        new_color = (self.current_color + 1) % len(MoraColor)
        self._set_color(new_color)

    def _set_color(self, new_color):
        self.current_color = MoraColor(new_color)
        new_hex = COLOR_HEX_MAP[self.current_color]
        self.configure(fg_color=new_hex, hover_color=new_hex)


class MoraButton(AbstractMoraButton):
    def _on_click(self):
        if self._current_mode == 'config':
            super()._on_click()
        else:
            self.dispatcher.emit("tile_clicked", row=self.row, column=self.column, color=self.current_color)

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
