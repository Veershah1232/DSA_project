import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from Backend.map_io import MapIO


class MainMenuScreen(tk.Frame):
    def __init__(self, root, app):
        super().__init__(root)
        self.app = app

        title = ttk.Label(self, text="Pathfinding Visualizer", font=("Arial", 32))
        title.pack(pady=40)

        ttk.Button(self, text="Create New Map",
                   command=lambda: app.switch_screen("map_editor")).pack(pady=10)

        ttk.Button(self, text="Load Saved Map",
                   command=self.load_map).pack(pady=10)

        ttk.Button(self, text="Exit",
                   command=root.destroy).pack(pady=40)

    def load_map(self):
        """Load a JSON map and switch to AlgorithmRunnerScreen."""
        filename = filedialog.askopenfilename(
            title="Load Map",
            filetypes=[("TEXT files", "*.txt")]
        )
        if not filename:
            return

        try:
            # Load the map
            grid = MapIO.load_map(filename)
            self.app.shared_state["current_grid"] = grid  # store for AlgorithmRunnerScreen

            self.app.switch_screen("algorithm_runner")
            print(f"Map loaded successfully: {filename}")
        except Exception as e:
            print(f"Failed to load map: {e}")
