
import time
# from Util.WindowMgr import WindowMgr
import sys
    


class Controller(object):

    def __init__(self, model, view):
        self.model = model
        self.view = view
        
        self.view.SetWindowChooserCallbacks(self._OnWindowNameChosen,
                                            self._OnRectChange,
                                            self._OnGridSizeChange,
                                            self._OnSave,
                                            self._OnRefresh,
                                            self.model.GetImageArray)
        self.ShowWindowChooser()
        

    # model.WindowSettings
    def _OnWindowNameChosen(self, hwnd, name):
        print('controller got windowName change')
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
        
    def ShowWindowChooser(self):
        self.view.LoadWindowChooser(self.model.WindowSettings.getWindowNames(),
                                    self.model.WindowSettings.rect,
                                    self.model.WindowSettings.gridSize)
        
    def update(self):
        self.model.update()
