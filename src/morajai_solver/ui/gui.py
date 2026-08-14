import customtkinter as ctk

from morajai_solver.infra.event_dispatcher import EventDispatcher
from morajai_solver.ui.panels.board_panel import BoardPanel
from morajai_solver.ui.panels.center_panel import CenterPanel
from morajai_solver.ui.panels.solution_panel import SolutionPanel
from morajai_solver.ui.ui_colors import UITheme


def fade_out(app, alpha=1.0):
    if alpha > 0.0:
        alpha -= 0.1
        app.attributes("-alpha", alpha)
        app.after(10, lambda: fade_out(app, alpha))
    else:
        app.destroy()


class MoraApp(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.board_panel: BoardPanel
        self.center_panel: CenterPanel
        self.solution_panel: SolutionPanel


def launch_gui(ui_bus: EventDispatcher) -> MoraApp:
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = MoraApp()
    app.title("Mora Jai Box Solver")
    app.geometry("1180x680")

    title = ctk.CTkLabel(app, text="Mora Jai Box Solver", font=("Arial", 20, "bold"))
    title.pack(pady=15)

    quit_button = ctk.CTkButton(
        app,
        text="Quit",
        fg_color=UITheme.BTN_QUIT_BG.value,
        hover_color=UITheme.BTN_QUIT_HOVER.value,
        command=lambda: fade_out(app),
        border_width=0,
    )
    quit_button.pack(side="bottom", pady=20)

    main_container = ctk.CTkFrame(app, fg_color="transparent")
    main_container.pack(fill="both", expand=True, padx=15, pady=5)
    main_container.grid_columnconfigure(0, weight=2)
    main_container.grid_columnconfigure(1, weight=1, minsize=300)
    main_container.grid_columnconfigure(2, weight=1)

    app.board_panel = BoardPanel(main_container, ui_bus)
    app.board_panel.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    app.center_panel = CenterPanel(main_container, ui_bus)
    app.center_panel.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

    app.solution_panel = SolutionPanel(main_container, ui_bus)
    app.solution_panel.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

    return app
