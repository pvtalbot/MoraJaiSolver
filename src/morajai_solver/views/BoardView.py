import customtkinter as ctk
from itertools import product
from morajai_solver.components.ColorPalette import ColorPalette
from morajai_solver.components.MoraButton import MoraButton, MoraTargetButton

class BoardView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        outer_frame = ctk.CTkFrame(self, fg_color="#1E1E1E", corner_radius=10)
        outer_frame.pack(anchor="center", pady=10)

        grid_frame = ctk.CTkFrame(outer_frame, fg_color="#1E1E1E", corner_radius=10)
        grid_frame.pack(padx=10, pady=10)

        # Grille 3x3 : on passe les coordonnées row/column aux boutons
        for r, c in product(range(3), range(3)):
            button = MoraButton(grid_frame, r+1, c+1)
            button.grid(row=r+1, column=c+1, padx=6, pady=6)

        # Cibles aux 4 coins (Grille virtuelle 5x5 de 0 à 4)
        CORNER_TARGETS = [
            {"row": 0, "column": 0},
            {"row": 0, "column": 4},
            {"row": 4, "column": 4},
            {"row": 4, "column": 0},
        ]

        for target_pos in CORNER_TARGETS:
            target = MoraTargetButton(grid_frame, target_pos["row"], target_pos["column"])
            target.grid(**target_pos)

        palette = ColorPalette(outer_frame)
        palette.pack(fill='x', padx=15, pady=(0, 15))