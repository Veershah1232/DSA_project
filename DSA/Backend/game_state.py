
class GameState:
    '''
    self.mode : 
    1 = main menu
    2 = editor
    3 = viewer
    '''
    def __init__(self):
        self.mode = 1
        self.current_grid = None
        self.selected_algorithm = None
        self.algorithm_finished = None
        self.animating = None
        self.selected_terrain = 1
        self.unsaved = False

    def reset(self):
        self.current_grid = None
        self.selected_algorithm = None
        self.algorithm_finished = None
        self.animating = None
        self.selected_terrain = 1
        self.unsaved = False


    def enter_main_menu(self):
        self.reset()
        self.mode = 1

    def enter_editor(self, grid):
        self.reset()
        self.current_grid = grid
        self.mode = 2

    def enter_viewer(self, grid):
        self.reset()
        self.current_grid = grid
        self.mode = 3
    
    def start_algorith(self, algorithm):
        if self.can_run_algorithm():    
            self.selected_algorithm = algorithm
            self.animating = True
            self.algorithm_finished = False
            return True
        return False
    
    def can_run_algorithm(self):
        if self.animating:
            return False
        if self.current_grid == None:
            return False
        if self.mode != 3:
            return False
        return True

    def finish_algorithm(self):
        self.animating = False
        self.selected_algorithm = None
        self.algorithm_finished = True

    def set_terrain(self, terrain):
        self.selected_terrain = terrain

    def set_saved(self):
        self.unsaved = False

    def set_unsaved(self):
        self.unsaved = True
