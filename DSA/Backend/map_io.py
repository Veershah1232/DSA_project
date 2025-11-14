import json
from Backend.grid import Grid
from Backend.cell import Cell

class MapIO:

    @staticmethod
    def save_map_as_text(grid: Grid, filename: str):
        data = {
            "width": grid.width,
            "height": grid.height,
            "start": list(grid.start) if grid.start else None,
            "end": list(grid.end) if grid.end else None,
            "terrain": grid.save_map()
        }

        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
        print(f"Map saved to {filename}")

    @staticmethod
    def load_map(filename: str) -> Grid:

        with open(filename, "r") as f:
            data = json.load(f)

        MapIO.validate_loaded_data(data)

        width = data["width"]
        height = data["height"]
        terrain_matrix = data["terrain"]

        grid = Grid(width, height)
        grid.load_map(terrain_matrix)

        if data["start"]:
            grid.start = tuple(data["start"])
            grid.get_cell(grid.start[0], grid.start[1]).is_start = True

        if data["end"]:
            grid.end = tuple(data["end"])
            grid.get_cell(grid.end[0], grid.end[1]).is_end = True

        print(f"Map loaded from {filename}")
        return grid

    @staticmethod
    def validate_loaded_data(data: dict):
        required_keys = ["width", "height", "terrain"]

        for key in required_keys:
            if key not in data:
                raise ValueError(f"Invalid map file: Missing '{key}'")

        width = data["width"]
        height = data["height"]
        terrain = data["terrain"]

        if not isinstance(width, int) or not isinstance(height, int):
            raise ValueError("Grid dimensions must be integers")

        if len(terrain) != height or any(len(row) != width for row in terrain):
            raise ValueError("Terrain matrix dimensions do not match width/height")

        # Check terrain values
        for row in terrain:
            for val in row:
                if val not in (1, 2, 3, 4):
                    raise ValueError(f"Invalid terrain value: {val}")

        for key in ("start", "end"):
            if key in data and data[key] is not None:
                if (
                    not isinstance(data[key], list)
                    or len(data[key]) != 2
                    or not all(isinstance(v, int) for v in data[key])
                ):
                    raise ValueError(f"Invalid coordinate format for '{key}'")

