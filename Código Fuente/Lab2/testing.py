import scipy as sc
import scipy.io.wavfile
import wave
from scipy.fftpack import fftfreq, ifftshift, fftshift
from scipy.signal import kaiserord, lfilter, firwin, freqz
import scipy.integrate as intgrl
import numpy as np
from numpy import cos, pi, sin, linspace
import matplotlib as mp
import matplotlib.pyplot as mplot

i=0.0
coseno=[]
largo=[]
while i < 9:
    coseno.append(cos(2*np.pi*i))
    largo.append(i)
    i += 0.001

mplot.title("hi")
mplot.xlabel('Tiempo [s]')
mplot.ylabel('Amplitud [dB]')
mplot.plot(largo, coseno, 'indianred')
mplot.show()
