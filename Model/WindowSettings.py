
def rectToString(rect):
    strings = [str(x) for x in rect]
    return ",".join(strings)
    
def rectFromString(string):
    result = string.split(",")
    return [int(x) for x in result]
    
class WindowSettings(object):
    def __init__(self,loadSettings = False):
        self.windowNameTarget = None
        self.rect = None
        self.gridSize = 0
        if loadSettings:
            self.loadSettings()
    
    def loadSettings(self):
        try:
            with open("windowSettings.cfg", "r") as f:
                lines = f.readlines()
                self.windowNameTarget = lines[0].strip()
                self.rect = rectFromString(lines[1].strip())
                self.gridSize = int(lines[2].strip())                
        except (IndexError, FileNotFoundError): #file wrong format.
            print ("Error loading windowSettings")
            
    def saveSettings(self):
        lines = []
        lines.append(str(self.windowNameTarget) + '\n')
        lines.append(rectToString(self.rect) + '\n')
        lines.append(str(self.gridSize) + '\n')
        with open("windowSettings.cfg", "w") as f:
            f.writelines(lines)
            
    def __str__(self):
        return (str(self.windowNameTarget) + ":" +
                str(self.rect) + " @ " +
                str(self.gridSize))
        