from Model.ImageCaptureMethod import FullImageCapture
from Model.MarkMethodPixelOffset import markImagePreview
class FullImageMarker(object):
    def __init__(self, settings):
        self.data = None
        self.WindowSettings = settings

    def update(self):
        image = self.imageCapture()
        
        if image is not None:
            markImagePreview(self, image)
            self.data = image
    
    def imageCapture(self):
        return FullImageCapture(self.WindowSettings.rect, self.WindowSettings.hwndTarget)   

            
        
    