from collections.abc import Callable

import customtkinter as ctk

from morajai_solver.domain.colors import MoraColor
from morajai_solver.ui.game_modes import MoraMode
from morajai_solver.ui.ui_colors import COLOR_HEX_MAP, UITheme


class ColorPalette(ctk.CTkFrame):
    def __init__(
        self,
        master,
        on_color_selected: Callable[[MoraColor], None],
        initial_color: MoraColor = MoraColor.GREY,
        **kwargs,
    ):
        super().__init__(master, fg_color="transparent", height=75, **kwargs)

        self._on_color_selected = on_color_selected
        self.buttons: dict[MoraColor, ctk.CTkButton] = dict()

        # Empêche la frame de se déformer selon son contenu
        self.pack_propagate(False)

        # Conteneur visuel (label + boutons)
        self.content_container = ctk.CTkFrame(self, fg_color="transparent")
        self.content_container.pack(fill="both", expand=True)

        # Label
        self.label = ctk.CTkLabel(
            self.content_container,
            text="Palette",
            font=("Arial", 11, "bold"),
        )
        self.label.pack(anchor="w", padx=5, pady=(2, 2))

        # Conteneur horizontal pour les couleurs
        self.palette_frame = ctk.CTkFrame(
            self.content_container,
            fg_color=UITheme.BG_TILE_CONTAINER.value,
            corner_radius=8,
        )
        self.palette_frame.pack(fill="x", padx=2, pady=2)

        for color in MoraColor:
            btn = ctk.CTkButton(
                self.palette_frame,
                text="",
                width=24,
                height=24,
                fg_color=COLOR_HEX_MAP[color],
                hover_color=COLOR_HEX_MAP[color],
                corner_radius=4,
                border_width=1,
                border_color=UITheme.BORDER_DARK.value,
                command=lambda c=color: self._select_color(c),
            )
            btn.pack(side="left", padx=4, pady=6, expand=True)
            self.buttons[color] = btn

        self._update_highlight(initial_color)

    def set_mode(self, new_mode: MoraMode) -> None:
        if new_mode == MoraMode.PLAY:
            self.content_container.pack_forget()
        else:
            self.content_container.pack(fill="both", expand=True)

    def _update_highlight(self, active_color: MoraColor):
        for color, btn in self.buttons.items():
            if color == active_color:
                btn.configure(
                    border_width=2, border_color=UITheme.BORDER_HIGHLIGHT.value
                )
            else:
                btn.configure(border_width=1, border_color=UITheme.BORDER_DARK.value)

    def _select_color(self, color: MoraColor):
        self._update_highlight(color)
        self._on_color_selected(color)
