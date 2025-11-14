import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from Frontend.map_canvas import MapCanvas
from Backend.grid import Grid
from Backend.map_io import MapIO


class MapEditorScreen(tk.Frame):
    def __init__(self, root, app):
        super().__init__(root)
        self.app = app

        if app.shared_state.get("current_grid") is None:
            self.grid = Grid(25, 25)   # default 25×25 grid
        else:
            self.grid = app.shared_state["current_grid"]

        app.shared_state["current_grid"] = self.grid


        toolbar = tk.Frame(self, height=60)
        toolbar.pack(fill="x", side="top")


        ttk.Label(toolbar, text="Terrain:", font=("Arial", 12)).pack(side="left", padx=5)

        ttk.Button(toolbar, text="Air", command=lambda: self.set_mode("terrain", 1)).pack(side="left", padx=3)
        ttk.Button(toolbar, text="Water", command=lambda: self.set_mode("terrain", 2)).pack(side="left", padx=3)
        ttk.Button(toolbar, text="Sand", command=lambda: self.set_mode("terrain", 3)).pack(side="left", padx=3)
        ttk.Button(toolbar, text="Wall", command=lambda: self.set_mode("terrain", 4)).pack(side="left", padx=3)

        ttk.Separator(toolbar, orient="vertical").pack(side="left", fill="y", padx=8)


        ttk.Button(toolbar, text="Set Start", command=lambda: self.set_mode("start")).pack(side="left", padx=3)
        ttk.Button(toolbar, text="Set End", command=lambda: self.set_mode("end")).pack(side="left", padx=3)

        ttk.Separator(toolbar, orient="vertical").pack(side="left", fill="y", padx=7)

        ttk.Button(toolbar, text="Clear Map", command=self.clear_map).pack(side="left", padx=3)
        ttk.Button(toolbar, text="Save Map", command=self.save_map).pack(side="left", padx=3)

        ttk.Button(toolbar, text="Next → Run Algorithms", command=self.go_to_algorithm_runner).pack(side="right", padx=5)
        ttk.Button(toolbar, text="Back", command=self.go_back).pack(side="right", padx=5)


        self.canvas = MapCanvas(self, cell_size=25)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.set_grid(self.grid)


        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)


        self.current_tool = "terrain"
        self.current_terrain = 1



    def set_mode(self, mode, terrain=None):
        self.current_tool = mode
        if terrain:
            self.current_terrain = terrain


    def apply_tool(self, event):
        x, y = self.canvas.pixel_to_cell(event.x, event.y)

        if not self.grid.bound_check(x, y):
            return

        cell = self.grid.get_cell(x, y)

        if self.current_tool == "terrain":
            cell.terrain = self.current_terrain
            cell.cost = cell.cost_mapping()
            cell.blocked = (cell.terrain == 4)

        elif self.current_tool == "start":
            self.grid.set_start(x, y)

        elif self.current_tool == "end":
            self.grid.set_end(x, y)


        self.canvas.draw()

    def on_click(self, event):
        self.apply_tool(event)

    def on_drag(self, event):
        self.apply_tool(event)



    def clear_map(self):
        self.grid.reset_map()
        self.canvas.set_grid(self.grid)

    def save_map(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt")]
        )
        if filename:
            MapIO.save_map_as_text(self.grid, filename)
            messagebox.showinfo("Saved", "Map saved successfully!")



    def go_back(self):
        self.app.switch_screen("main_menu")

    def go_to_algorithm_runner(self):
        """Pass grid to shared_state + switch screen."""
        self.app.shared_state["current_grid"] = self.grid
        self.app.switch_screen("algorithm_runner")
