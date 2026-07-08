import customtkinter as ctk

from morajai_solver.event_dispatcher import EventDispatcher

class SolutionView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            fg_color="#1E1E1E",
            corner_radius=10,
            **kwargs
        )

        self.dispatcher = EventDispatcher()

        title = ctk.CTkLabel(
            self,
            text="Solution",
            font=('Arial', 14, 'bold')
        )
        title.pack(pady=10, padx=10)

        self.scroll_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="#101010",
            corner_radius=6
        )
        self.scroll_frame.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0,15)
        )

        self.create_placeholder()

        self.dispatcher.subscribe('solution_found', self.display_solution)
        self.dispatcher.subscribe('randomize_board', self.clear_solution)

    def create_placeholder(self):
        self.placeholder = ctk.CTkLabel(
            self.scroll_frame,
            text="Aucune solution calculée.",
            font=('Arial', 12, 'italic'),
            text_color="#666666"
        )
        self.placeholder.pack(expand=True, pady=40)

    def clear_solution(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        self.create_placeholder()

    def display_solution(self, steps: list):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        if not steps:
            label = ctk.CTkLabel(
                self.scroll_frame,
                text="La grille est déjà résolue !",
                font=('Arial', 13, 'bold'),
            )
            label.pack(pady=20)
            return

        for i, (r, c) in enumerate(steps, 1):
            step_frame = ctk.CTkFrame(
                self.scroll_frame,
                fg_color="#1A1A1A",
                corner_radius=6,
                height=35
            )
            step_frame.pack(fill="x", padx=5, pady=4)
            step_frame.pack_propagate(False)

            num_lbl = ctk.CTkLabel(
                step_frame,
                text=f" {i} ",
                font=('Arial', 12, 'bold'),
                fg_color="#1E88E5",
                text_color="white",
                corner_radius=4
            )
            num_lbl.pack(side="left", padx=8, pady=5)

            text_lbl = ctk.CTkLabel(
                step_frame,
                text=f"Cliquer sur la case {r}, {c}",
                font=('Arial', 12)
            )
            text_lbl.pack(side='left', padx=5)
