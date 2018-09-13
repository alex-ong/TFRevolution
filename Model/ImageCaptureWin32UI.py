try:
    import win32ui
    import win32gui
    import win32con
    import pywintypes        
except ImportError:
    print('Please run "pip install pypiwin32"')

try:
    from PIL import Image
except ImportError:
    print('Please run "pip install pillow"')

#todo: wrap in a class

lastRectangle = None
lasthwndTarget = None
hDC = None
myDC = None
newDC = None
myBitMap = None

def InitAll():
    global hDC
    global myDC 
    global newDC 
    global myBitMap
    global lastRectangle
    global lasthwndTarget
    
    hwnd = lasthwndTarget
    x, y, w, h = lastRectangle
    hDC = win32gui.GetDC(hwnd)
    myDC = win32ui.CreateDCFromHandle(hDC)
    newDC = myDC.CreateCompatibleDC()
            
    myBitMap = win32ui.CreateBitmap()
    myBitMap.CreateCompatibleBitmap(myDC, w, h)
        
    newDC.SelectObject(myBitMap)

def ReleaseAll():
    global hDC
    global myDC 
    global newDC 
    global myBitMap
    global lasthwndTarget
    
    hwnd = lasthwndTarget
    if myDC is not None:
        myDC.DeleteDC()
        myDC = None
    if newDC is not None:
        newDC.DeleteDC()
        newDC = None
    if hDC is not None:
        win32gui.ReleaseDC(hwnd, hDC)
        hDC = None
    if myBitMap is not None:
        win32gui.DeleteObject(myBitMap.GetHandle())    
        myBitMap = None

def ImageCapture(rectangle, hwndTarget):
    global lastRectangle
    global lasthwndTarget
    global myDC
    global newDC
    global myBitMap
    x, y, w, h = rectangle
    if w <= 0 or h <= 0:
        return
    hwnd = hwndTarget
    if hwnd == 0: 
        return None
    try:        
        if lastRectangle != rectangle or lasthwndTarget != hwndTarget:
            ReleaseAll()
            lastRectangle = rectangle
            lasthwndTarget = hwndTarget 
            InitAll()

        newDC.BitBlt((0, 0), (w, h) , myDC, (x, y), win32con.SRCCOPY)
        myBitMap.Paint(newDC)
        bmpinfo = myBitMap.GetInfo()
        bmpstr = myBitMap.GetBitmapBits(True)
        im = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)
        # im.save("C:/temp/temp.png")
        # Free Resources            
        return im
    except pywintypes.error:
        raise
    except win32ui.error:
        raise
    return None

