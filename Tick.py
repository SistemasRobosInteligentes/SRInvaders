class Tick():
    def __init__(self):
        self.tick = 0

    def addTick(self,value):
        self.tick = self.tick + value
    
    def getTick(self):
        return self.tick