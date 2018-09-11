from enum import Enum
CaptureMode = Enum('CaptureMode', 'Win32UI mss')
CAPTURE_MODE = CaptureMode.mss
#CAPTURE_MODE = CaptureMode.mss
if CAPTURE_MODE == CaptureMode.Win32UI:
    from Model.ImageCaptureWin32UI import ImageCapture
else:
    from Model.ImageCaptureMSS import ImageCapture

from PIL import Image

class FullImageMarker(object):

    def __init__(self, settings):
        self.data = None
        self.WindowSettings = settings

    def update(self):
        self.updateSlowArray()
    
    def imageCapture(self):
        return ImageCapture(self.WindowSettings.rect, self.WindowSettings.hwndTarget)

    def updateSlowArray(self):
        image = self.imageCapture()

        if image is not None:
            self.markImage(image)
            self.data = image

    def markImage(self, image):
        pixels = image.load()
    
        startOffset = [20, 20]  # magic number :(
        garbageOffset = self.WindowSettings.garbageXOffset
        # mark player 1
        self.markPlayer(pixels, image.size, startOffset, garbageOffset)
        
        startOffset[0] += self.WindowSettings.playerDistance
        # mark player 2
        self.markPlayer(pixels, image.size, startOffset, garbageOffset)
        
    def markPlayer(self, pixels, imgsize, startOffset, garbageOffset):
        markColor = (255, 255, 255)
        garboColor = (0, 255, 0)
        gs = self.WindowSettings.gridSize
        w, h = imgsize
        for y in range(20):
            yPix = round(y * gs + startOffset[1]) 
            if yPix >= h:
                break
            for x in range(10):
                xPix = round(x * gs + startOffset[0])
                if xPix >= w:
                    break
                
                pixels[xPix, yPix] = markColor     
            xPix = round(x * gs + startOffset[0] + garbageOffset)
            if xPix >= w:
                continue
            pixels[xPix, yPix] = garboColor 
