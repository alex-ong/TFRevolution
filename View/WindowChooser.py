import tkinter as tk

from View.RectChooser import RectChooser 
from View.ImageCanvas import ImageCanvas
from View.NumberChooser import NumberChooser

#todo move this copy to Util.
def tryGetInt(x):
    try:
        return (True, int(x))
    except:
        return (False, 0)


class WindowChooser(tk.Frame):

    def __init__(self, root):
        super().__init__(root)        
        tk.Label(self,text="Window Target").grid(row=0,column=0)
        self.windowTarget = tk.StringVar()
        self.windowNameTargetChooser = tk.OptionMenu(self, self.windowTarget, "choice1")
        self.windowNameTargetChooser.grid(row=0,column=1)
        tk.Button(self, text="Refresh window list", command=self._OnRefresh).grid(row=0,column=2)
        
        tk.Label(self,text="Capture rectangle").grid(row=1,column=0)
        self.rect = RectChooser(self, self._OnRectChange)
        self.rect.grid(row=2,column=0,columnspan=3)
        
        self.gridSize = NumberChooser(self, 'gridSizePixels', self._OnGridSizeChange)
        tk.Label(self,text="Grid distance").grid(row=3,column=0)        
        self.gridSize.grid(row=3, columnspan=2)
        
        tk.Button(self, text="Save", command=self._OnSave).grid(row=4)        
        self.imageCanvas = ImageCanvas(self)
        self.imageCanvas.grid(row=5,columnspan=4,sticky=tk.NSEW)
        
        self._GridSizeChangeCb = None
        self._RectChangeCb = None
        self._WindowNameChangeCb = None
        self._RefreshCb = None
        
    
    def update(self):
        self.imageCanvas.update()
            
    # call callbacks if necessary    
    def _OnGridSizeChange(self):
        success, value = tryGetInt(self.gridSize.value.get())
        if success and self._GridSizeChangeCb is not None:
            self._GridSizeChangeCb(value)
    
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
        self.imageCanvas.SetImageSource(cb)
        
    def show(self, names, rect, grid):
        self.windowNameTargetChooser['menu'].delete(0, 'end')         
        self.windowTarget.set(str(names[0][1]))
        autoChooseWindow = None #calculate hwnd and send to model if it is present
        
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
        if (autoChooseWindow is not None):
            autoChooseWindow()
