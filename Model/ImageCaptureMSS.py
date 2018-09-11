try:
    from mss import mss
except ImportError:
    print ('Please "pip install mss"')

try:
    import win32ui
    import pywintypes
except ImportError:
    print ('Please "pip install pypiwin32"')

try:
    from PIL import Image
except ImportError:
    print ('Please "pip install pillow"')


def ImageCapture(rectangle, hwndTarget):
    x, y, w, h = rectangle        
    if w <= 0 or h <= 0:
        return None
    hwnd = hwndTarget
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