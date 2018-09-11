from Model.ImageCaptureMethod import FastImageCapture

try:
    from PIL import Image    
except ImportError:
    print('Please run "pip install pillow"')

from enum import Enum


def hexNoLeader(number):
    return hex(number).replace("0x", "")


def ToHex(numbers):
    return ('#' + hexNoLeader(numbers[0]).zfill(2) + 
                hexNoLeader(numbers[1]).zfill(2) + 
                hexNoLeader(numbers[2]).zfill(2))
from Model.PlayerData import PlayerData
       
class FastImageMarker(object):
    MATRIX_Y = 20
    MATRIX_X = 10

    def __init__(self, settings):
        self.data = [PlayerData(i) for i in range(2)]        
        self.WindowSettings = settings
        
    def update(self):
        image = FastImageCapture(self.WindowSettings.rect, self.WindowSettings.hwndTarget)
        if image is not None:
            self.markImage(image)

    def markImage(self, image):
        pixels = image.load()
        garbageOffset = self.WindowSettings.garbageXOffset
        startOffset = [20, 20]  # magic number :(
        # mark player 1
        for player in self.data:
            self.markPlayer(player, pixels, image.size, garbageOffset, startOffset)            
            startOffset[0] += self.WindowSettings.playerDistance
        
    def markPlayer(self, player, pixels, imgsize, garbageOffset, startOffset):
        player.resetGarbage()
        gs = self.WindowSettings.gridSize
        w, h = imgsize
        y = 0
        x = 0

        for y in range(FastImageMarker.MATRIX_Y):
            yPix = round(y * gs + startOffset[1]) 
            if yPix >= h:
                break
            for x in range(FastImageMarker.MATRIX_X):
                xPix = round(x * gs + startOffset[0])
                if xPix >= w:
                    break
                player.updateField(x, y, ToHex(pixels[xPix, yPix]))
        
        # garbage detection
        for y in range(FastImageMarker.MATRIX_Y - 1, -1, -1):
            yPix = round(y * gs + startOffset[1])
            xPix = round(x * gs + startOffset[0] + garbageOffset)
            if xPix >= w or yPix >= h:
                continue
            player.updateGarbage(20 - y, pixels[xPix, yPix])
             
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

                
