import scipy as sc
import scipy.io.wavfile
from scipy.fftpack import fftfreq, ifftshift, fftshift
from scipy.signal import kaiserord, lfilter, firwin, freqz
import numpy as np
import matplotlib as mp
import matplotlib.pyplot as mplot
import math

# La función leer_audio se encarga de abrir el archivo a partir de una dirección pedida por pantalla.
# En ella se obtienen los datos del archivo .wav con la función read de Scipy. Se entrega el tiempo de
# muestreo, un arreglo de tiempos en los que se toman los datos, el rate del archivo y los datos leídos.
def leer_audio(nombre):
    fs, data = sc.io.wavfile.read(nombre)
    dimension = data[0].size

    if dimension == 1:
        senal = data
    else:
        senal = data[:, dimension - 1]

    timeStamp = 1.0/fs
    rango = senal.shape[0]
    x = rango / float(fs)
    tArray = scipy.arange(0, x, timeStamp)
    freqs = scipy.fftpack.fftfreq(senal.size, tArray[1]-tArray[0])
    fft_freqs = np.array(freqs)
    return fs, senal, tArray, fft_freqs

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

# Funcion que realiza el filtro paso bajo de una transformada de una señal, entra el ratio, la transformada y el valor de frecuencia de corte
# Retorna la señal filtrada.
def filtro_paso_bajo(rate, senal, corte):
    numtaps = 1001
    cutoff_frecuencia = corte
    nyquist_rate = rate/2
    fir_coeff = firwin(numtaps, cutoff_frecuencia/nyquist_rate)
    filtro = lfilter(fir_coeff, 1.0, senal)
    return filtro

# Funcion que realiza el filtro paso alto de una transformada de una señal, entra el ratio, la transformada y el valor de frecuencia de corte
# Retorna la señal filtrada.
def filtro_paso_alto(rate, senal, corte):
    numtaps = 1001
    cutoff_frecuencia = corte
    nyquist_rate = rate / 2
    fir_coeff = firwin(numtaps, cutoff_frecuencia/nyquist_rate, pass_zero = False)
    filtro = lfilter(fir_coeff, 1.0, senal)
    return filtro

# Funcion que realiza el filtro paso banda de una transformada de una señal, entra el ratio, la transformada y los valores de frecuencia de corte
# Retorna la señal filtrada.
def filtro_paso_banda(rate, senal, corte_bajo, corte_alto):
    numtaps = 1001
    cutoff_frecuencia_inf = corte_bajo
    cutoff_frecuencia_sup = corte_alto
    nyquist_rate = rate / 2
    fir_coeff = firwin(numtaps, [cutoff_frecuencia_inf/nyquist_rate, cutoff_frecuencia_sup/nyquist_rate], pass_zero = False)
    filtro = lfilter(fir_coeff, 1.0, senal)
    return filtro

# Funcion que realiza el filtro multi banda de una transformada de una señal, entra el ratio y la transformada
# Retorna la señal filtrada.
def filtro_multi_banda(rate, senal):
    numtaps = 1001
    nyquist_rate = rate / 2

    corte01 = 200
    corte02 = 1000
    corte03 = 4000
    corte04 = 6000
    corte05 = 8000
    corte06 = 8500
    corte07 = 10000
    corte08 = 10400
    corte09 = 12000
    corte10 = 12350
    corte11 = 18000
    corte12 = 18400

    fir_coeff = firwin(numtaps,[corte01/nyquist_rate,
                                corte02/nyquist_rate,
                                corte03/nyquist_rate,
                                corte04/nyquist_rate,
                                corte05/nyquist_rate,
                                corte06/nyquist_rate,
                                corte07/nyquist_rate,
                                corte08/nyquist_rate,
                                corte09/nyquist_rate,
                                corte10/nyquist_rate,
                                corte11/nyquist_rate,
                                corte12/nyquist_rate],
                                pass_zero = False)
    filtro = lfilter(fir_coeff, 1.0, senal)
    return filtro

