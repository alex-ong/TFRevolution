import Networking.TCPClient as tcp 
import json
import time


class Controller(object):

    def __init__(self, model, view):
        self.model = model
        self.view = view
        
        self.view.SetWindowChooserCallbacks(self._OnWindowNameChosen,
                                            self._OnRectChange,
                                            self._OnGridSizeChange,
                                            self._OnSave,
                                            self._OnRefresh,
                                            self._OnGarbageXChange,
                                            self._OnPlayerSepChange,
                                            self.model.GetImageArray,
                                            self.model.GetProcessedArray,
                                            self._OnShowCalibration,
                                            self._OnShowProcessed,
                                            )
        self.ShowWindowChooser()
        self.FieldOutput = tcp.CreateClient("127.0.0.1", 9999)
        self.lastFieldOutput = time.time()
        
    # model.WindowSettings
    def _OnWindowNameChosen(self, hwnd, name):        
        self.model.WindowSettings.windowNameTarget = name
        self.model.WindowSettings.hwndTarget = hwnd

    def _OnGridSizeChange(self, value):
        self.model.WindowSettings.gridSize = value    

    def _OnRectChange(self, value):
        self.model.WindowSettings.rect = value
    
    def _OnSave(self):
        self.model.WindowSettings.saveSettings()
                
    def _OnRefresh(self):
        self.view.LoadWindowChooser()           
    
    def _OnGarbageXChange(self, value):
        self.model.WindowSettings.garbageXOffset = value
        
    def _OnPlayerSepChange(self, value):     
        self.model.WindowSettings.playerDistance = value

    def _OnShowProcessed(self):
        self.model.processedMode = not self.model.processedMode
        self.view.winChooser.SetProcessed(self.model.processedMode)
        
    def _OnShowCalibration(self):
        self.model.calibrationMode = not self.model.calibrationMode
        self.view.winChooser.SetCalibration(self.model.calibrationMode)
                 
    def ShowWindowChooser(self):
        self.view.LoadWindowChooser(self.model.WindowSettings.getWindowNames(),
                                    self.model.WindowSettings.rect,
                                    self.model.WindowSettings.gridSize,
                                    self.model.WindowSettings.garbageXOffset,
                                    self.model.WindowSettings.playerDistance)

    def stop(self):
        self.FieldOutput.stop()
        self.FieldOutput.join()
    
    def update(self):
        self.model.update()
        
        # We can use this to refresh update rate.
        timer = time.time()        
        '''Uncomment this to cap framerate
        minFrameTime = 0.02 # 50 fps
        if (timer - self.lastFieldOutput > minFrameTime):
            this is roughly 3fps in tetris friends.
        '''    
        if (self.model.fastImageMarker.changed() > 0):                      
            self.lastFieldOutput = timer 
            data = self.model.fastImageMarker.toDict()            
            jsonStr = json.dumps(data, indent=2)           
            self.FieldOutput.sendMessage(jsonStr)            
