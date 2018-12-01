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

# La función leer_audio se encarga de abrir el archivo a partir de una dirección pedida por pantalla.
# En ella se obtienen los datos del archivo .wav con la función read de Scipy. Se entrega el tiempo de
# muestreo, un arreglo de tiempos en los que se toman los datos, el rate del archivo y los datos leídos.
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

# Funcion que realiza el filtro paso bajo de una transformada de una señal, entra el ratio, la transformada y el valor de frecuencia de corte
# Retorna la señal filtrada.
def filtro_paso_bajo(rate, senal, corte):
    numtaps = 1001
    cutoff_frecuencia = corte
    nyquist_rate = rate/2
    fir_coeff = firwin(numtaps, cutoff_frecuencia/nyquist_rate)
    senal_filtro = lfilter(fir_coeff, 1.0, senal)
    return senal_filtro

# La función transformada de encarga de aplicar la funcion fft de scipy a la señal obtenido del archivo,
#  esta función entrega el arreglo de datos que corresponden a la transformada de Fourier.
def transformada(senal):
    fft = sc.fft(senal)
    return fft

# La función transformada_inversa de encarga de aolicar la funcion ifft de scipy a una fft,
#  esta función entrega el arreglo de datos que corresponden a la transformada inversa de Fourier.
def transformada_inversa(senal):
    inversaFft = sc.ifft(senal)
    return inversaFft

def rango_data(tpo, x):
    rango_senal = linspace(0, tpo, x)
    return rango_senal

def fx_portadora(Wo, A, rango_portadora):
    portadora = A * cos(2 * pi * Wo * rango_portadora)
    return portadora

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

# Las funciones graficar_tiempo y graficar_frecuencia se encargan de elaborar los graficos, difieren en los parametros, pero su
# comportamiento es el mismno, graficar_tiempo entrega un grafico de la señal en el tiempo y graficar_frecuencia entrega un
# grafico de la transformada de la señal en la frecuencia.
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

# La funcion multi_grafico_tiempo entrega un grafico compartivo de distintas señales en el tiempo.
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
    mplot.plot(rango, senal_1, 'indianred')
    mplot.subplot(414)
    mplot.title(title_4)
    mplot.xlabel('Tiempo [s]')
    mplot.ylabel('Amplitud [dB]')
    mplot.plot(rango, senal_4, 'yellow')
    mplot.plot(rango, senal_1, 'indianred')
    mplot.show()

def main():

    nombre = input('Ingrese el nombre del archivo .wav a trabajar: ')

    fs, senal, rango_senal, freqs, t = leer_audio(nombre)

    fftAudioOriginal = transformada(senal)
    ifftAudioOriginal = transformada_inversa(fftAudioOriginal)

    graficar_tiempo(rango_senal, senal, 'indianred', 'Grafico Amplitud vs. Tiempo del audio leído')
    graficar_frecuencia(rango_senal, fftAudioOriginal, freqs, 'indianred', 'Grafico FFT vs. Frecuencia de la transformada del audio leído')

    portadora_A08 = fx_portadora(15*fs, 0.8, rango_senal)
    portadora_A1  = fx_portadora(15*fs, 1.0, rango_senal)
    portadora_A12 = fx_portadora(15*fs, 1.2, rango_senal)

    multi_grafico_tiempo(rango_senal, senal, 'Amplitud vs Tiempo Original', portadora_A08, 'Amplitud vs Tiempo Portadora 80%', portadora_A1, 'Amplitud vs Tiempo Portadora 100%', portadora_A12, 'Amplitud vs Tiempo Portadora 120%')

    modulacion_A08 = modulacion_am(senal, portadora_A08)
    modulacion_A1 = modulacion_am(senal, portadora_A1)
    modulacion_A12 = modulacion_am(senal, portadora_A12)

    multi_grafico_tiempo(rango_senal, senal, 'Amplitud vs Tiempo Original', modulacion_A08, 'Amplitud vs Tiempo Modulación 80%', modulacion_A1, 'Amplitud vs Tiempo Modulación 100%', modulacion_A12, 'Amplitud vs Tiempo Modulación 120%')

    multi_grafico_comparativo(rango_senal, senal, 'Amplitud vs Tiempo Original', modulacion_A08, 'Amplitud vs Tiempo Modulación 80%', modulacion_A1, 'Amplitud vs Tiempo Modulación 100%', modulacion_A12, 'Amplitud vs Tiempo Modulación 120%')

    demodulacion = demodulacion_am(modulacion_A1, portadora_A1)

    graficar_tiempo(rango_senal, demodulacion, 'indianred', 'Grafico Amplitud vs. Tiempo de Demodulada AM')


    fft_lpf = filtro_paso_bajo(8*fs, demodulacion, 20000)

    graficar_tiempo(rango_senal, fft_lpf, 'indianred', 'Grafico Amplitud vs. Tiempo de Demodulada pasa bajo AM')

    scipy.io.wavfile.write('dem1.wav',fs, fft_lpf)

    ########################################################################################################################################################################################################################################################################

    ######################## Modulación FM #################################################################################################################################################################################################################################

    modulacion_F08 = modulacion_fm(senal, rango_senal, 25000, 44100, 0.8)
    modulacion_F1  = modulacion_fm(senal, rango_senal, 25000, 44100, 1.0)
    modulacion_F12 = modulacion_fm(senal, rango_senal, 25000, 44100, 1.2)

    multi_grafico_tiempo(rango_senal, senal, 'Amplitud vs Tiempo Original',
                         modulacion_F08, 'Amplitud vs Tiempo Modulación k = 80%', modulacion_F1, 'Amplitud vs Tiempo Modulación 100%',
                         modulacion_F12, 'Amplitud vs Tiempo Modulación 120%')


    return 0

main();
