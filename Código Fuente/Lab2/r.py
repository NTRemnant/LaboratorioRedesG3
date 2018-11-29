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

def leer_audio(nombre):
    fs, data = sc.io.wavfile.read(nombre)
    canales = data[0].size

    if canales == 1:
        senal = data
    else:
        senal = data[:, canales - 1]

    t = len(senal) / fs
    rango_senal = linspace(0, t, len(senal))
    freqs = scipy.fftpack.fftfreq(len(senal), rango_senal[1] - rango_senal[0])
    return fs, senal, rango_senal, freqs, t

def filtro_paso_bajo(rate, senal, corte):
    numtaps = 1001
    cutoff_frecuencia = corte
    nyquist_rate = rate/2
    fir_coeff = firwin(numtaps, cutoff_frecuencia/nyquist_rate)
    senal_filtro = lfilter(fir_coeff, 1.0, senal)
    return senal_filtro

def transformada(senal):
    fft = sc.fft(senal)
    return fft

def transformada_inversa(senal):
    inversaFft = sc.ifft(senal)
    return inversaFft

def rango_data(tpo, x):
    rango_senal = linspace(0, tpo, x)
    return rango_senal

def fx_portadora(Wo, x, rango_portadora):
    portadora = x * cos(2 * pi * Wo * rango_portadora)
    print("Largo de funcion portadora") ###########
    print(len(portadora))           ###########
    return portadora

def interpolar_senal(rango_senal, senal, rango_portadora):
    f = sc.interpolate.interp1d(rango_senal, senal)
    senal_ip = f(rango_portadora)
    print("Cantiad de datos de la nueva data")  ###########
    print (len(senal_ip))                       ###########
    return senal_ip

def modulacion_am(senal_ip, portadora):
    modulacion = portadora * senal_ip
    return modulacion

def demodulacion_am(modulacion, portadora):
    #Demodular AM
    demodulacion = modulacion * portadora
    return demodulacion

def graficar_tiempo(rango_senal, senal, color, title):
    mplot.title(title)
    mplot.xlabel('Tiempo [s]')
    mplot.ylabel('Amplitud [dB]')
    mplot.plot(rango_senal, senal, color)
    mplot.show()

def graficar_frecuencia(rango_senal, senalFFT, freqs, color, title):
    mplot.title(title)
    mplot.xlabel('Frecuencia [Hz]')
    mplot.ylabel('FFT')
    mplot.plot(freqs, abs(senalFFT), color)
    mplot.show()

def main():

    # nombre = input('Ingrese el nombre del archivo .wav a trabajar: ')

    fs, senal, rango_senal, freqs, t = leer_audio('handel.wav')

    print(fs)

    fftAudioOriginal = transformada(senal)
    ifftAudioOriginal = transformada_inversa(fftAudioOriginal)

    '''
    graficar_tiempo(rango_senal, senal, 'indianred', 'Grafico Amplitud vs. Tiempo del audio leído')
    graficar_frecuencia(rango_senal, fftAudioOriginal, freqs, 'indianred', 'Grafico FFT vs. Frecuencia de la transformada del audio leído')
    '''
    rango_portadora = rango_data(t, 1000)

    senal_ip = interpolar_senal(rango_senal, senal, rango_portadora)
    graficar_tiempo(rango_portadora, senal_ip, 'indianred', 'Grafico Amplitud vs. Tiempo de señal interpolada')


    portadora = fx_portadora(1000, 0.8, rango_portadora)

    graficar_tiempo(rango_portadora, portadora, 'indianred', 'Grafico Amplitud vs. Tiempo de función portadora')

    modulacion = modulacion_am(senal_ip, portadora)

    graficar_tiempo(rango_portadora, modulacion, 'indianred', 'Grafico Amplitud vs. Tiempo de Modulada AM')

    demodulacion = demodulacion_am(modulacion, portadora)

    graficar_tiempo(rango_portadora, demodulacion, 'indianred', 'Grafico Amplitud vs. Tiempo de Demodulada AM')

    return 0

main();
