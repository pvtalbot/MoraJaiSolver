from abc import ABC, abstractmethod
from morajai_solver.event_dispatcher import EventDispatcher
import customtkinter as ctk
import logging

from morajai_solver.models.ColorHexMap import COLOR_HEX_MAP
from morajai_solver.models.MoraColor import MoraColor

logger = logging.getLogger(__name__)

class AbstractMoraButton(ctk.CTkButton, ABC):
    r: int
    c: int
    current_color: MoraColor
    _current_mode: str
    dispatcher: EventDispatcher

    _selected_brush_color: MoraColor = MoraColor.GREY

    @abstractmethod
    def _get_init_parameters(self) -> dict:
        pass

    def __init__(self, master, r: int, c: int):
        super().__init__(master, **self._get_init_parameters())

        self.r = r
        self.c = c

        self.dispatcher = EventDispatcher()
        self.dispatcher.subscribe("mode_changed", self._on_mode_changed)

        self._set_color(MoraColor.GREY)
        self._current_mode = "config"

        self.configure(command=self._on_click)

    def _on_mode_changed(self, new_mode: str):
        self._current_mode = new_mode

    @classmethod
    def set_brush_color(cls, color: MoraColor):
        cls._selected_brush_color = color

    @abstractmethod
    def _on_click(self):
        self._set_color(AbstractMoraButton._selected_brush_color)

    @abstractmethod
    def _get_event_name_when_color_changed(self) -> str :
        pass

    def _on_tile_color_update(self, r: int, c: int, color: MoraColor):
        if (self.r, self.c) != (r, c):
            return
        if color == self.current_color:
            return

        self._set_color(color)

    def _set_color(self, new_color, emit_event=True):
        self.current_color = MoraColor(new_color)
        new_hex = COLOR_HEX_MAP[self.current_color]
        self.configure(fg_color=new_hex, hover_color=new_hex)

        if emit_event:
            self.dispatcher.emit(self._get_event_name_when_color_changed(), r=self.r, c=self.c, color=self.current_color)

class MoraButton(AbstractMoraButton):
    def __init__(self, master, r: int, c: int):
        super().__init__(master, r, c)
        self.dispatcher.subscribe("board_updated", self._on_board_updated)

    def _on_board_updated(self, board_state: dict):
        new_color = board_state.get((self.r, self.c))

        if new_color is None or new_color == self.current_color:
            return

        self._set_color(new_color, emit_event=False)

    def _on_click(self):
        if self._current_mode == 'config':
            super()._on_click()
        else:
            self.dispatcher.emit("tile_clicked", r=self.r, c=self.c, color=self.current_color)

    def _get_event_name_when_color_changed(self):
        return 'tile_color_changed'

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
            logger.info("Non disponible en mode play")

    def _get_event_name_when_color_changed(self):
        return 'target_color_changed'

    def _get_init_parameters(self) -> dict:
        return {
            "text": "",
            "width": 24,
            "height": 24,
            "corner_radius": 8,
            "border_width": 1,
            "border_color": "#1E1E1E"
        }
