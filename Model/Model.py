from Model.FullImageMarker import FullImageMarker
from Model.FastImageMarker import FastImageMarker
try:
    import win32ui
except ImportError:
    print('Please run "pip install pypiwin32"')
from .WindowSettings import WindowSettings
import time


class Model(object):

    def __init__(self):    
        self.WindowSettings = WindowSettings(True)
        self.ImageArray = None  # high res
        self.PixelArray = []  # low res
        self.lastTime = time.time()
        self.slowMode = False  # bmps of entire segments
        self.fastMode = True  # very small point arrays
        self.fullImageMarker = FullImageMarker(self.WindowSettings)
        self.fastImageMarker = FastImageMarker(self.WindowSettings)
        
    def update(self):
        if self.slowMode:
            self.fullImageMarker.update()
        if self.fastMode:
            self.fastImageMarker.update()
    
    def GetImageArray(self):
        return self.fullImageMarker.data                 
        
    def GetProcessedArray(self):
        return self.fastImageMarker.data
        

    
if __name__ == '__main__':
    # quick test
    m = Model()
    
    ws = m.WindowSettings
    print("printing:" + str(ws))
    ws.windowNameTarget = "test"
    ws.rect = [0, 2, 6, 100]
    ws.gridSize = 5
    ws.saveSettings()
