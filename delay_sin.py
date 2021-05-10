import math
RATE = 8000
vpre = 0. # Used for delay control
def getDelay(controlDelay=0.06, idx=0):
    '''
    @parameters: user-set Delay
    @returns: current delay time
    '''
    global vpre
    tau = 0.01
    # To simulate Capstan
    lb = math.e**(-1.0/(tau * RATE))
    vpre = (1 - lb) * controlDelay + lb * vpre

    # Sinusoid generation to simulate Pinch wheel
    gi = 0.001  #gain
    wi = 3.5 * 2 * math.pi
    pinchDelay = gi*math.sin(wi*idx/RATE)
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
plt.plot(x,y)
plt.show()