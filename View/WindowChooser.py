import tkinter as tk

from View.RectChooser import RectChooser 
from View.ImageCanvas import ImageCanvas
from View.NumberChooser import NumberChooser
from Util.math import tryGetFloat
from View.RawDataCanvas import RawDataCanvas
import time


class WindowChooser(tk.Frame):

    def __init__(self, root):
        super().__init__(root)        
        tk.Label(self, text="Window Target").grid(row=0, column=0)
        self.windowTarget = tk.StringVar()
        self.windowNameTargetChooser = tk.OptionMenu(self, self.windowTarget, "choice1")
        self.windowNameTargetChooser.grid(row=0, column=1)
        tk.Button(self, text="Refresh window list", command=self._OnRefresh).grid(row=0, column=2)
        
        tk.Label(self, text="Capture rectangle").grid(row=1, column=0)
        self.fpsLabel = tk.Label(self, text="FPS: ")
        self.fpsLabel.grid(row=1, column=2)
        self.rect = RectChooser(self, self._OnRectChange)
        self.rect.grid(row=2, column=0, columnspan=3)
        
        self.gridSize = NumberChooser(self, 'gridSizePixels', self._OnGridSizeChange, 0.1)        
        self.gridSize.grid(row=3, column=0)        
        self.garbageSep = NumberChooser(self, 'Garbage X Separation', self._OnGarbageXChange, 0.1)
        self.garbageSep.grid(row=3, column=1)
        self.playerSep = NumberChooser(self, 'playerX separation', self._OnPlayerXChange, 0.1)        
        self.playerSep.grid(row=3, column=2)
        
        tk.Button(self, text="Save", command=self._OnSave).grid(row=4, column=0)
        self.calibrationButton = tk.Button(self, text="Show/Hide Screenshot",
                                           command=self._OnShowCalibration)
        self.calibrationButton.grid(row=4, column=1)
        
        self.processedButton = tk.Button(self, text="Show/Hide Processed",
                                           command=self._OnShowProcessed)
        self.processedButton.grid(row=4, column=2)
        
        self.calibrationCanvas = ImageCanvas(self)  # don't grid        
        self.processedCanvas = RawDataCanvas(self)  # don't grid
        
        self._GridSizeChangeCb = None
        self._GarbageXChangeCb = None
        self._RectChangeCb = None
        self._WindowNameChangeCb = None
        self._RefreshCb = None
        self._UpdatePlayerSeparation = None
        self._OnShowProcessed = None
        self._OnShowCalibration = None
        
        self.showCalibration = False
        self.showProcessed = False
        self.timer = time.time()
        self.frameCount = 0
        self.isBeingDestroyed = False

    def safeDestroy(self):
        self.isBeingDestroyed = True

    def update(self):
        if not self.isBeingDestroyed:
            self.updateFPSLabel()
            if self.showCalibration:
                self.calibrationCanvas.update()
            if self.showProcessed:
                self.processedCanvas.update()
        
    def updateFPSLabel(self):
        
        self.frameCount += 1
        if self.frameCount >= 10:            
            diff = time.time() - self.timer
            fps = round(self.frameCount / float(diff))
            if (diff != 0):
                text = ("FPS " + str(fps).zfill(3))
                try:
                    self.fpsLabel.config(text=text) 
                except tk.TclError as e:
                    pass
            self.frameCount = 0
            self.timer = time.time()
                    
    # call callbacks if necessary    
    def _OnGridSizeChange(self):
        success, value = tryGetFloat(self.gridSize.value.get())
        if success and self._GridSizeChangeCb is not None:
            self._GridSizeChangeCb(value)
    
    def _OnGarbageXChange(self):
        success, value = tryGetFloat(self.garbageSep.value.get())
        if success and self._GarbageXChangeCb is not None:
            self._GarbageXChangeCb(value)
            
    def _OnRectChange(self, value):
        if self._RectChangeCb is not None:
            self._RectChangeCb(value)

    def _OnWindowNameChosen(self, hwnd, newName):                
        self.windowTarget.set(newName)
        if self._WindowNameChangeCb is not None:
            self._WindowNameChangeCb(hwnd, newName)
    
    def _OnSave(self):
        if self._Save is not None:
            self._Save()
    
    def _OnRefresh(self):
        if self._RefreshCb is not None:
            self._RefreshCb()
    
    def _OnPlayerXChange(self):        
        success, value = tryGetFloat(self.playerSep.value.get())        
        if success and self._UpdatePlayerSeparation is not None:
            self._UpdatePlayerSeparation(value)
    
    def _OnShowProcessed(self):        
        if self._OnToggleShowProcessed:
            self._OnToggleShowProcessed()
    
    def _OnShowCalibration(self):
        if self._OnToggleShowCalibration:
            self._OnToggleShowCalibration()
                    
    # Set callbacks
    def SetGridSizeChangeCallback(self, cb):
        self._GridSizeChangeCb = cb
    
    def SetRectChangeCallback(self, cb):
        self._RectChangeCb = cb
        
    def SetWindowNameChosenCallback(self, cb):
        self._WindowNameChangeCb = cb
            
    def SetSaveCallback(self, cb):
        self._Save = cb
    
    def SetRefreshCallback(self, cb):
        self._RefreshCb = cb
                        
    def SetGetImageSource(self, cb):
        self.calibrationCanvas.SetImageSource(cb)
    
    def SetRawImageSource(self, cb):
        self.processedCanvas.SetImageSource(cb)
    
    def SetGarbageXOffsetCallback(self, cb):
        self._GarbageXChangeCb = cb
        
    def SetPlayerXOffsetCallback(self, cb):
        self._UpdatePlayerSeparation = cb
        
    def SetShowCalibrationCallback(self, cb):
        self._OnToggleShowCalibration = cb
        
    def SetShowProcessedCallback(self, cb):
        self._OnToggleShowProcessed = cb
                         
    def show(self, names, rect, grid, garbageX, playerX):
        self.windowNameTargetChooser['menu'].delete(0, 'end')         
        self.windowTarget.set(str(names[0][1]))
        autoChooseWindow = None  # calculate hwnd and send to model if it is present
        
        for name in names:            
            hwnd = name[0]
            winName = name[1]
            command = lambda h = hwnd, n = winName :self._OnWindowNameChosen(h, n)            
            self.windowNameTargetChooser['menu'].add_command(label=name,
                                                             command=command)
            if (self.windowTarget.get() == winName):
                autoChooseWindow = command
                
        self.rect.show(rect)
        self.gridSize.value.set(str(grid))
        self.garbageSep.value.set(str(garbageX))
        self.playerSep.value.set(str(playerX))
        if (autoChooseWindow is not None):
            autoChooseWindow()

    def SetCalibration(self, value):
        if value:            
            self.calibrationCanvas.grid(row=5, columnspan=4, sticky=tk.NSEW)        
        else:
            self.calibrationCanvas.grid_forget()
        self.showCalibration = value
    
    def SetProcessed(self, value):
        if value:
            self.processedCanvas.grid(row=6, columnspan=4, sticky=tk.NSEW)
        else:
            self.processedCanvas.grid_forget()
        self.showProcessed = value
        
