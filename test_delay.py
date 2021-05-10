import math
import numpy as np
from scipy import signal
from scipy.signal import lfilter
from delay import getDelay

RATE = 8000
controls = [0.06, 0.09, 0.12, 0.15, 0.17, 0.2]
curContrl = 0

import matplotlib.pyplot as plt
plt.ylim(50, 205)
plt.xlim(0, 75)
x=[]
y=[]
for i in range(600000):
    x.append(i/RATE)
    y.append(getDelay(controls[curContrl], i))
    if ((i+1) % 100000) == 0:
        curContrl = (curContrl + 1) % len(controls)
#plt.ylim(timeDelay*1000 - 100,timeDelay * 1000 + 100)
y=np.array(y)
y = y * 1000
plt.plot(x,y)
plt.show()