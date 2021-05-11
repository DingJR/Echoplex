import math
import numpy as np
from scipy import signal
from scipy.signal import lfilter

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
            if self.end == (self.curDelay - 1):
                self.length = self.curDelay
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
            

class delay:
    def __init__(self, RATE=8000, timeDelay=0.06):
        self.RATE = RATE
        self.rs = runningSum(int(timeDelay * RATE))
        self.vpre = timeDelay # Used for delay control
        self.whiteNoiseSamples = np.random.normal(0, 1, size=RATE)
        self.b, self.a = signal.butter(2, 2 * 20 / RATE, 'low', analog=False)
        self.lpfNoise = lfilter(self.b ,self.a, self.whiteNoiseSamples)


    def getDelay(self, controlDelay=0.06, idx=0):
        '''
        @parameters: user-set Delay
        @returns: current delay time
        '''
        vpre = self.vpre
        RATE = self.RATE
        whiteNoiseSamples = self.whiteNoiseSamples
        lpfNoise = self.lpfNoise
        rs = self.rs
        tau = 0.5
        # To simulate nominal delay
        lb = math.e**(-1.0/(tau * RATE))
        vpre = lb * vpre + (1 - lb) * controlDelay

        # Sinusoid generation to simulate Pinch wheel
        g0 = 0.0006  / (math.e**((0.2-controlDelay)/controlDelay))# gain
        g1 = 0.0010  / (math.e**((0.2-controlDelay)/controlDelay))# gain
        w0 = 3.5 *  math.pi
        w1 = 22 * math.pi
        pinchDelay = g0 * math.sin(w0*idx/RATE)
        capDelay = g1 * math.sin(w1*idx/RATE)
        sinDelay = pinchDelay + capDelay

        # To simulate tensioner friction's effect
        gi = 0.005 / (math.e**((0.2-controlDelay)/controlDelay))# gain
        tensionerDelay = gi * lpfNoise[int((idx)/50) % RATE]

        delayTime = vpre + sinDelay + tensionerDelay
        rs.write(delayTime)
        delayTime = rs.getSum(int(RATE * controlDelay))
        self.vpre = vpre
        return delayTime
