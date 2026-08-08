from abc import ABC, abstractmethod
from typing import Callable
import customtkinter as ctk

from morajai_solver.ui.ui_colors import COLOR_HEX_MAP, UITheme
from morajai_solver.domain.colors import MoraColor


class AbstractMoraButton(ctk.CTkButton, ABC):
    _current_color: MoraColor

    @abstractmethod
    def _get_init_parameters(self) -> dict:
        pass

    def __init__(
        self,
        master,
        r: int,
        c: int,
        on_tile_clicked: Callable[[int, int], None],
    ):
        super().__init__(master, **self._get_init_parameters())
        self._set_color(MoraColor.GREY)
        self.configure(command=lambda r=r, c=c: on_tile_clicked(r, c))

    def set_color(self, color: MoraColor):
        if color != self._current_color:
            self._set_color(color)

    def _set_color(self, new_color: MoraColor):
        self._current_color = new_color
        new_hex = COLOR_HEX_MAP[self._current_color]
        self.configure(fg_color=new_hex, hover_color=new_hex)


class MoraButton(AbstractMoraButton):
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
    def _get_init_parameters(self) -> dict:
        return {
            "text": "",
            "width": 24,
            "height": 24,
            "corner_radius": 8,
            "border_width": 1,
            "border_color": UITheme.BORDER_DEFAULT.value,
        }
