import tkinter as tk


def tryGetInt(x):
    try:
        return (True, int(x))
    except:
        return (False, 0)

    
class RectChooser(tk.Frame):

    def __init__(self, root, OnChange):
        super().__init__(root)
        
        self.x = tk.StringVar()
        self.y = tk.StringVar()
        self.w = tk.StringVar()
        self.h = tk.StringVar()
        
        # when any of these variables change, fire our event
        self.x.trace("w", lambda _, _2, _3: self.FireEvent())
        self.y.trace("w", lambda _, _2, _3: self.FireEvent())
        self.w.trace("w", lambda _, _2, _3: self.FireEvent())
        self.h.trace("w", lambda _, _2, _3: self.FireEvent())
        
        self.OnChange = OnChange
        
        tk.Label(self, text="x").grid(row=0, column=0)
        tk.Label(self, text="y").grid(row=0, column=1)
        tk.Label(self, text="w").grid(row=0, column=2)
        tk.Label(self, text="h").grid(row=0, column=3)
        tk.Entry(self, textvariable=self.x).grid(row=1, column=0)
        tk.Entry(self, textvariable=self.y).grid(row=1, column=1)
        tk.Entry(self, textvariable=self.w).grid(row=1, column=2)
        tk.Entry(self, textvariable=self.h).grid(row=1, column=3)        
    
    def FireEvent(self):   
        # convert from string to integer
        x = tryGetInt(self.x.get())
        y = tryGetInt(self.y.get())
        w = tryGetInt(self.w.get())
        h = tryGetInt(self.h.get())
        if (x[0] and y[0] and w[0] and h[0]):
            self.OnChange([item[1] for item in [x, y, w, h]])

    def show(self, value):
        x, y, w, h = value
        self.x.set(str(x))
        self.y.set(str(y))
        self.w.set(str(w))
        self.h.set(str(h))

        
class ImageCanvas(tk.Canvas):
    def __init__(self, root):
        super().__init__(root, width=500, height=400)
        self._getImg = None
        self._img = None
        
    def update(self):
        if self._getImg is not None:
            self.updateImage(self._getImg)
            
    def updateImage(self, image):
        #create image if not existing...
        if self._img is None:
            self._img = self.canvas.create_image(300,250,image=image)
        else:    
            self.canvas.itemconfig(self._img, image=image)            
        
    def SetImageSource(self, callback):
        self._getImg = callback
    
class WindowChooser(tk.Toplevel):

    def __init__(self, root):
        super().__init__(root)
        self.title("Window capture settings")    
        tk.Label(self,text="Window Target").grid(row=0,column=0)
        self.windowTarget = tk.StringVar()
        self.windowNameTargetChooser = tk.OptionMenu(self, self.windowTarget, "choice1")
        self.windowNameTargetChooser.grid(row=0,column=1)
        
        tk.Label(self,text="Capture rectangle").grid(row=1,column=0)
        self.rect = RectChooser(self, self._OnRectChange)
        self.rect.grid(row=2,column=0,columnspan=2)
        
        tk.Label(self,text="Grid distance").grid(row=3,column=0)
        self.gridSize = tk.StringVar()
        self.gridSize.trace("w", lambda a, b, c: self._OnGridSizeChange())        
        tk.Entry(self, textvariable=self.gridSize).grid(row=3,column=1)
        
        tk.Button(self, text="Save", command=self._OnSave).grid(row=4)
        
        self._GridSizeChangeCb = None
        self._RectChangeCb = None
        self._WindowNameChangeCb = None
        
        
    
    def update(self):
        self.rawCanvas.update()
            
    # call callbacks if necessary    
    def _OnGridSizeChange(self):
        value = tryGetInt(self.gridSize.get())
        if value[0] and self._GridSizeChangeCb is not None:
            self._GridSizeChangeCb(value[1])
    
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
            
    # Set callbacks
    def SetGridSizeChangeCallback(self, cb):
        self._GridSizeChangeCb = cb
    
    def SetRectChangeCallback(self, cb):
        self._RectChangeCb = cb
        
    def SetWindowNameChosenCallback(self, cb):
        self._WindowNameChangeCb = cb
            
    def SetSaveCallback(self, cb):
        self._Save = cb
                    
    def SetGetImageSource(self, cb):
        self.rawCanvas.SetImageSource(cb)
        
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
        self.gridSize.set(str(grid))
        if (autoChooseWindow is not None):
            autoChooseWindow()
