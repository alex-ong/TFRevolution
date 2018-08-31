try:
    import win32ui
    import win32gui
    import win32con
    import pywintypes    
except ImportError:
    print('Please run "pip install pypiwin32"')
try:
    from mss import mss
except ImportError:
    print ('Please "pip install mss"')

from PIL import Image
from enum import Enum
CaptureMode = Enum('CaptureMode', 'Win32UI mss')
class FullImageMarker(object):

    def __init__(self, settings):
        self.data = None
        self.WindowSettings = settings
        self.captureMode = CaptureMode.Win32UI

    def update(self):
        self.updateSlowArray()
    
    def captureImageWin32UI(self):            
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
        
            # win32gui.SetForegroundWindow(hwnd)
            
            newDC.BitBlt((0, 0), (w, h) , myDC, (x, y), win32con.SRCCOPY)
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
            return im
        except pywintypes.error:
            pass
        except win32ui.error:
            pass

    def captureImageMSS(self):
        x, y, w, h = self.WindowSettings.rect        
        if w <= 0 or h <= 0:
            return None
        hwnd = self.WindowSettings.hwndTarget
        if hwnd == 0: 
            return None
        try:                    
            winRect = win32gui.GetWindowRect(hwnd)
            x += winRect[0]
            y += winRect[1]            
            mon = {'left': x,'top': y, 'width': w, 'height': h}
            with mss() as sct:
                sct_img = sct.grab(mon)
                img = Image.frombytes('RGB', sct_img.size, sct_img.bgra, "raw", "BGRX")
                return img
        except pywintypes.error:
            pass
        except win32ui.error:
            pass
        return None

    def updateSlowArray(self):
        if self.captureMode == CaptureMode.Win32UI:
            image = self.captureImageWin32UI()
        else:
            image = self.captureImageMSS()

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
