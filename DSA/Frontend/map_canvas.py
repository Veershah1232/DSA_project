import tkinter as tk
from Backend.grid import Grid

class MapCanvas(tk.Canvas):
    def __init__(self, parent, cell_size=30):
        super().__init__(parent, bg="white", highlightthickness=0)
        self.parent = parent
        self.cell_size = cell_size

        self.grid_obj = None
        self.bind("<Button-1>", self.on_click)
        self.bind("<B1-Motion>", self.on_drag)

    def set_grid(self, grid):
        self.grid_obj = grid
        self.draw()

    def clear_visuals(self):
        if not self.grid_obj:
            return

        for row in self.grid_obj.grid:
            for cell in row:
                cell.explored = False
                cell.correct = False
        self.draw()

    def draw(self):
        self.delete("all")
        if not self.grid_obj:
            return

        for y in range(self.grid_obj.height):
            for x in range(self.grid_obj.width):
                self.draw_cell(x, y)

    def draw_cell(self, x, y):
        cs = self.cell_size
        cell = self.grid_obj.get_cell(x, y)
        x1, y1 = x * cs, y * cs
        x2, y2 = x1 + cs, y1 + cs

        if cell.is_start:
            color = "#4CAF50"        # green
        elif cell.is_end:
            color = "#E53935"        # red

        else:
            if cell.terrain == 1:
                color = "white"       # air
            elif cell.terrain == 2:
                color = "#64B5F6"     # water
            elif cell.terrain == 3:
                color = "#FDD835"     # sand
            elif cell.terrain == 4:
                color = "#212121"     # wall

        if cell.correct:
            color = "#00D420"         # path
        elif cell.explored and cell.terrain != 4:
            color = "#144166"         # explored
        if cell.is_start:
            color = "#4CAF50"        # green
        elif cell.is_end:
            color = "#E53935"        # red
        self.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")


    def on_click(self, event):
        if not self.grid_obj:
            return
        x = event.x // self.cell_size
        y = event.y // self.cell_size
        self.toggle_cell(x, y)

    def on_drag(self, event):
        if not self.grid_obj:
            return
        x = event.x // self.cell_size
        y = event.y // self.cell_size
        self.toggle_cell(x, y)

    def toggle_cell(self, x, y):
        if not self.grid_obj.bound_check(x, y):
            return

        cell = self.grid_obj.get_cell(x, y)

        if cell.is_start or cell.is_end:
            return

        cell.is_wall = not cell.is_wall
        self.draw()

    def pixel_to_cell(self, px, py):
        x = px // self.cell_size
        y = py // self.cell_size

        if self.grid_obj is None:
            return None, None

        if x < 0 or y < 0 or x >= self.grid_obj.width or y >= self.grid_obj.height:
            return None, None

        return int(x), int(y)
