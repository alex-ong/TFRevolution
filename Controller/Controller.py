
import Networking.TCPClient as tcp 
import json
import time
messagesSent = 0
class Controller(object):

    def __init__(self, model, view):
        self.model = model
        self.view = view
        
        self.view.SetWindowChooserCallbacks(self._OnWindowNameChosen,
                                            self._OnRectChange,
                                            self._OnGridSizeChange,
                                            self._OnSave,
                                            self._OnRefresh,
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
                                    self.model.WindowSettings.playerDistance)
    def stop(self):
        self.FieldOutput.stop()
        self.FieldOutput.join()
    
    def update(self):
        self.model.update()
        minFrameTime = 0.016 #10 fps
        #output data to our fieldOutput
        if (time.time() - self.lastFieldOutput > minFrameTime):
            if (self.model.fastImageMarker.changed):        
                self.lastFieldOutput = time.time()            
                data = self.model.fastImageMarker.toDict()            
                jsonStr = json.dumps(data,indent=2)           
                self.FieldOutput.sendMessage(jsonStr)
                global messagesSent
                messagesSent +=1
                print("Messages sent:" + str(messagesSent))
            
        
