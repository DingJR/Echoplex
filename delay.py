import math
import numpy as np
from scipy import signal
from scipy.signal import lfilter
from runningsum import runningSum
class delay:
    def __init__(self, RATE, timeDelay=0.06):
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
        tau = 1
        # To simulate nominal delay
        lb = math.e**(-1.0/(tau * RATE))
        vpre = lb * vpre + (1 - lb) * controlDelay
        self.vpre = vpre

        # Sinusoid generation to simulate Pinch wheel
        g0 = 0.0006  / (math.e**((0.2-controlDelay)/controlDelay))# gain
        g1 = 0.0010  / (math.e**((0.2-controlDelay)/controlDelay))# gain
        w0 = 3.5 *  2 * math.pi
        w1 = 22 * 2 * math.pi
        pinchDelay = g0 * math.sin(w0*idx/RATE)
        capDelay = g1 * math.sin(w1*idx/RATE)
        sinDelay = pinchDelay + capDelay

        # To simulate tensioner friction's effect
        gi = 0.005 / (math.e**((0.2-controlDelay)/controlDelay))# gain
        tensionerDelay = gi * lpfNoise[int((idx)/50) % RATE]

        delayTime = vpre + sinDelay + tensionerDelay
        rs.write(delayTime)
        delayTime = rs.getSum(int(RATE * controlDelay))
        return delayTime
