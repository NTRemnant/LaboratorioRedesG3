import scipy as sc
import scipy.io.wavfile
import wave
from scipy.fftpack import fftfreq, ifftshift, fftshift
from scipy.signal import kaiserord, lfilter, firwin, freqz
import scipy.signal.signaltools as sigtool
import scipy.integrate as intgrl
import numpy as np
from numpy import cos, pi, sin, linspace
import matplotlib as mp
import matplotlib.pyplot as mplot

from math import floor


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

def modulacion_digital_16_fsk(senal, Tb, amplitud, fs):

    resultado = []
    t = np.linspace(0, Tb, fs * Tb)

    C_0000 = amplitud * cos(2 * pi * 100 * t)
    C_0001 = amplitud * cos(2 * pi * 500 * t)
    C_0010 = amplitud * cos(2 * pi * 1000 * t)
    C_0011 = amplitud * cos(2 * pi * 1500 * t)
    C_0100 = amplitud * cos(2 * pi * 2000 * t)
    C_0101 = amplitud * cos(2 * pi * 2500 * t)
    C_0110 = amplitud * cos(2 * pi * 3000 * t)
    C_0111 = amplitud * cos(2 * pi * 3500 * t)
    C_1000 = amplitud * cos(2 * pi * 4000 * t)
    C_1001 = amplitud * cos(2 * pi * 4500 * t)
    C_1010 = amplitud * cos(2 * pi * 5000 * t)
    C_1011 = amplitud * cos(2 * pi * 5500 * t)
    C_1100 = amplitud * cos(2 * pi * 6000 * t)
    C_1101 = amplitud * cos(2 * pi * 6500 * t)
    C_1110 = amplitud * cos(2 * pi * 7000 * t)
    C_1111 = amplitud * cos(2 * pi * 7500 * t)

    for b in range(0, len(senal)-3, 4):
        if senal[b] == 0 and senal[b+1] == 0 and senal[b+2] == 0 and senal[b+3] == 0:
            resultado.extend(C_0000)

        if senal[b] == 0 and senal[b+1] == 0 and senal[b+2] == 0 and senal[b+3] == 1:
            resultado.extend(C_0001)

        if senal[b] == 0 and senal[b+1] == 0 and senal[b+2] == 1 and senal[b+3] == 0:
            resultado.extend(C_0010)

        if senal[b] == 0 and senal[b+1] == 0 and senal[b+2] == 1 and senal[b+3] == 1:
            resultado.extend(C_0011)

        if senal[b] == 0 and senal[b+1] == 1 and senal[b+2] == 0 and senal[b+3] == 0:
            resultado.extend(C_0100)

        if senal[b] == 0 and senal[b+1] == 1 and senal[b+2] == 0 and senal[b+3] == 1:
            resultado.extend(C_0101)

        if senal[b] == 0 and senal[b+1] == 1 and senal[b+2] == 1 and senal[b+3] == 0:
            resultado.extend(C_0110)

        if senal[b] == 0 and senal[b+1] == 1 and senal[b+2] == 1 and senal[b+3] == 1:
            resultado.extend(C_0111)

        if senal[b] == 1 and senal[b+1] == 0 and senal[b+2] == 0 and senal[b+3] == 0:
            resultado.extend(C_1000)

        if senal[b] == 1 and senal[b+1] == 0 and senal[b+2] == 0 and senal[b+3] == 1:
            resultado.extend(C_1001)

        if senal[b] == 1 and senal[b+1] == 0 and senal[b+2] == 1 and senal[b+3] == 0:
            resultado.extend(C_1010)

        if senal[b] == 1 and senal[b+1] == 0 and senal[b+2] == 1 and senal[b+3] == 1:
            resultado.extend(C_1011)

        if senal[b] == 1 and senal[b+1] == 1 and senal[b+2] == 0 and senal[b+3] == 0:
            resultado.extend(C_1100)

        if senal[b] == 1 and senal[b+1] == 1 and senal[b+2] == 0 and senal[b+3] == 1:
            resultado.extend(C_1101)

        if senal[b] == 1 and senal[b+1] == 1 and senal[b+2] == 1 and senal[b+3] == 0:
            resultado.extend(C_1110)

        if senal[b] == 1 and senal[b+1] == 1 and senal[b+2] == 1 and senal[b+3] == 1:
            resultado.extend(C_1111)

    tiempo = np.linspace(0, Tb * len(senal), len(resultado))
    return tiempo, resultado

