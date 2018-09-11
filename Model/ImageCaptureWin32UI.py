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

def ImageCapture(rectangle, hwndTarget):
    x, y, w, h = rectangle
    if w <= 0 or h <= 0:
        return
    hwnd = hwndTarget
    if hwnd == 0: 
        return None
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
        raise
    except win32ui.error:
        raise
    return None