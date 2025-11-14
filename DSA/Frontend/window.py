import tkinter as tk
from .screens.main_menu import MainMenuScreen
from .screens.map_editor_screen import MapEditorScreen
from .screens.algorithm_runner_screen import AlgorithmRunnerScreen


class Window:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PathFinding Visualizer")
        self.root.geometry("1000x700")

        self.screen = None

        self.shared_state = {
            "current_grid": None,
            "start": None,
            "end": None
        }

        self.screens = {
            "main_menu": MainMenuScreen,
            "map_editor" : MapEditorScreen,
            "algorithm_runner" : AlgorithmRunnerScreen
        }

        self.switch_screen("main_menu")

    def switch_screen(self, name = "main_menu"):
        if self.screen != None:
            self.screen.pack_forget()
            self.screen.destroy()
        
        ScreenClass = self.screens[name]
        self.screen = ScreenClass(self.root, self)
        self.screen.pack(fill = "both", expand = True)

    def run(self):
        self.root.mainloop()

