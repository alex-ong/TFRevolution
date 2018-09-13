import Model.ImageCaptureMethod as ImageCaptureMethod
from Model.MarkMethodPixelOffset import markImagePreview
class FullImageMarker(object):
    def __init__(self, settings):
        self.data = None
        self.WindowSettings = settings
        self.lastId = None

    def update(self):        
        image = self.imageCapture()        
        if image is not None:
            markImagePreview(self, image)
            self.data = image
    
    def imageCapture(self):
        ImageCaptureMethod.setCaptureArgs([self.WindowSettings.rect, self.WindowSettings.hwndTarget])
        imageID = ImageCaptureMethod.getImageID()
        if imageID != self.lastId:
            image = ImageCaptureMethod.getImage()
            self.lastId = imageID
            return image        

            
        
    