try:
    import win32ui
except:
    print ("please run command: pip install pypiwin32")
import time
from Util.WindowMgr import WindowMgr
import sys
    
'''
name = "TFRevolution" #just an example of a window I had open at the time
w = win32ui.FindWindow( None, name )
t1 = time.time()

count = 0
while count < 16000:    
    dc = w.GetWindowDC()
    dc.GetPixel (60,20)    
    dc.DeleteDC()
    count += 1
t2 = time.time()
tf = t2-t1
it_per_sec = int(count/tf)
print (str(it_per_sec) + " iterations per second")
'''

class Controller(object):
    def __init__(self, model, view):
        self.model = model
        self.view = view
    
    def update(self, timeDelta):
        self.model.update()