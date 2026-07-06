import customtkinter as ctk
from morajai_solver.event_dispatcher import EventDispatcher

class ControlPanelView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="#1E1E1E", corner_radius=10, **kwargs)
        
        panel_title = ctk.CTkLabel(self, text="Controls & Logs", font=('Arial', 14, 'bold'))
        panel_title.pack(pady=10)

        mode_label = ctk.CTkLabel(self, text="Application Mode :", font=('Arial', 11))
        mode_label.pack(anchor="w", padx=20, pady=(5, 2))

        mode_selector = ctk.CTkSegmentedButton(
            self,
            values=["Config", "Play"],
            font=('Arial', 12, 'bold'),
            command=self._on_mode_change
        )
        mode_selector.pack(padx=20, pady=(0, 15), fill="x")
        mode_selector.set("Config")

        solve_button = ctk.CTkButton(
            self,
            text="Solve Box",
            fg_color="#2E7D32",
            hover_color="#1B5E20",
            command=lambda: print("Calcul de la solution...") 
        )
        solve_button.pack(pady=10, padx=20, fill="x")

        log_label = ctk.CTkLabel(self, text="Console output :", font=('Arial', 11))
        log_label.pack(anchor="w", padx=20, pady=(10, 2))
        
        self.log_box = ctk.CTkTextbox(
            self, 
            height=220, 
            fg_color="#101010", 
            text_color="#00FF00", 
            font=("Courier New", 12)
        )
        self.log_box.pack(pady=5, padx=20, fill="both", expand=True)
        self.log_box.insert("0.0", "> Application démarrée.\n> Prêt à résoudre...\n")
        self.log_box.configure(state="disabled")

    def _on_mode_change(self, value: str):
        dispatcher = EventDispatcher()
        dispatcher.emit("mode_changed", new_mode=value.lower())