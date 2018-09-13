from enum import Enum
import threading
import time
CaptureMode = Enum('CaptureMode', 'Win32UI mss')

CAPTURE_MODE = CaptureMode.Win32UI

if CAPTURE_MODE == CaptureMode.Win32UI:
    from Model.ImageCaptureWin32UI import ImageCapture
else:
    from Model.ImageCaptureMSS import ImageCapture

import Networking.StoppableThread as StoppableThread

class ThreadedWinCapture(StoppableThread.StoppableThread):
    def __init__(self, *args):
        self.captureArgs = None
        self.currentImage = None
        self.imageId = 0
        self.captureArgLock = threading.Lock()
        self.imageLock = threading.Lock()        
        super().__init__(*args)    
            
    def setCaptureArgs(self, captureArgs):
        self.captureArgLock.acquire()
        self.captureArgs = captureArgs
        self.captureArgLock.release()

    def getCaptureArgs(self):
        self.captureArgLock.acquire()
        result = self.captureArgs
        self.captureArgLock.release()
        return result

    def getImageId(self):
        self.imageLock.acquire()
        result = self.imageId
        self.imageLock.release()
        return result
    
    def getCurrentImage(self):
        self.imageLock.acquire()
        result = self.currentImage
        self.imageLock.release()
        return result

    def run(self):        
        timer = time.time()
        # Create a socket (SOCK_STREAM means a TCP socket)
        while not self.stopped():                
            captureArgs = self.getCaptureArgs()
            if captureArgs is not None:
                rectangle, hwndTarget = captureArgs
                image = ImageCapture(rectangle, hwndTarget)
                if image is not None:
                    self.imageLock.acquire()
                    self.currentImage = image
                    self.imageId += 1
                    self.imageLock.release()
                    print (1.0 / (time.time() - timer))
                    timer = time.time()

#todo: static single instance winCapture.
myWinCap = ThreadedWinCapture()
myWinCap.start()

def setCaptureArgs(args):       
    myWinCap.setCaptureArgs(args)

def getImageID():
    return myWinCap.getImageId()    
    
def getImage():
    return myWinCap.getCurrentImage()
