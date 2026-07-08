import customtkinter as ctk

from morajai_solver.event_dispatcher import EventDispatcher
from morajai_solver.models.ColorHexMap import COLOR_HEX_MAP, UITheme
from morajai_solver.models.MoraColor import MoraColor
from morajai_solver.models.MoraEvent import MoraEvent
from morajai_solver.models.MoraMode import MoraMode

class ColorPalette(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", height=75, **kwargs)
        self.dispatcher = EventDispatcher()
        self.buttons = {}

        # CRUCIAL : On interdit à la frame de se déformer ou rétrécir selon ce qu'elle contient
        self.pack_propagate(False)

        # On crée un sous-conteneur qui contiendra tout le visuel (label + boutons)
        self.content_container = ctk.CTkFrame(self, fg_color="transparent")
        self.content_container.pack(fill="both", expand=True)

        # Le label (attaché au content_container)
        self.label = ctk.CTkLabel(self.content_container, text="Palette (Mode Config) :", font=('Arial', 11, 'bold'))
        self.label.pack(anchor="w", padx=5, pady=(2, 2))

        # Conteneur horizontal pour les 10 couleurs (attaché au content_container)
        self.palette_frame = ctk.CTkFrame(self.content_container, fg_color=UITheme.BG_TILE_CONTAINER.value, corner_radius=8)
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
                command=lambda c=color: self._select_color(c)
            )
            btn.pack(side="left", padx=4, pady=6, expand=True)
            self.buttons[color] = btn

        self._update_highlight(MoraColor.GREY)

        self.dispatcher.subscribe(MoraEvent.MODE_CHANGED, self._on_mode_changed)

    def _on_mode_changed(self, new_mode: MoraMode):
        if new_mode == MoraMode.PLAY:
            self.content_container.pack_forget()
        else:
            self.content_container.pack(fill="both", expand=True)

    def _update_highlight(self, active_color: MoraColor):
        for color, btn in self.buttons.items():
            if color == active_color:
                btn.configure(border_width=2, border_color=UITheme.BORDER_HIGHLIGHT.value)
            else:
                btn.configure(border_width=1, border_color=UITheme.BORDER_DARK.value)

    def _select_color(self, color: MoraColor):
        from morajai_solver.components.MoraButton import AbstractMoraButton
        AbstractMoraButton.set_brush_color(color)
        self._update_highlight(color)
