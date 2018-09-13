import Model.ImageCaptureMethod as ImageCaptureMethod
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
        self.lastId = None

    def update(self):
        image = self.imageCapture()    
        if image is not None:
            markImageOutput(self,image)
    
    def imageCapture(self):        
        ImageCaptureMethod.setCaptureArgs([self.WindowSettings.rect, self.WindowSettings.hwndTarget])
        imageID = ImageCaptureMethod.getImageID()
        if imageID != self.lastId:
            image = ImageCaptureMethod.getImage()            
            self.lastId = imageID
            return image     

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
            