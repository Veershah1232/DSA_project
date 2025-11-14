import tkinter as tk
from tkinter import ttk
from collections import deque
from Frontend.map_canvas import MapCanvas


class AlgorithmRunnerScreen(tk.Frame):
    def __init__(self, root, app):
        super().__init__(root)
        self.app = app
        self.visited = []

        # Reference to current grid (sent from map editor)
        self.grid = app.shared_state.get("current_grid", None)

        toolbar = tk.Frame(self, height=60)
        toolbar.pack(fill="x", side="top")

        ttk.Label(toolbar, text="Select Algorithm:", font=("Arial", 12)).pack(side="left", padx=10)

        ttk.Button(toolbar, text="BFS", command=lambda: self.start_algorithm("bfs")).pack(side="left", padx=5)
        ttk.Button(toolbar, text="Dijkstra", command=lambda: self.start_algorithm("dijkstra")).pack(side="left", padx=5)
        ttk.Button(toolbar, text="A*", command=lambda: self.start_algorithm("astar")).pack(side="left", padx=5)

        ttk.Button(toolbar, text="Back", command=self.go_back).pack(side="right", padx=10)

        self.canvas = MapCanvas(self, cell_size=25)
        self.canvas.pack(fill="both", expand=True)

        if self.grid:
            self.canvas.set_grid(self.grid)

        self.animation_queue = []
        self.current_animation = None
        self.is_animating = False



    def go_back(self):
        """Return to map editor."""
        self.grid.clear_animations()
        self.app.switch_screen("map_editor")



    def start_algorithm(self, algo_name):
        if self.is_animating:
            return  # block until previous animation finishes

        print(f"Starting algorithm: {algo_name}")

        self.canvas.clear_visuals()

        if algo_name == "bfs":
            from Algorithms.bfs import bfs as algo
        elif algo_name == "dijkstra":
            from Algorithms.dijkstra import dijkstra as algo
        else:
            from Algorithms.astar import astar as algo

        self.exploration_gen = algo(self.grid)
        self.is_animating = True

        self.animate_step()

    def animate_step(self):
        try:
            pos_x, pos_y = next(self.exploration_gen)
            self.visited.append((pos_x,pos_y))
            cell = self.grid.get_cell(pos_x, pos_y)
            cell.explored = True
            self.canvas.draw()
            self.after(20, self.animate_step)  # schedule next step after 30ms
        except StopIteration as path:
            self.final_path = path.value if hasattr(path, 'value') else path

            for cell in self.final_path:
                cell.correct = True
            for cells in self.visited:
                print(cells[0])
                self.grid.get_cell(cells[0], cells[1]).explored = False
            self.canvas.draw()
            self.is_animating = False
            self.visited = []
            print("Algorithm animation completed")
