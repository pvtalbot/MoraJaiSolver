import customtkinter as ctk
from itertools import product
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
    app.geometry('520x620')

    title = ctk.CTkLabel(
        app,
        text='Mora Jai Box Solver',
        font=('Arial', 20, 'bold')
    )
    title.pack(pady=20)

    outer_frame = ctk.CTkFrame(
        app,
        fg_color = "#1E1E1E",
        corner_radius=10
    )
    outer_frame.pack(pady=10, padx=10)

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