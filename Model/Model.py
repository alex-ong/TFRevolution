from .WindowSettings import WindowSettings
class Model(object):
    def __init__(self):
        self.WindowSettings = WindowSettings(True)
    
    def update(self):
        pass
    
if __name__ == '__main__':
    #quick test
    m = Model()
    
    ws = m.WindowSettings
    print("printing:" + str(ws))
    ws.windowNameTarget = "test"
    ws.rect = [0,2,6,100]
    ws.gridSize = 5
    ws.saveSettings()