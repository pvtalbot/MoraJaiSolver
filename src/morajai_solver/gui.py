import customtkinter as ctk

from morajai_solver.views.BoardView import BoardView
from morajai_solver.views.ControlPanelView import ControlPanelView
from morajai_solver.core.game_engine import GameEngine

def fade_out(app, alpha=1.0):
    if alpha > 0.0:
        alpha -= 0.1
        app.attributes('-alpha', alpha)
        app.after(10, lambda: fade_out(app, alpha))
    else:
        app.destroy()

def main():
    engine = GameEngine()

    ctk.set_appearance_mode('dark')
    ctk.set_default_color_theme('blue')

    app = ctk.CTk()
    app.title('Mora Jai Box Solver')
    app.geometry('780x680')

    title = ctk.CTkLabel(
        app,
        text='Mora Jai Box Solver',
        font=('Arial', 20, 'bold')
    )
    title.pack(pady=15)

    quit_button = ctk.CTkButton(
        app,
        text="Quit",
        fg_color="#D32F2F",
        hover_color="#B71C1C",
        command=lambda: fade_out(app)
    )
    quit_button.pack(side='bottom', pady=20)

    main_container = ctk.CTkFrame(app, fg_color="transparent")
    main_container.pack(fill="both", expand=True, padx=15, pady=5)
    main_container.grid_columnconfigure(0, weight=1)
    main_container.grid_columnconfigure(1, weight=1)

    board_view = BoardView(main_container)
    board_view.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    control_panel = ControlPanelView(main_container)
    control_panel.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")


    app.mainloop()

if __name__ == '__main__':
    main()