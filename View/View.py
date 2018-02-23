import tkinter as tk
from tkinter import Label, Button
from View.WindowChooser import WindowChooser


class View(tk.Frame):
            
    def __init__(self):
        root = tk.Tk()
        super().__init__(root)
        root.focus_force()             
        root.wm_title("TFRevolution")
        self.pack()
        self.winChooser = WindowChooser(root) 
  
    # called by Controller to set callbacks for when input changes
    def SetWindowChooserCallbacks(self, name, rect, grid, save):
        self.winChooser.SetWindowNameChosenCallback(name)
        self.winChooser.SetRectChangeCallback(rect)
        self.winChooser.SetGridSizeChangeCallback(grid)
        self.winChooser.SetSaveCallback(save)
                
    def LoadWindowChooser(self, names, rect, grid):
        self.winChooser.show(names, rect, grid)
