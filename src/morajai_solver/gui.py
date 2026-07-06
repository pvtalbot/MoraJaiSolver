import customtkinter as ctk
from itertools import product

from morajai_solver.event_dispatcher import EventDispatcher
from .components.MoraButton import MoraButton, MoraTargetButton

def fade_out(app, alpha=1.0):
    if alpha > 0.0:
        alpha -= 0.1
        app.attributes('-alpha', alpha)
        app.after(10, lambda: fade_out(app, alpha))
    else:
        app.destroy()

def main():
    ctk.set_appearance_mode('dark')
    ctk.set_default_color_theme('blue')

    app = ctk.CTk()
    app.title('Mora Jai Box Solver')
    app.geometry('780x620')

    title = ctk.CTkLabel(
        app,
        text='Mora Jai Box Solver',
        font=('Arial', 20, 'bold')
    )
    title.pack(pady=15)

    main_container = ctk.CTkFrame(app, fg_color="transparent")
    main_container.pack(fill="both", expand=True, padx=15, pady=5)
    main_container.grid_columnconfigure(0, weight=1)
    main_container.grid_columnconfigure(1, weight=1)

    left_area = ctk.CTkFrame(main_container, fg_color="transparent")
    left_area.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    outer_frame = ctk.CTkFrame(
        left_area,
        fg_color = "#1E1E1E",
        corner_radius=10
    )
    outer_frame.pack(anchor="center", padx=10)

    grid_frame = ctk.CTkFrame(
        outer_frame,
        fg_color="#1E1E1E",
        corner_radius=10
    )
    grid_frame.pack(padx=10, pady=10)

    for r, c in product(range(3), range(3)):
        button = MoraButton(grid_frame)
        button.grid(row=r+1, column=c+1, padx=6, pady=6)

    # 2. Placement des 4 targets aux extrémités absolues du tableau (5x5)
    # On leur donne des petites tailles pour qu'elles fassent "pastilles"
    CORNER_TARGETS = [
        {"row": 0, "column": 0},
        {"row": 0, "column": 4},
        {"row": 4, "column": 0},
        {"row": 4, "column": 4},
    ]

    for target_pos in CORNER_TARGETS:
        target = MoraTargetButton(grid_frame)
        target.grid(**target_pos)

    control_panel = ctk.CTkFrame(main_container, fg_color="#1E1E1E", corner_radius=10)
    control_panel.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

    panel_title = ctk.CTkLabel(
        control_panel,
        text="Controls & Logs",
        font=('Arial', 14, 'bold')
    )
    panel_title.pack(pady=10)

    mode_label = ctk.CTkLabel(control_panel, text="Application Mode :", font=('Arial', 11))
    mode_label.pack(anchor='w', padx=20, pady=(5, 2))

    def on_mode_change(value):
        dispatcher = EventDispatcher()
        dispatcher.emit('mode_changed', new_mode=value.lower())

    mode_selector = ctk.CTkSegmentedButton(
        control_panel,
        values=['Config', 'Play'],
        font=('Arial', 12, 'bold'),
        command=on_mode_change
    )
    mode_selector.pack(padx=20, pady=(0, 15), fill='x')
    mode_selector.set('Config')

    solve_button = ctk.CTkButton(
        control_panel,
        text="Solve",
        fg_color="#2E7D32",
        hover_color="#1B5E20"
    )
    solve_button.pack(pady=10, padx=20, fill="x")

    quit_button = ctk.CTkButton(
        app,
        text="Quit",
        fg_color="#D32F2F",
        hover_color="#B71C1C",
        command=lambda: fade_out(app)
    )
    quit_button.pack(pady=30)

    app.mainloop()

if __name__ == '__main__':
    main()