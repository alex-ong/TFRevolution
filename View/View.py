import tkinter as tk
from tkinter import Label, Button
from View.WindowChooser import WindowChooser


class View(tk.Frame):
            
    def __init__(self):
        root = tk.Tk()
        super().__init__(root)
        root.protocol("WM_DELETE_WINDOW", self.on_exit)
        root.focus_force()             
        root.wm_title("TFRevolution")
        self.pack()
        self.winChooser = WindowChooser(root)
        self.winChooser.pack() 
        self.root = root

    # called by Controller to set callbacks for when input changes
    def SetWindowChooserCallbacks(self, name, rect, grid, save, refresh, garbageX,
                                  playerX, image, rawImage, showCalib, showProcessed):
        self.winChooser.SetWindowNameChosenCallback(name)
        self.winChooser.SetRectChangeCallback(rect)
        self.winChooser.SetGridSizeChangeCallback(grid)
        self.winChooser.SetSaveCallback(save)
        self.winChooser.SetRefreshCallback(refresh)
        self.winChooser.SetGarbageXOffsetCallback(garbageX)
        self.winChooser.SetPlayerXOffsetCallback(playerX)
        self.winChooser.SetGetImageSource(image)
        self.winChooser.SetRawImageSource(rawImage)
        self.winChooser.SetShowCalibrationCallback(showCalib)
        self.winChooser.SetShowProcessedCallback(showProcessed)
        
    def LoadWindowChooser(self, names, rect, grid, garbageX, playerX):
        self.winChooser.show(names, rect, grid, garbageX, playerX)
    
    def update(self):
        self.winChooser.update()
        super().update()
    
    def on_exit(self):
        self.winChooser.safeDestroy()
        self.root.destroy()