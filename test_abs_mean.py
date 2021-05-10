import math
import numpy as np
from scipy import signal
from scipy.signal import lfilter
from delay import delay

RATE = 8000
controls = [0.06, 0.09, 0.12, 0.15, 0.17, 0.2]
curContrl = 0

import matplotlib.pyplot as plt
plt.ylim(-1, 12)
plt.xlim(0, 13)
x=[]
y=[]
delaySys = delay(RATE=RATE, timeDelay=0.06)

for i in range(600000):
    x.append((i%100000)/RATE)
    y.append(delaySys.getDelay(controls[curContrl], i))
    if ((i+1) % 100000) == 0:
        y=np.array(y)
        y = y - controls[curContrl]
        y = y * 1000 + 2 * curContrl
        plt.plot(x,y)
        x=[]
        y=[]
        curContrl = (curContrl + 1) % len(controls)
#plt.ylim(timeDelay*1000 - 100,timeDelay * 1000 + 100)
plt.legend(["0.06","0.09","0.12","0.15","0.18","0.2"])
plt.show()