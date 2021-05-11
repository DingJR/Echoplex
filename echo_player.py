# play_vibrato_interpolation.py
# Reads a specified wave file (mono) and plays it with a vibrato effect.
# (Sinusoidally time-varying delay)
# Uses linear interpolation

import pyaudio
import wave
import struct
import math
from myfunctions import clip16
from delay import delay
from echo import echo

wavfile = 'piano1.wav'
wf = wave.open( wavfile, 'rb')

# Read wave file properties
RATE        = wf.getframerate()     # Frame rate (frames/second)
WIDTH       = wf.getsampwidth()     # Number of bytes per sample
LEN         = wf.getnframes()       # Signal length
CHANNELS    = wf.getnchannels()     # Number of channels

print('The file has %d channel(s).'         % CHANNELS)
print('The file has %d frames/second.'      % RATE)
print('The file has %d frames.'             % LEN)
print('The file has %d bytes per sample.'   % WIDTH)


# Open an output audio stream
p = pyaudio.PyAudio()
stream = p.open(format      = pyaudio.paInt16,
                channels    = 1,
                rate        = RATE,
                input       = True,
                output      = True )

echoPlex = echo(gain=0.4, sustain=0.8, timeDelay=0.06, RATE=RATE)

## Tkinter
import tkinter as Tk    	# for Python 3
root = Tk.Tk()

sustain = Tk.IntVar()			# Define Tk variable
volumn  = Tk.IntVar()			# Define Tk variable
mydelay   = Tk.IntVar()			# Define Tk variable
sustain.set(30)  					# Initilize
volumn.set(30)  					# Initilize
mydelay.set(60)  					# Initilize
CONTINUE = True
def my_quit():
  global CONTINUE
  CONTINUE = False
def my_start():
  global CONTINUE
  CONTINUE = True

def updateVolumn(event):
    global echoPlex
    echoPlex.setVolumn(volumn.get()/100)

def updateSustain(event):
    global echoPlex
    echoPlex.setSustain(sustain.get()/100)

def updateDelay(event):
    global echoPlex
    echoPlex.setMainDelay(mydelay.get()/1000)

B1 = Tk.Button(root, text = 'TurnUp', command = my_start)
B2 = Tk.Button(root, text = 'TurnOff', command = my_quit)
S1 = Tk.Scale(root,
  length = 200, orient = Tk.HORIZONTAL, 
  from_ = 1, to = 100,
  command = updateVolumn,
  variable = volumn, label = 'Volumn')
S2 = Tk.Scale(root,
  length = 200, orient = Tk.HORIZONTAL, 
  from_ = 1, to = 100,
  command = updateSustain,
  variable = sustain, label = 'sustain')
S3 = Tk.Scale(root,
  length = 200, orient = Tk.HORIZONTAL, 
  from_ = 1, to = 1000,
  command = updateDelay,
  variable = mydelay, label = 'Main Delay')
L1 = Tk.Label(root, text="Echoplex")

L1.pack()
B1.pack()
B2.pack()
S1.pack()
S2.pack()
S3.pack()

output = wave.open("outputFile.wav", 'wb')
output.setnchannels(CHANNELS)			# two channels (stereo)
output.setsampwidth(WIDTH)			# two bytes per sample (16 bits per sample)
output.setframerate(RATE)			# samples per second

# Loop through wave file 
#LEN = 100000000
for n in range(0, LEN):
    # Get sample from wave file
    root.update()
    #input_bytes = stream.read(1, exception_on_overflow=False)
    input_bytes = wf.readframes(1)

    # Convert string to number
    x0,  = struct.unpack('h', input_bytes)

    if CONTINUE:
        y0 = echoPlex.move(x0, idx=n)
    else:
        y0 = x0

    # Clip and convert output value to binary data
    output_bytes = struct.pack('h', int(clip16(y0)))

    # Write output to audio stream
    stream.write(output_bytes)
    output.writeframes(output_bytes)

stream.stop_stream()
stream.close()
output.close()
p.terminate()
wf.close()
