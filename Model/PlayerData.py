class PlayerData(object):

    GARBAGE_RED = 100
    MATRIX_Y = 20
    MATRIX_X = 10

    def __init__(self, playerNum):
        # access field by x, y
        self.field = [["#FF00FF" for i in range(20)]
                      for j in range(10)] 
        self.incomingGarbage = 0
        self.playerNum = playerNum
        self.changed = 0
    
    def updateField(self, x, y, value):
        if self.field[x][y] != value:
            self.changed += 1
            self.field[x][y] = value
    
    def resetGarbage(self):
        self.incomingGarbage = 0
        
    def updateGarbage(self, y, color):
        if color[0] >= PlayerData.GARBAGE_RED:
            if (self.incomingGarbage != y - 1):
                self.incomingGarbage = 0
            else:
                self.incomingGarbage = y
            
    def getData(self, x, y):
        return self.field[x][y]
      
    def toDict(self):        
        self.changed = 0
        result = {}
        result["field"] = self.field  # no need to deepcopy
        result["incomingGarbage"] = self.incomingGarbage
        return result        

