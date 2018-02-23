try:
    import win32ui
except ImportError:
    print('Please run "pip install pypiwin32"')    
import time
# from Util.WindowMgr import WindowMgr
import sys
    
'''
name = "TFRevolution" #just an example of a window I had open at the time
w = win32ui.FindWindow( None, name )
t1 = time.time()

count = 0
while count < 16000:    
    dc = w.GetWindowDC()
    dc.GetPixel (60,20)    
    dc.DeleteDC()
    count += 1
t2 = time.time()
tf = t2-t1
it_per_sec = int(count/tf)
print (str(it_per_sec) + " iterations per second")
'''


class Controller(object):

    def __init__(self, model, view):
        self.model = model
        self.view = view
        
        self.view.SetWindowChooserCallbacks(self._OnWindowNameChosen,
                                            self._OnRectChange,
                                            self._OnGridSizeChange)
        print(self.model.WindowSettings.rect)
        self.view.LoadWindowChooser(self.model.WindowSettings.getWindowNames(),
                                    self.model.WindowSettings.rect,
                                    self.model.WindowSettings.gridSize)

    # model.WindowSettings
    def _OnWindowNameChosen(self, value):
        print('controller got windowName change')
        self.model.WindowSettings.windowNameTarget = value

    def _OnGridSizeChange(self, value):
        self.model.WindowSettings.gridSize = value    

    def _OnRectChange(self, value):
        self.model.WindowSettings.rect = value
            
    def update(self):
        self.model.update()
