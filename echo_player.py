import pyaudio
import wave
import struct
import math
from myfunctions import clip16
from delay import delay
from echo import echo

wavfile = 'guitar2.wav'
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
                channels    = CHANNELS,
                rate        = RATE,
                input       = False,
                output      = True )

echoPlex0 = echo(gain=0.4, sustain=0.8, timeDelay=0.06, RATE=RATE)
echoPlex1 = echo(gain=0.4, sustain=0.8, timeDelay=0.06, RATE=RATE)

CONTINUE = True
## Tkinter
import tkinter as Tk    	# for Python 3
root = Tk.Tk()

sustain = Tk.IntVar()			# Define Tk variable
volumn  = Tk.IntVar()			# Define Tk variable
mydelay   = Tk.IntVar()			# Define Tk variable
sustain.set(30)  					# Initilize
volumn.set(30)  					# Initilize
mydelay.set(60)  					# Initilize
def my_quit():
  global CONTINUE
  CONTINUE = False
def my_start():
  global CONTINUE
  CONTINUE = True

def updateVolumn(event):
    global echoPlex0
    global echoPlex1
    echoPlex0.setVolumn(volumn.get()/100)
    echoPlex1.setVolumn(volumn.get()/100)

def updateSustain(event):
    global echoPlex0
    global echoPlex1
    echoPlex0.setSustain(sustain.get()/100)
    echoPlex1.setSustain(sustain.get()/100)

def updateDelay(event):
    global echoPlex0
    global echoPlex1
    echoPlex0.setMainDelay(mydelay.get()/1000)
    echoPlex1.setMainDelay(mydelay.get()/1000)

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
  variable = sustain, label = 'Sustain')
S3 = Tk.Scale(root,
  length = 200, orient = Tk.HORIZONTAL, 
  from_ = 1, to = 120,
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
BLOCKLEN = 1024
NUMBLOCKS = int(LEN/BLOCKLEN)
idx = 0
for n in range(0, NUMBLOCKS):
    # Get sample from wave file
    root.update()
    #input_bytes = stream.read(1, exception_on_overflow=False)
    input_bytes = wf.readframes(BLOCKLEN)

    # Convert string to number
    if CHANNELS == 1:
      input_tuple= struct.unpack('h' * BLOCKLEN, input_bytes)
      output_block = BLOCKLEN * [0]
      if CONTINUE:
        for i in range(BLOCKLEN):
            #y0 = (x0, x1)
            output_block[i] = int(clip16(echoPlex0.move(input_tuple[i], idx=idx)))
            idx += 1
      else:
            output_block = input_tuple
      output_bytes = struct.pack('h' * BLOCKLEN, *output_block)

    elif CHANNELS == 2:
      input_tuple= struct.unpack('hh' * BLOCKLEN, input_bytes)
      output_block = (2*BLOCKLEN) * [0]
      if CONTINUE:
        for i in range(BLOCKLEN):
            #y0 = (x0, x1)
            idx += 1
            output_block[i*2] = int(clip16(echoPlex0.move(input_tuple[i*2], idx=idx)))
            output_block[i*2+1] = int(clip16(echoPlex1.move(input_tuple[i*2+1], idx=idx)))
      else:
            output_block = input_tuple
      output_bytes = struct.pack('hh' * BLOCKLEN, *output_block)


    # Write output to audio stream
    stream.write(output_bytes)
    output.writeframes(output_bytes)

stream.stop_stream()
stream.close()
output.close()
p.terminate()
wf.close()
