import math
import numpy as np
from scipy import signal
from scipy.signal import lfilter
from delay import delay

RATE = 8000
controls = [0.06, 0.09, 0.12, 0.15, 0.17, 0.2]
curContrl = 0
delaySys = delay(RATE=RATE, timeDelay=0.06)

import matplotlib.pyplot as plt
plt.ylim(50, 130)
plt.xlim(0, 75)
x=[]
y=[]
for i in range(600000):
    x.append(i/RATE)
    y.append(delaySys.getDelay(controls[curContrl], i))
    if ((i+1) % 200000) == 0:
        curContrl = (curContrl + 1) % len(controls)
#plt.ylim(timeDelay*1000 - 100,timeDelay * 1000 + 100)
y=np.array(y)
y = y * 1000
plt.xlabel("Time(seconds)")
plt.ylabel("Delay Time(milleseconds)")
plt.plot(x,y)
plt.show()