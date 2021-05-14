class runningSum:
    def __init__(self, input):
        self.curDelay = input
        self.acc = 0
        self.allDelay = [0] * 5000
        self.strt = 0
        self.end  = 0
        self.length = 0
        self.isFull = False
    
    def write(self, v=0.):
        self.end = (self.end + 1) % len(self.allDelay)
        self.allDelay[self.end] = v
        if self.isFull:
            self.acc -= self.allDelay[self.strt]
            self.acc += self.allDelay[self.end]
            self.strt =  (self.strt + 1) % len(self.allDelay)
        else :
            self.acc += self.allDelay[self.end]
            self.length += 1
            #if self.end == (self.curDelay - 1):
            if self.length == self.curDelay:
                self.isFull = True

    def getSum(self, controlDelay=480):
        if self.curDelay != controlDelay:
            if self.length > controlDelay:
                while self.length > controlDelay:
                    self.acc -= self.allDelay[self.strt]
                    self.strt =  (self.strt + 1) % len(self.allDelay)
                    self.length -= 1
            elif self.length < int(controlDelay):
                while self.length < controlDelay:
                    self.strt =  (self.strt - 1) % len(self.allDelay)
                    self.acc += self.allDelay[self.strt]
                    self.length += 1
            self.curDelay = controlDelay
        return self.acc/self.length