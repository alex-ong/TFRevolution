from Model.ImageCaptureMethod import FastImageCapture
from Model.MarkMethodPixelOffset import markImageOutput

try:
    from PIL import Image    
except ImportError:
    print('Please run "pip install pillow"')

from Model.PlayerData import PlayerData
       
class FastImageMarker(object):
    def __init__(self, settings):
        self.data = [PlayerData(i) for i in range(2)]        
        self.WindowSettings = settings
        
    def update(self):
        image = FastImageCapture(self.WindowSettings.rect, self.WindowSettings.hwndTarget)
        if image is not None:
            markImageOutput(self,image)
         
    def changed(self):        
        for player in self.data:
            if player.changed:
                return True
        return False 
    
    def toDict(self):
        data = {}
        for i in range (len(self.data)):
            data["player" + str(i)] = self.data[i].toDict()                
        return data

                
