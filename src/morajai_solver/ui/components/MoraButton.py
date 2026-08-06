from abc import ABC, abstractmethod
from typing import Callable
import customtkinter as ctk
import logging

from morajai_solver.ui.ui_colors import COLOR_HEX_MAP, UITheme
from morajai_solver.domain.colors import MoraColor
from morajai_solver.ui.game_modes import MoraMode

logger = logging.getLogger(__name__)


class AbstractMoraButton(ctk.CTkButton, ABC):
    r: int
    c: int
    _current_color: MoraColor
    _current_mode: MoraMode
    _selected_brush_color: MoraColor
    _on_color_changed: Callable[[int, int, MoraColor], None]
    _on_tile_clicked: Callable[[int, int, MoraColor], None] | None

    @abstractmethod
    def _get_init_parameters(self) -> dict:
        pass

    def __init__(
        self,
        master,
        r: int,
        c: int,
        on_color_changed: Callable[[int, int, MoraColor], None],
        on_tile_clicked: Callable[[int, int, MoraColor], None] | None = None,
    ):
        super().__init__(master, **self._get_init_parameters())

        self.r = r
        self.c = c
        self._on_color_changed = on_color_changed
        self._on_tile_clicked = on_tile_clicked

        self._set_color(MoraColor.GREY)

        self.configure(command=self._on_click)

    def set_mode(self, new_mode: MoraMode):
        self._current_mode = new_mode

    def set_brush_color(self, color: MoraColor):
        self._selected_brush_color = color

    def set_color(self, color: MoraColor):
        if color != self._current_color:
            self._set_color(color)

    def _set_color(self, new_color: MoraColor):
        self._current_color = new_color
        new_hex = COLOR_HEX_MAP[self._current_color]
        self.configure(fg_color=new_hex, hover_color=new_hex)

    def _on_click(self):
        if self._current_mode == MoraMode.CONFIG:
            self._set_color(self._selected_brush_color)
            self._on_color_changed(self.r, self.c, self._current_color)
        else:
            self._handle_play_click()

    @abstractmethod
    def _handle_play_click(self) -> None:
        pass


class MoraButton(AbstractMoraButton):
    def _handle_play_click(self) -> None:
        if self._on_tile_clicked:
            self._on_tile_clicked(self.r, self.c, self._current_color)

    def _get_init_parameters(self) -> dict:
        return {
            "text": "",
            "width": 95,
            "height": 95,
            "corner_radius": 6,
            "border_width": 1,
            "border_color": UITheme.BORDER_DEFAULT.value,
        }


class MoraTargetButton(AbstractMoraButton):
    def _handle_play_click(self) -> None:
        logger.info("Non disponible en mode play")

    def _get_init_parameters(self) -> dict:
        return {
            "text": "",
            "width": 24,
            "height": 24,
            "corner_radius": 8,
            "border_width": 1,
            "border_color": UITheme.BORDER_DEFAULT.value,
        }
