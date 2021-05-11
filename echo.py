import math
from delay import delay
def circlyBack(idx, BUFFER_LEN):
    if idx >= BUFFER_LEN:
        return idx - BUFFER_LEN
    if idx < 0:
        return idx + BUFFER_LEN
    return idx

class echo:
    def __init__(self, gain = 0.9, sustain = 0.8, timeDelay=0.06,  RATE=8000):
        ## Need code: Change to delay system
        p1_time = timeDelay + 0.0
        p2_time = timeDelay + 0.06
        p3_time = timeDelay + 0.12
        self.gain = gain
        self.sustain = sustain
        self.p_time = [p1_time, p2_time, p3_time]
        self.RATE = RATE
        self.BUFFER_LEN = int(RATE * 2) + 2
        self.buffer = self.BUFFER_LEN * [0]
        self.wr = [0, 0, 0, int(0.5 * self.BUFFER_LEN) + 1]
        self.delaySys = [delay(RATE=RATE, timeDelay=self.p_time[0]), delay(RATE=RATE, timeDelay=self.p_time[1]), delay(RATE=RATE, timeDelay=self.p_time[2])]
        for i in range(3):
            self.wr[i] = self.wr[3] - int(self.delaySys[i].getDelay(controlDelay=self.p_time[i], idx=0) * RATE)

    def interpolate(self, kr):
        kr_prev = int(math.floor(kr))
        frac = kr - kr_prev    # 0 <= frac < 1
        kr_next = kr_prev + 1
        if kr_next == self.BUFFER_LEN:
            kr_next = 0
        return (1-frac) * self.buffer[kr_prev] + frac * self.buffer[kr_next]

    def move(self, input, idx = 0, p1_time=0.06, p2_time=0.12, p3_time=0.18):
        '''
        @parameters: read x0 from input stream
        @return:     mixed output value
        '''
        x = self.sustain * (self.interpolate(self.wr[0]) + self.interpolate(self.wr[1]) + self.interpolate(self.wr[2])) / 3 + input
        y0 = self.gain * (self.interpolate(self.wr[0]) + self.interpolate(self.wr[1]) + self.interpolate(self.wr[2])) + input
        self.buffer[self.wr[3]] = x
        self.wr[3] = circlyBack(self.wr[3] + 1, self.BUFFER_LEN)
        for i in range(3):
            self.wr[i] = circlyBack(self.wr[3] - int(self.delaySys[i].getDelay(controlDelay=self.p_time[i], idx=idx) * self.RATE), self.BUFFER_LEN)
            #self.wr[i] = circlyBack(self.wr[i] + 1, self.BUFFER_LEN)
        return y0

    def setMainDelay(self, timeDelay=0.06):
        p1_time = timeDelay + 0.0
        p2_time = timeDelay + 0.06
        p3_time = timeDelay + 0.12
        self.p_time = [p1_time, p2_time, p3_time]
    
    def setVolumn(self, Gain=0.8):
        self.gain = Gain

    def setSustain(self, Sustain=0.8):
        self.sustain = Sustain