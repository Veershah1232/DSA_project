from Backend.cell import Cell

class Grid:
    def __init__(self, width, height, start = None, end = None):
        self.width = width
        self.height = height
        self.start = start
        self.end = end

        self.grid = []
        for y in range(height):
            row = []
            for x in range(width):
                row.append(Cell(x,y))
            self.grid.append(row)
        
    def bound_check(self, x, y):
        if x < 0 or x >= self.width:
            return False
        if y < 0 or y >= self.height:
            return False
        return True
    def get_cell(self, x, y):
        if self.bound_check(x, y) :
            return self.grid[y][x]
        return None
    
    def set_terrain(self, x, y, terrain):
        cell = self.get_cell(x, y)
        if cell:
            cell.terrain = terrain
            cell.cost = cell.cost_mapping()
            if terrain == 4:
                cell.is_wall = True
            else : 
                cell.is_wall = False

    def cell_explored(self, x, y, explored = False):
        cell = self.get_cell(x, y)
        if cell:
            cell.explored = explored
    
    def cell_correct(self, x, y, correct = False):
        cell = self.get_cell(x, y)
        if cell:
            cell.correct = correct

    def clear_animations(self):
        for row in self.grid :
            for cell in row :
                cell.explored = False
                cell.correct = False
    
    def reset_map(self):
        self.grid = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                row.append(Cell(x,y))
            self.grid.append(row)

    def set_start(self, x, y):
        if self.start != None:
            old_x, old_y = self.start
            self.get_cell(old_x, old_y).is_start = False
        self.start = (x, y)
        self.get_cell(x, y).is_start = True


    def set_end(self, x, y):
        if self.end:
            old_x, old_y = self.end
            self.get_cell(old_x, old_y).is_end = False

        self.end = (x, y)
        self.get_cell(x, y).is_end = True

    
    def save_map(self):
        map_values = []
        for row in self.grid :
            row_values = []
            for cell in row :
                row_values.append(cell.terrain)
            map_values.append(row_values)

        return map_values
    
    def load_map(self, new_map):
        self.height = len(new_map)
        self.width = len(new_map[0])
        self.grid = []
        for y, row in enumerate(new_map):
            new_row = []
            for x, terrain in enumerate(row):
                new_row.append(Cell(x, y, terrain))
            self.grid.append(new_row)

    def get_neighbors(self, x, y):

        steps = [
            (0, -1),  # up
            (0, 1),   # down
            (-1, 0),  # left
            (1, 0),   # right
        ]

        neighbors = []

        for dx, dy in steps:
            nx, ny = x + dx, y + dy
            if self.bound_check(nx, ny):
                cell = self.grid[ny][nx]
                if not cell.blocked:
                    neighbors.append(cell)

        return neighbors