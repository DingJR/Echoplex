import math
RATE = 8000
vpre = 0.06 # Used for delay control
def getDelay(controlDelay=0.06, idx=0):
    '''
    @parameters: user-set Delay
    @returns: current delay time
    '''
    global vpre
    tau = 0.6
    lb = math.e**(-1.0/(tau * RATE))
    vpre = (1 - lb) * controlDelay + lb * vpre
    delayTime = vpre
    return delayTime

x=[]
y=[]
controls = [0.06, 0.12, 0.09]
curContrl = 0
for i in range(110000):
    x.append(i/RATE)
    if ((i+1) % 40000) == 0:
        curContrl += 1
        curContrl %= 3
    y.append(getDelay(controls[curContrl], i))
import matplotlib.pyplot as plt
plt.xlabel("Time(seconds)")
plt.ylabel("Delay Time(seconds)")
plt.plot(x,y)
plt.show()