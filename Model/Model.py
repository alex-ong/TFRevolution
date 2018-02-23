try:
    import win32ui
    import win32gui
    import win32con
    import pywintypes
except ImportError:
    print('Please run "pip install pypiwin32"')
from PIL import Image    
from .WindowSettings import WindowSettings
import time


class Model(object):

    def __init__(self):    
        self.WindowSettings = WindowSettings(True)
        self.ImageArray = None #high res
        self.PixelArray = [] #low res
        self.lastTime = time.time()
        self.slowMode = True  # bmps of entire segments
        self.fastMode = False  # very small point arrays
    
    def update(self):
        if self.slowMode:
            self.updateSlowArray()
        if self.fastMode:
            self.updatePixelArray()
    
    def GetImageArray(self):
        return self.ImageArray
    
    def updateSlowArray(self):
        # todo: use windowSettings class..
        x,y,w,h = self.WindowSettings.rect
        if w <= 0 or h <= 0:
            return
        hwnd = self.WindowSettings.hwndTarget
        if hwnd != 0:
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
                self.ImageArray = im      
                print ("yay")  
            except pywintypes.error:
                print ("error")
            except win32ui.error:
                print ("error")
    
    def updatePixelArray(self):
        try:
            w = win32ui.FindWindow(None, "Untitled - Notepad")
        except win32ui.error:
            return  # no window found                
        print ("found window...")
        count = 0
        dc = w.GetWindowDC()
        while count < 1000:                
            dc.GetPixel (60, 20)         
            count+= 1
        dc.DeleteDC()        
        print ("woot!")

    
if __name__ == '__main__':
    # quick test
    m = Model()
    
    ws = m.WindowSettings
    print("printing:" + str(ws))
    ws.windowNameTarget = "test"
    ws.rect = [0, 2, 6, 100]
    ws.gridSize = 5
    ws.saveSettings()
