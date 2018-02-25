try:
    import win32ui
    import win32gui
    import win32con
    import pywintypes
except ImportError:
    print('Please run "pip install pypiwin32"')
from PIL import Image

class FullImageMarker(object):

    def __init__(self, settings):
        self.data = None
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
            self.data = im      
             
        except pywintypes.error:
            pass
        except win32ui.error:
            pass

    def markImage(self, image):
        pixels = image.load()
    
        startOffset = [20, 20]  # magic number :(
        # mark player 1
        self.markPlayer(pixels, image.size, startOffset)
        
        startOffset[0] += self.WindowSettings.playerDistance
        # mark player 2
        self.markPlayer(pixels, image.size, startOffset)
        
    def markPlayer(self, pixels, imgsize, startOffset):
        markColor = (255, 255, 255)
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
