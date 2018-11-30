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

def fx_portadora(Wo, A, rango_portadora):
    portadora = A * cos(2 * pi * Wo * rango_portadora)
    print("Largo de funcion portadora") ###########
    print(len(portadora))           ###########
    return portadora

def interpolar_senal(rango_senal, senal, rango_portadora):
    f = sc.interpolate.interp1d(rango_senal, senal)
    senal_ip = f(rango_portadora)
    print("Cantiad de datos de la nueva data")  ###########
    print (len(senal_ip))                       ###########
    return senal_ip

def modulacion_am(senal, portadora):
    modulacion = portadora * senal
    return modulacion

def demodulacion_am(modulacion, portadora):
    #Demodular AM
    demodulacion = (modulacion/portadora)/40000
    return demodulacion

def modulacion_fm(senal, rango_senal, amplitud, w0, k):
    integral = sc.integrate.cumtrapz(senal, rango_senal, initial=0)
    modulacion = amplitud * cos(w0*2*pi*rango_senal + 2*pi*k*integral)
    return modulacion

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

def multi_grafico_tiempo(rango, senal_1, title_1, senal_2, title_2, senal_3, title_3, senal_4, title_4):
    mplot.figure()
    mplot.subplot(411)
    mplot.title(title_1)
    mplot.xlabel('Tiempo [s]')
    mplot.ylabel('Amplitud [dB]')
    mplot.plot(rango, senal_1, 'y')
    mplot.subplot(412)
    mplot.title(title_2)
    mplot.xlabel('Tiempo [s]')
    mplot.ylabel('Amplitud [dB]')
    mplot.plot(rango, senal_2, 'green')
    mplot.subplot(413)
    mplot.title(title_3)
    mplot.xlabel('Tiempo [s]')
    mplot.ylabel('Amplitud [dB]')
    mplot.plot(rango, senal_3, 'blue')
    mplot.subplot(414)
    mplot.title(title_4)
    mplot.xlabel('Tiempo [s]')
    mplot.ylabel('Amplitud [dB]')
    mplot.plot(rango, senal_4, 'indianred')
    mplot.show()

def multi_grafico_comparativo(rango, senal_1, title_1, senal_2, title_2, senal_3, title_3, senal_4, title_4):
    mplot.figure()
    mplot.subplot(411)
    mplot.title(title_1)
    mplot.xlabel('Tiempo [s]')
    mplot.ylabel('Amplitud [dB]')
    mplot.plot(rango, senal_1, 'y')
    mplot.subplot(412)
    mplot.title(title_2)
    mplot.xlabel('Tiempo [s]')
    mplot.ylabel('Amplitud [dB]')
    mplot.plot(rango, senal_2, 'green')
    mplot.plot(rango, senal_1, 'indianred')
    mplot.subplot(413)
    mplot.title(title_3)
    mplot.xlabel('Tiempo [s]')
    mplot.ylabel('Amplitud [dB]')
    mplot.plot(rango, senal_3, 'blue')
    mplot.subplot(414)
    mplot.title(title_4)
    mplot.xlabel('Tiempo [s]')
    mplot.ylabel('Amplitud [dB]')
    mplot.plot(rango, senal_4, 'yellow')
    mplot.show()

def main():

    # nombre = input('Ingrese el nombre del archivo .wav a trabajar: ')

    fs, senal, rango_senal, freqs, t = leer_audio('handel.wav')

    print(fs)

    fftAudioOriginal = transformada(senal)
    ifftAudioOriginal = transformada_inversa(fftAudioOriginal)


    graficar_tiempo(rango_senal, senal, 'indianred', 'Grafico Amplitud vs. Tiempo del audio leído')
    graficar_frecuencia(rango_senal, fftAudioOriginal, freqs, 'indianred', 'Grafico FFT vs. Frecuencia de la transformada del audio leído')

    '''
    rango_portadora = rango_data(t, len(senal))

    senal_ip = interpolar_senal(rango_senal, senal, rango_portadora)
    graficar_tiempo(rango_portadora, senal_ip, 'indianred', 'Grafico Amplitud vs. Tiempo de señal interpolada')
    '''

    portadora_A08 = fx_portadora(15*fs, 0.2, rango_senal)
    portadora_A1  = fx_portadora(15*fs, 1.0, rango_senal)
    portadora_A12 = fx_portadora(15*fs, 1.8, rango_senal)

    multi_grafico_tiempo(rango_senal, senal, 'Amplitud vs Tiempo Original', portadora_A08, 'Amplitud vs Tiempo Portadora 20%', portadora_A1, 'Amplitud vs Tiempo Portadora 100%', portadora_A12, 'Amplitud vs Tiempo Portadora 180%')

    # graficar_tiempo(rango_senal, portadora_A08, 'indianred', 'Grafico Amplitud vs. Tiempo de función portadora')

    modulacion_A08 = modulacion_am(senal, portadora_A08)
    modulacion_A1 = modulacion_am(senal, portadora_A1)
    modulacion_A12 = modulacion_am(senal, portadora_A12)

    multi_grafico_tiempo(rango_senal, senal, 'Amplitud vs Tiempo Original', modulacion_A08, 'Amplitud vs Tiempo Modulación 20%', modulacion_A1, 'Amplitud vs Tiempo Modulación 100%', modulacion_A12, 'Amplitud vs Tiempo Modulación 180%')


    # graficar_tiempo(rango_senal, modulacion_A08, 'indianred', 'Grafico Amplitud vs. Tiempo de Modulada AM')

    demodulacion = demodulacion_am(modulacion_A1, portadora_A1)

    graficar_tiempo(rango_senal, demodulacion, 'indianred', 'Grafico Amplitud vs. Tiempo de Demodulada AM')


    fft_lpf = filtro_paso_bajo(8*fs, demodulacion, 20000)

    graficar_tiempo(rango_senal, fft_lpf, 'indianred', 'Grafico Amplitud vs. Tiempo de Demodulada pasa bajo AM')

    modulacion_F08 = modulacion_fm(senal, rango_senal, 25000, 44100, 0.8)
    modulacion_F1  = modulacion_fm(senal, rango_senal, 25000, 44100, 1.0)
    modulacion_F12 = modulacion_fm(senal, rango_senal, 25000, 44100, 1.2)

    multi_grafico_tiempo(rango_senal, senal, 'Amplitud vs Tiempo Original',
                         modulacion_F08, 'Amplitud vs Tiempo Modulación k = 80%', modulacion_F1, 'Amplitud vs Tiempo Modulación 100%',
                         modulacion_F12, 'Amplitud vs Tiempo Modulación 120%')

    scipy.io.wavfile.write('dem1.wav',fs, fft_lpf)

    return 0

main();