def graficar_tiempo(rango_senal, senal, color, title):
    mplot.title(title)
    mplot.xlabel('Tiempo [s]')
    mplot.ylabel('Amplitud [dB]')
    mplot.plot(rango_senal, senal, color)
    mplot.show()

def generador_ruido(senal, A):
    ruido = (np.random.randn(len(senal))+1)*A
    snr = 10*np.log10(np.mean(np.square(senal)) / np.mean(np.square(ruido)))
    print("SNR = %fdB" % snr)
    senal_ruidosa = np.add(senal,ruido)
    return senal_ruidosa

'''
def demodulacion_digital_16_fsk(senal, tiempo, amplitud, Tb, Tt, fs):
    # Creando señales portadoras conocidas
    t = np.linspace(0, Tb, fs)

    C_0000 = amplitud * cos(2 * pi * 100 * t)
    C_0001 = amplitud * cos(2 * pi * 500 * t)
    C_0010 = amplitud * cos(2 * pi * 1000 * t)
    C_0011 = amplitud * cos(2 * pi * 1500 * t)
    C_0100 = amplitud * cos(2 * pi * 2000 * t)
    C_0101 = amplitud * cos(2 * pi * 2500 * t)
    C_0110 = amplitud * cos(2 * pi * 3000 * t)
    C_0111 = amplitud * cos(2 * pi * 3500 * t)
    C_1000 = amplitud * cos(2 * pi * 4000 * t)
    C_1001 = amplitud * cos(2 * pi * 4500 * t)
    C_1010 = amplitud * cos(2 * pi * 5000 * t)
    C_1011 = amplitud * cos(2 * pi * 5500 * t)
    C_1100 = amplitud * cos(2 * pi * 6000 * t)
    C_1101 = amplitud * cos(2 * pi * 6500 * t)
    C_1110 = amplitud * cos(2 * pi * 7000 * t)
    C_1111 = amplitud * cos(2 * pi * 7500 * t)

    # Correlacionando datos
    msg_0000 = np.correlate(senal, C_0000)
    y_env_0000 = np.abs(sigtool.hilbert(msg_0000))
    h_0000 = firwin(numtaps=100, cutoff=0.4 * fs, nyq=fs)
    senal_filtrada_0000 = lfilter(h_0000, 1.0, y_env_0000)

    msg_0001 = np.correlate(senal, C_0001)
    y_env_0001 = np.abs(sigtool.hilbert(msg_0001))
    h_0001 = firwin(numtaps=100, cutoff=0.4 * fs, nyq=fs)
    senal_filtrada_0001 = lfilter(h_0001, 1.0, y_env_0001)

    msg_0010 = np.correlate(senal, C_0010)
    y_env_0010 = np.abs(sigtool.hilbert(msg_0010))
    h_0010 = firwin(numtaps=100, cutoff=0.4 * fs, nyq=fs)
    senal_filtrada_0010 = lfilter(h_0010, 1.0, y_env_0010)

    msg_0011 = np.correlate(senal, C_0011)
    y_env_0011 = np.abs(sigtool.hilbert(msg_0011))
    h_0011 = firwin(numtaps=100, cutoff=0.4 * fs, nyq=fs)
    senal_filtrada_0011 = lfilter(h_0011, 1.0, y_env_0011)

    msg_0100 = np.correlate(senal, C_0100)
    y_env_0100 = np.abs(sigtool.hilbert(msg_0100))
    h_0100 = firwin(numtaps=100, cutoff=0.4 * fs, nyq=fs)
    senal_filtrada_0100 = lfilter(h_0100, 1.0, y_env_0100)

    msg_0101 = np.correlate(senal, C_0101)
    y_env_0101 = np.abs(sigtool.hilbert(msg_0101))
    h_0101 = firwin(numtaps=100, cutoff=0.4 * fs, nyq=fs)
    senal_filtrada_0101 = lfilter(h_0101, 1.0, y_env_0101)

    msg_0110 = np.correlate(senal, C_0110)
    y_env_0110 = np.abs(sigtool.hilbert(msg_0110))
    h_0110 = firwin(numtaps=100, cutoff=0.4 * fs, nyq=fs)
    senal_filtrada_0110 = lfilter(h_0110, 1.0, y_env_0110)

    msg_0111 = np.correlate(senal, C_0111)
    y_env_0111 = np.abs(sigtool.hilbert(msg_0111))
    h_0111 = firwin(numtaps=100, cutoff=0.4 * fs, nyq=fs)
    senal_filtrada_0111 = lfilter(h_0111, 1.0, y_env_0111)

    msg_1000 = np.correlate(senal, C_1000)
    y_env_1000 = np.abs(sigtool.hilbert(msg_1000))
    h_1000 = firwin(numtaps=100, cutoff=0.4 * fs, nyq=fs)
    senal_filtrada_1000 = lfilter(h_1000, 1.0, y_env_1000)

    msg_1001 = np.correlate(senal, C_1001)
    y_env_1001 = np.abs(sigtool.hilbert(msg_1001))
    h_1001 = firwin(numtaps=100, cutoff=0.4 * fs, nyq=fs)
    senal_filtrada_1001 = lfilter(h_1001, 1.0, y_env_1001)

    msg_1010 = np.correlate(senal, C_1010)
    y_env_1010 = np.abs(sigtool.hilbert(msg_1010))
    h_1010 = firwin(numtaps=100, cutoff=0.4 * fs, nyq=fs)
    senal_filtrada_1010 = lfilter(h_1010, 1.0, y_env_1010)

    msg_1011 = np.correlate(senal, C_1011)
    y_env_1011 = np.abs(sigtool.hilbert(msg_1011))
    h_1011 = firwin(numtaps=100, cutoff=0.4 * fs, nyq=fs)
    senal_filtrada_1011 = lfilter(h_0011, 1.0, y_env_1011)

    msg_1100 = np.correlate(senal, C_1100)
    y_env_1100 = np.abs(sigtool.hilbert(msg_1100))
    h_1100 = firwin(numtaps=100, cutoff=0.4 * fs, nyq=fs)
    senal_filtrada_1100 = lfilter(h_1100, 1.0, y_env_1100)

    msg_1101 = np.correlate(senal, C_1101)
    y_env_1101 = np.abs(sigtool.hilbert(msg_1101))
    h_1101 = firwin(numtaps=100, cutoff=0.4 * fs, nyq=fs)
    senal_filtrada_1101 = lfilter(h_1101, 1.0, y_env_1101)

    msg_1110 = np.correlate(senal, C_1110)
    y_env_1110 = np.abs(sigtool.hilbert(msg_1110))
    h_1110 = firwin(numtaps=100, cutoff=0.4 * fs, nyq=fs)
    senal_filtrada_1110 = lfilter(h_1110, 1.0, y_env_1110)

    msg_1111 = np.correlate(senal, C_1111)
    y_env_1111 = np.abs(sigtool.hilbert(msg_1111))
    h_1111 = firwin(numtaps=100, cutoff=0.4 * fs, nyq=fs)
    senal_filtrada_1111 = lfilter(h_1111, 1.0, y_env_1111)

    tiempo = np.linspace(0, Tt, len(msg_0000))

    graficar_tiempo(np.linspace(0, Tt, len(senal)), senal, 'indianred', 'origi')

    graficar_tiempo(tiempo, msg_0000, 'indianred', '0000 sin filtro')
    graficar_tiempo(tiempo, msg_0001, 'indianred', '0001 sin filtro')
    graficar_tiempo(tiempo, msg_0010, 'indianred', '0010 sin filtro')
    graficar_tiempo(tiempo, msg_0011, 'indianred', '0011 sin filtro')
    graficar_tiempo(tiempo, msg_0100, 'indianred', '0100 sin filtro')
    graficar_tiempo(tiempo, msg_0101, 'indianred', '0101 sin filtro')
    graficar_tiempo(tiempo, msg_0110, 'indianred', '0110 sin filtro')
    graficar_tiempo(tiempo, msg_0111, 'indianred', '0111 sin filtro')
    graficar_tiempo(tiempo, msg_1000, 'indianred', '1000 sin filtro')
    graficar_tiempo(tiempo, msg_1001, 'indianred', '1001 sin filtro')
    graficar_tiempo(tiempo, msg_1010, 'indianred', '1010 sin filtro')
    graficar_tiempo(tiempo, msg_1011, 'indianred', '1011 sin filtro')
    graficar_tiempo(tiempo, msg_1100, 'indianred', '1100 sin filtro')
    graficar_tiempo(tiempo, msg_1101, 'indianred', '1101 sin filtro')
    graficar_tiempo(tiempo, msg_1110, 'indianred', '1110 sin filtro')
    graficar_tiempo(tiempo, msg_1111, 'indianred', '1111 sin filtro')

    graficar_tiempo(tiempo, senal_filtrada_0000, 'indianred', 'ceros con filtro')
    graficar_tiempo(tiempo, senal_filtrada_0001, 'indianred', 'unos con filtro')
    graficar_tiempo(tiempo, senal_filtrada_0010, 'indianred', 'ceros con filtro')
    graficar_tiempo(tiempo, senal_filtrada_0011, 'indianred', 'unos con filtro')
    graficar_tiempo(tiempo, senal_filtrada_0100, 'indianred', 'ceros con filtro')
    graficar_tiempo(tiempo, senal_filtrada_0101, 'indianred', 'unos con filtro')
    graficar_tiempo(tiempo, senal_filtrada_0110, 'indianred', 'ceros con filtro')
    graficar_tiempo(tiempo, senal_filtrada_0111, 'indianred', 'unos con filtro')
    graficar_tiempo(tiempo, senal_filtrada_1000, 'indianred', 'ceros con filtro')
    graficar_tiempo(tiempo, senal_filtrada_1001, 'indianred', 'unos con filtro')
    graficar_tiempo(tiempo, senal_filtrada_1010, 'indianred', 'ceros con filtro')
    graficar_tiempo(tiempo, senal_filtrada_1011, 'indianred', 'unos con filtro')
    graficar_tiempo(tiempo, senal_filtrada_1100, 'indianred', 'ceros con filtro')
    graficar_tiempo(tiempo, senal_filtrada_1101, 'indianred', 'unos con filtro')
    graficar_tiempo(tiempo, senal_filtrada_1110, 'indianred', 'ceros con filtro')
    graficar_tiempo(tiempo, senal_filtrada_1111, 'indianred', 'unos con filtro')

    senal_filtrada_final = np.subtract(senal_filtrada_1,senal_filtrada_0)
    graficar_tiempo(tiempo, senal_filtrada_final, 'indianred', 'resta')

    largo_final = len(senal_filtrada_final)
    largo_fragmento = floor(largo_final / (Tt/Tb))

    mean = np.mean(senal_filtrada_final)
    msg_binario = []
    sampled_signal = senal_filtrada_final[floor(largo_fragmento / 2):largo_final:floor(largo_fragmento)]
    for bit in sampled_signal:
        if bit > mean/4:
            msg_binario.append(1)
        else:
            msg_binario.append(0)

    print(msg_binario)
    return msg_binario
'''

def main():

    array_prueba = (0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0)

    amplitud = 0.8
    Tb = 0.1
    fs = 32000

    tprueba, prueba = modulacion_digital_16_fsk(array_prueba, Tb, amplitud, fs)
    graficar_tiempo(tprueba, prueba, 'indianred', 'mod 16-fsk normal')
    prueba = generador_ruido(prueba, 0.1)
    graficar_tiempo(tprueba, prueba, 'indianred', 'mod ask ruidosa')

    return 0

main();
