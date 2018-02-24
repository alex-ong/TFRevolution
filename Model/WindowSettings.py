from Util.WindowMgr import WindowMgr

def rectToString(rect):
    strings = [str(x) for x in rect]
    return ",".join(strings)
    
def rectFromString(string):
    result = string.split(",")
    return [int(x) for x in result]
    
class WindowSettings(object):
    def __init__(self,loadSettings = False):
        self.winmgr = WindowMgr()
        self.windowNameTarget = "None"
        self.hwndTarget = 0
        self.rect = [0,0,0,0]
        self.gridSize = 0
        self.playerDistance = 140
        if loadSettings:
            self.loadSettings()
    
    def setTarget(self, hwnd, name):
        self.hwndTarget = hwnd
        self.windowNameTarget = name
        
    def loadSettings(self):
        try:
            with open("windowSettings.cfg", "r") as f:
                lines = f.readlines()
                self.windowNameTarget = lines[0].strip()
                self.rect = rectFromString(lines[1].strip())
                self.gridSize = float(lines[2].strip())
                self.playerDistance = float(lines[3].strip())                
        except (IndexError, FileNotFoundError): #file wrong format.
            print ("Error loading windowSettings")
            
    def saveSettings(self):
        lines = []
        lines.append(str(self.windowNameTarget) + '\n')
        lines.append(rectToString(self.rect) + '\n')
        lines.append(str(self.gridSize) + '\n')
        lines.append(str(self.playerDistance) + '\n')
        with open("windowSettings.cfg", "w") as f:
            f.writelines(lines)
    
    def getWindowNames(self):
        result = self.winmgr.getWindows()
        foundIndex = -1
        for i in range(len(result)):
            if self.windowNameTarget == result[i][1]:
                foundIndex = i
                break
        if foundIndex != -1:
            foundItem = result[foundIndex]
            result.remove(foundItem)
            result = [foundItem] + result
        return result
    
    def __str__(self):
        return (str(self.windowNameTarget) + ":" +
                str(self.rect) + " @ " +
                str(self.gridSize))
        