# Las funciones graficar y graficarFFT se encargan de elaborar los graficos, difieren en los parametros, pero su
# comportamiento es el mismno, graficar entrega un grafico de la señal en el tiempo y graficarFFT entrega un
# grafico de la transformada de la señal en la frecuencia.
def graficar(tpo, senal, color, title):
    f, ax = mplot.subplots()
    ax.plot(tpo, senal.real, color)
    ax.set_title(title)
    ax.set_xlabel('Tiempo [s]')
    ax.set_ylabel('Amplitud [dB]')
    mplot.show()

def graficarFFT(freqs, senalFFT, color, title):
    f, ax = mplot.subplots()
    ax.set_title(title)
    ax.plot(freqs, abs(senalFFT), color)
    ax.set_xlabel('Frecuencia [Hz]')
    ax.set_ylabel('FFT')
    mplot.show()

# Funcion que se encarga de desarrollar el espectrograma de una transformada de fourier, recibe como entrada
# la trasnformada de una señal, su ratio y el titulo que se le pondra al espectrograma.
def espectrograma(senal, rate, title):
    NFFT = 1024
    fig = mplot.figure()
    cmap = mplot.get_cmap('jet')
    pxx, frequs, bins, im = mplot.specgram(senal.real, NFFT=NFFT, Fs=rate, cmap=cmap)
    mplot.ylabel('Frecuencia [Hz]')
    mplot.xlabel('Tiempo [seg]')
    mplot.title(title)
    fig.colorbar(im).set_label('Amplitud [dB]')
    mplot.show()

