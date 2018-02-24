try:
    import win32ui
    import win32gui
    import win32con
    import pywintypes
    from PIL import Image
    
except ImportError:
    print('Please run "pip install pypiwin32"')

from enum import Enum
def hexNoLeader(number):
    return hex(number).replace("0x","")

def ToHex(numbers):
    return ('#' + hexNoLeader(numbers[0]).zfill(2) +
                hexNoLeader(numbers[1]).zfill(2) +
                hexNoLeader(numbers[2]).zfill(2))


    
class PlayerData(object):

    def __init__(self, playerNum):
        # access field by x, y
        self.field = [["#FF00FF" for i in range(20)]
                      for j in range(10)] 
        self.incomingGarbage = 0
        self.playerNum = playerNum
        self.changed = False
    
    def updateField(self,x,y, value):
        if self.field[x][y] != value:
            self.changed = True
            self.field[x][y] = value
            
    def getData(self, x, y):
        return self.field[x][y]
      
    def toDict(self):        
        self.changed = False
        result = {}
        result["field"] = self.field #no need to deepcopy
        result["incomingGarbage"] = self.incomingGarbage
        return result        
    
class FastImageMarker(object):
    def __init__(self, settings):
        self.data = [PlayerData(i) for i in range(2)]        
        self.WindowSettings = settings
        
    def update(self):
        self.updateSlowArray()
        
    def updateSlowArray(self):
        # todo: use windowSettings class..
        x, y, w, h = self.WindowSettings.rect
        if w <= 0 or h <= 0:
            return
        hwnd = self.WindowSettings.hwndTarget
        if hwnd == 0: 
            return
        try:        
            hDC = win32gui.GetDC(hwnd)
            myDC = win32ui.CreateDCFromHandle(hDC)
            newDC = myDC.CreateCompatibleDC()
        
            myBitMap = win32ui.CreateBitmap()
            myBitMap.CreateCompatibleBitmap(myDC, w, h)
        
            newDC.SelectObject(myBitMap)
        
            win32gui.SetForegroundWindow(hwnd)
            
            newDC.BitBlt((x, y), (w, h) , myDC, (0, 0), win32con.SRCCOPY)
            myBitMap.Paint(newDC)
            bmpinfo = myBitMap.GetInfo()
            bmpstr = myBitMap.GetBitmapBits(True)
            im = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)                    
            # im.save("C:/temp/temp.png")
            # Free Resources
            myDC.DeleteDC()
            newDC.DeleteDC()
            win32gui.ReleaseDC(hwnd, hDC)
            win32gui.DeleteObject(myBitMap.GetHandle())
            self.markImage(im)              
        except pywintypes.error:
            pass
        except win32ui.error:
            pass

    def markImage(self, image):
        pixels = image.load()
    
        startOffset = [20, 20]  # magic number :(
        # mark player 1
        for player in self.data:
            self.markPlayer(player, pixels, image.size, startOffset)            
            startOffset[0] += self.WindowSettings.playerDistance
        
    def markPlayer(self, player, pixels, imgsize, startOffset):
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
                player.updateField(x,y, ToHex(pixels[xPix,yPix]))
                
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

                