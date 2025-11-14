class Cell:
    def __init__(self, x, y, terrain=1):
        self.x = x
        self.y = y
        self.terrain = terrain
        self.cost = self.cost_mapping()
        self.blocked = (self.terrain == 4)

        self.explored = False
        self.correct = False

        self.is_start = False
        self.is_end = False


    def cost_mapping(self):
        if self.terrain == 1:
            return 1
        if self.terrain == 2:
            return 10
        if self.terrain == 3:
            return 5
        if self.terrain == 4:
            return 1000
