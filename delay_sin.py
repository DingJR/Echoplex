import math
RATE = 8000
vpre = 0. # Used for delay control
def getDelay(controlDelay=0.06, idx=0):
    '''
    @parameters: user-set Delay
    @returns: current delay time
    '''
    global vpre
    tau = 0.1
    # To simulate Capstan
    lb = math.e**(-1.0/(tau * RATE))
    vpre = (1 - lb) * controlDelay + lb * vpre

    # Sinusoid generation to simulate Pinch wheel
    gi = 0.001  #gain
    w0 = 3.5 * 2 * math.pi
    w1 = 22 * 2 * math.pi
    pinchDelay = gi*math.sin(w0*idx/RATE) + gi*math.sin(w1*idx/RATE)
    # To simulate tensioner

    delayTime = vpre + pinchDelay
    return delayTime

x=[]
y=[]
controls = [0.06, 0.12, 0.09]
curContrl = 0
for i in range(100000):
    x.append(i/RATE)
    if (i % 8000) == 0:
        curContrl += 1
        curContrl %= 3
    y.append(getDelay(controls[curContrl], i))
import matplotlib.pyplot as plt
plt.xlabel("Time(seconds)")
plt.ylabel("Delay Time(seconds)")
plt.plot(x,y)
plt.show()