def main():

    nombre = input('Ingrese el nombre del archivo .wav a trabajar: ')

    fs, senal, arreglo, fft_freqs = leer_audio(nombre)

    fftAudioOriginal = transformada(senal)
    ifftAudioOriginal = transformada_inversa(fftAudioOriginal)

    # Se grafica la señal de acuerdo al tiempo.
    graficar(arreglo, senal, 'indianred', 'Grafico Amplitud vs. Tiempo del audio leído')
    # Se grafica la señal de acuerdo a la frecuencia.
    graficarFFT(fft_freqs, fftAudioOriginal, 'indianred', 'Grafico FFT vs. Frecuencia de la transformada del audio leído')
    # Se grafica el espectrograma de la señal original.
    espectrograma(senal, fs, 'Espectrograma del audio leído')

    valor_corte_paso_bajo = input('Ingrese el valor de frecuencia de corte para el filtro paso bajo en Hz (i.e. 2000): ')
    corte_paso_bajo = int(valor_corte_paso_bajo)
    fft_lpf = filtro_paso_bajo(fs, fftAudioOriginal, corte_paso_bajo)
    # Se grafica la señal de acuerdo a la frecuencia post filtro paso bajo.
    graficarFFT(fft_freqs, fft_lpf, 'y', 'Grafico FFT vs. Frecuencia de la transformada del audio leído con filtro paso bajo de ' + str(corte_paso_bajo) + 'Hz')
    ifft_lpf = transformada_inversa(fft_lpf)
    # Se grafica el espectrograma de la señal original filtrada por filtro paso bajo.
    espectrograma(ifft_lpf, fs, 'Espectrograma del audio leído con filtro paso bajo de ' + str(corte_paso_bajo) + 'Hz')
    # Se grafica el espectrograma de la fft de la señal original para comprobar la aplicación del corte.
    espectrograma(fft_lpf, fs, 'Espectrograma del audio leído en Frecuencia con filtro paso bajo de ' + str(corte_paso_bajo) + 'Hz')
    # Se grafica la señal filtrada con filtro paso bajo de acuerdo al tiempo.
    graficar(arreglo, ifft_lpf, 'indianred', 'Grafico Amplitud vs. Tiempo del audio leído filtrado paso bajo')
    # Se crea un audio a partir de la señal filtrada.
    sc.io.wavfile.write(nombre + '-LowPassFilter.wav', fs, ifft_lpf.real)

    valor_corte_paso_alto = input('Ingrese el valor de frecuencia de corte para el filtro paso alto en Hz (i.e. 7000): ')
    corte_paso_alto = int(valor_corte_paso_alto)
    fft_hpf = filtro_paso_alto(fs, fftAudioOriginal, corte_paso_alto)
    # Se grafica la señal de acuerdo a la frecuencia post filtro paso alto.
    graficarFFT(fft_freqs, fft_hpf, 'g', 'Grafico FFT vs. Frecuencia de la transformada del audio leído con filtro paso alto de ' + str(corte_paso_bajo) + 'Hz')
    ifft_hpf = transformada_inversa(fft_hpf)
    # Se grafica el espectrograma de la señal original filtrada por filtro paso alto.
    espectrograma(ifft_hpf, fs, 'Espectrograma del audio leído con filtro paso alto de ' + str(corte_paso_alto) + 'Hz')
    # Se grafica el espectrograma de la fft de la señal original para comprobar la aplicación del corte.
    espectrograma(fft_hpf, fs, 'Espectrograma del audio leído en Frecuencia con filtro paso alto de ' + str(corte_paso_alto) + 'Hz')
    # Se grafica la señal filtrada con filtro paso alto de acuerdo al tiempo.
    graficar(arreglo, ifft_hpf, 'indianred', 'Grafico Amplitud vs. Tiempo del audio leído filtrado paso alto')
    # Se crea un audio a partir de la señal filtrada.
    sc.io.wavfile.write(nombre + '-HighPassFilter.wav', fs, ifft_hpf.real)

    valor_banda_bajo = input('Ingrese el valor de frecuencia de corte baja para el filtro paso banda en Hz (i.e. 2000): ')
    banda_bajo = int(valor_banda_bajo)
    valor_banda_alto = input('Ingrese el valor de frecuencia de corte alta para el filtro paso banda en Hz (i.e. 5000): ')
    banda_alto = int(valor_banda_alto)
    fft_bpf = filtro_paso_banda(fs, fftAudioOriginal, banda_bajo, banda_alto)
    # Se grafica la señal de acuerdo a la frecuencia post filtro paso banda.
    graficarFFT(fft_freqs, fft_bpf, 'g', 'Grafico FFT vs. Frecuencia de la transformada del audio leído con filtro paso banda entre ' + str(banda_bajo) + 'Hz y ' + str(banda_alto) + 'Hz')
    ifft_bpf = transformada_inversa(fft_bpf)
    # Se grafica el espectrograma de la señal original filtrada por filtro paso banda.
    espectrograma(ifft_bpf, fs, 'Espectrograma del audio leído con filtro paso banda entre ' + str(banda_bajo) + 'Hz y ' + str(banda_alto) + 'Hz')
    # Se grafica el espectrograma de la fft de la señal original para comprobar la aplicación del corte.
    espectrograma(fft_bpf, fs, 'Espectrograma del audio leído en Frecuencia con filtro paso banda entre ' + str(banda_bajo) + 'Hz y ' + str(banda_alto) + 'Hz')
    # Se grafica la señal filtrada con filtro paso banda de acuerdo al tiempo.
    graficar(arreglo, ifft_bpf, 'indianred', 'Grafico Amplitud vs. Tiempo del audio leído filtrado paso banda')
    # Se crea un audio a partir de la señal filtrada.
    sc.io.wavfile.write(nombre + '-BandPassFilter.wav', fs, ifft_bpf.real)

    fft_mbf = filtro_multi_banda(fs, fftAudioOriginal)
    # Se grafica la señal de acuerdo a la frecuencia post filtro multi banda.
    graficarFFT(fft_freqs, fft_mbf, 'g', 'Grafico FFT vs. Frecuencia de la transformada del audio leído con filtro multi banda')
    ifft_mbf = transformada_inversa(fft_mbf)
    # Se grafica el espectrograma de la señal original filtrada por filtro multi banda.
    espectrograma(ifft_mbf, fs, 'Espectrograma del audio leído con filtro multi banda')
    # Se grafica el espectrograma de la fft de la señal original para comprobar la aplicación del corte.
    espectrograma(fft_mbf, fs, 'Espectrograma del audio leído en Frecuencia con filtro multi banda')
    # Se grafica la señal filtrada con filtro multi banda de acuerdo al tiempo.
    graficar(arreglo, ifft_mbf, 'indianred', 'Grafico Amplitud vs. Tiempo del audio leído filtrado multi banda')
    # Se crea un audio a partir de la señal filtrada.
    sc.io.wavfile.write(nombre + '-MultiBandFilter.wav', fs, ifft_mbf.real)

main();
