import scipy as sc
import scipy.io.wavfile

from scipy.fftpack import fftfreq
from scipy.signal import lfilter, firwin
import scipy.signal.signaltools as sigtool
from numpy import cos, pi, linspace
import matplotlib.pyplot as mplot

import scipy.misc
import numpy as np

from math import floor

from PIL import Image
import wave
import array
import struct

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
    # print("Largo de funcion portadora") ###########
    # print(len(portadora))           ###########
    return portadora

def interpolar_senal(rango_senal, senal, rango_portadora):
    f = sc.interpolate.interp1d(rango_senal, senal)
    senal_ip = f(rango_portadora)
    # print("Cantiad de datos de la nueva data")  ###########
    # print (len(senal_ip))                       ###########
    return senal_ip

def modulacion_am(senal, portadora):
    modulacion = portadora * senal
    return modulacion

def demodulacion_am(modulacion, portadora):
    #Demodular AM
    demodulacion = (modulacion/portadora)/40000
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

def conversion_binaria(senal, formato):
    resultado = []
    for i in senal:
        bin_array = formato.format(i)
        for bit in bin_array:
            resultado.append(int(bit))
    return resultado

def deconversion_binaria(bin_data, n_bits):
    data = []
    exp = n_bits - 1
    dec_value = 0
    for i in bin_data:
        dec_value += (i * (2 ** exp))
        if exp > 0:
            exp -= 1
        else:
            data.append(dec_value)
            dec_value = 0
            exp = n_bits - 1
    return data

def generador_ruido(senal, A):
    ruido = (np.random.randn(len(senal))+1)*A
    snr = 10*np.log10(np.mean(np.square(senal)) / np.mean(np.square(ruido)))
    # print("SNR = %fdB" % snr)
    senal_ruidosa = np.add(senal,ruido)
    return senal_ruidosa

# Entradas: - la señal
#           - la frecuencia de corte y el periodo de la señal
#           - la amplitud A para señal 0 y B para señal 1
#           - la frecuencia fs de muestreo
# Salida:   - el arreglo tiempo y el arreglo de la señal modificada
# Entradas: - la señal
#           - la frecuencia de corte y el periodo de la señal
#           - la amplitud A para señal 0 y B para señal 1
#           - la frecuencia fs de muestreo
# Salida:   - el arreglo tiempo y el arreglo de la señal modificada
def modulacion_digital_ask(senal, fc, Tb, A, B, fs):
    resultado = []
    t = np.linspace(0, Tb, fs * Tb)

    C0 = A * cos(2 * pi * fc * t)
    C1 = B * cos(2 * pi * fc * t)

    for b in senal:
        if b:
            resultado.extend(C1)
        else:
            resultado.extend(C0)

    tiempo = np.linspace(0, Tb * len(senal), len(resultado))
    return tiempo, resultado


# Entradas: - la señal
#           - las frecuencias de corte para cada señal y el periodo de la señal
#           - la amplitud A
#           - la frecuencia fs de muestreo
# Salida:   - el arreglo tiempo y el arreglo de la señal modificada
def modulacion_digital_fsk(senal, fc1, fc2, Tb, amplitud, fs):
    resultado = []

    cantMuestras = round(fs * Tb)

    t = np.linspace(0, Tb, cantMuestras)

    C0 = amplitud * cos(2 * pi * fc1 * t)
    C1 = amplitud * cos(2 * pi * fc2 * t)

    for b in senal:
        if b:
            resultado.extend(C1)
        else:
            resultado.extend(C0)

    tiempo = np.linspace(0, Tb * len(senal), len(resultado))
    return tiempo, resultado

def demodulacion_digital_ask(senal, fc, fs, Tt, Tb):
    t = np.linspace(0, Tb, fs * Tb)
    C0 = cos(2 * pi * fc * t)

    senal_correl = np.correlate(senal, C0)

    y_diff = np.diff(senal_correl)

    y_env = np.abs(sigtool.hilbert(y_diff))
    h = firwin(numtaps=100, cutoff=0.4 * fs, nyq=fs)
    senal_filtrada = lfilter(h, 1.0, y_env)

    t = np.linspace(0, Tt, len(senal_filtrada))

    # graficar_tiempo(np.linspace(0, Tt, len(senal)), senal, 'indianred', 'Señal ASK original')
    # graficar_tiempo(t, senal_filtrada, 'indianred', 'Señal ASK filtrada')

    largo_final = len(senal_filtrada)
    largo_fragmento = floor(largo_final / (Tt / Tb))

    mean = np.mean(senal_filtrada)
    msg_binario = []

    sampled_signal = senal_filtrada[floor(largo_fragmento * 0.5):largo_final:floor(largo_fragmento)]
    for bit in sampled_signal:
        if bit > mean * 0.9:
            msg_binario.append(1)
        else:
            msg_binario.append(0)

    # print(msg_binario)
    return msg_binario

# Entradas: - la señal
#           - las frecuencias de corte para cada señal y el periodo de la señal
#           - la amplitud A
#           - la frecuencia fs de muestreo
# Salida:   - el arreglo tiempo y el arreglo de la señal modificada
def demodulacion_digital_fsk(senal, fc1, fc2, Tb, fs, filtro = False):
    # Creando señales portadoras conocidas
    cantMuestras = round(fs * Tb)
    aproxCantBits = round(len(senal)/cantMuestras)
    t = np.linspace(0, Tb, cantMuestras)

    C0 = cos(2 * pi * fc1 * t)
    C1 = cos(2 * pi * fc2 * t)

    # graficar_tiempo(np.linspace(0, Tb * aproxCantBits, len(senal)), senal, 'indianred', 'Señal FSK original')
    # print("correl c0")
    # Correlacionando datos
    # print("1/4")
    msg_0 = np.correlate(senal, C0)
    # graficar_tiempo(np.linspace(0, Tb * aproxCantBits, len(msg_0)), msg_0, 'indianred', 'Gráfica detección de ceros sin filtrar')
    # print("2/4")
    y_env_0 = np.abs(sigtool.hilbert(msg_0))

    if filtro == True:
        # print("3/4")
        h_0 = firwin(numtaps=100, cutoff=0.4 * fs, nyq=fs)
        # print("4/4")
        senal_filtrada_0 = lfilter(h_0, 1.0, y_env_0)
    else:
        senal_filtrada_0 = y_env_0

    # print(len(senal_filtrada_0))
    # print("correl c1")
    # print("1/4")
    msg_1 = np.correlate(senal, C1)
    # print("2/4")
    y_env_1 = np.abs(sigtool.hilbert(msg_1))

    if filtro == True:
        # print("3/4")
        h_1 = firwin(numtaps=100, cutoff=0.4 * fs, nyq=fs)
        # print("4/4")
        senal_filtrada_1 = lfilter(h_1, 1.0, y_env_1)
    else:
        senal_filtrada_1 = y_env_1

    # print("graficas")

    # graficar_tiempo(np.linspace(0, Tb * aproxCantBits, len(senal)), senal, 'indianred', 'Señal FSK original')
    # graficar_tiempo(np.linspace(0, Tb * aproxCantBits, len(msg_0)), msg_0, 'indianred', 'Gráfica detección de ceros sin filtrar')
    # graficar_tiempo(np.linspace(0, Tb * aproxCantBits, len(msg_1)), msg_1, 'indianred', 'Gráfica detección de unos sin filtrar')

    # graficar_tiempo(np.linspace(0, Tb * aproxCantBits, len(y_env_0)), y_env_0, 'indianred', 'Gráfica detección de ceros filtrada')
    # graficar_tiempo(np.linspace(0, Tb * aproxCantBits, len(y_env_1)), y_env_1, 'indianred', 'Gráfica detección de unos filtrada')

    # graficar_tiempo(np.linspace(0, Tb * aproxCantBits, len(senal_filtrada_0)), senal_filtrada_0, 'indianred', 'Gráfica detección de ceros filtrada')
    # graficar_tiempo(np.linspace(0, Tb * aproxCantBits, len(senal_filtrada_1)), senal_filtrada_1, 'indianred', 'Gráfica detección de unos filtrada')

    # print(len(senal_filtrada_1))
    # print("resta")
    senal_filtrada_final = np.subtract(senal_filtrada_1,senal_filtrada_0)

    #graficar_tiempo(np.linspace(0, Tb * aproxCantBits, len(senal_filtrada_final)), senal_filtrada_final, 'indianred', 'Señal FSK filtrada')

    largo_final = len(senal_filtrada_final)
    largo_fragmento = cantMuestras * (len(senal_filtrada_final) / len(senal))
    # print(cantMuestras)
    # print(len(senal_filtrada_final))
    # print(len(senal))
    # print(len(senal_filtrada_final) / len(senal))

    msg_binario = []

    # Divisor mejorado
    #
    seccionBorde = largo_fragmento * 0.20
    posActual = seccionBorde
    #largo_fragmento *= 1

    # print("divisor")
    # print(posActual)
    # print(round(posActual))
    # print(largo_fragmento)
    #print(senal_filtrada_final[0:int(largo_fragmento * 5)])

    while posActual < largo_final:
        bit = senal_filtrada_final[int(round(posActual))]
        if bit > 0:
            msg_binario.append(1)
        else:
            msg_binario.append(0)

        # ubicacion siguiente posicion mejorada
        aux = posActual
        posEncontrada = False

        #print('pos actual = {:f} pos sig = {:f} '.format(posActual, posActual + largo_fragmento))
        # Si hay un cambio de bit recorregir divisor
        while (aux < (posActual + largo_fragmento)) & ((int(round(aux))-1) < len(senal_filtrada_final)) & (posEncontrada is False):
            auxAnterior = senal_filtrada_final[int(round(aux))-2]
            auxActual = senal_filtrada_final[int(round(aux))-1]
            #print('aux actual = {:f} {:f} {:f}'.format(aux, auxAnterior,auxActual))
            if ((auxAnterior < 0) & (auxActual > 0)) | ((auxAnterior > 0) & (auxActual < 0)):
                #print("cambio" + str(aux))
                posActual = aux + (largo_fragmento * 0.5)
                posEncontrada = True
            aux += 1
        if posEncontrada is False:
            #print('aux actual = {:f} '.format(aux))
            posActual += largo_fragmento
        #print(posActual)

    # print(len(senal_filtrada_final))
    # print(seccionBorde)
    # print(posActual)
    if ((posActual-largo_fragmento+seccionBorde) < len(senal_filtrada_final)) & (senal_filtrada_final[int(round(len(senal_filtrada_final)-seccionBorde))] > 0):
        msg_binario.append(1)
    elif ((posActual-largo_fragmento+seccionBorde) < len(senal_filtrada_final)) & (senal_filtrada_final[int(round(len(senal_filtrada_final)-seccionBorde))] < 0):
        msg_binario.append(0)

    #print(msg_binario)
    return msg_binario

# Entradas: - la señal
#           - El tiempo de la subseñal y el tiempo total
#           - la frecuencia de muestreo
# Salida:   - el arreglo tiempo y el arreglo de la señal modificada
def demodulacion_digital_fsk_2(senal, Tb, Tt, fs):
    y_diff = np.diff(senal, 1)

    y_env = np.abs(sigtool.hilbert(y_diff))
    h = firwin(numtaps=100, cutoff= 0.4 * fs, nyq=fs)
    senal_filtrada = lfilter(h, 1.0, y_env)

    t = np.linspace(0, Tt, len(senal_filtrada))

    graficar_tiempo(np.linspace(0, Tt, len(senal)), senal, 'indianred', 'señal inicial')
    graficar_tiempo(t, senal_filtrada, 'indianred', 'señal demodulada')

    largo_final = len(senal_filtrada)
    largo_fragmento = floor(largo_final / (Tt / Tb))

    mean = np.mean(senal_filtrada)
    msg_binario = []
    sampled_signal = senal_filtrada[floor(largo_fragmento / 2)-1:largo_final:floor(largo_fragmento)-1]
    for bit in sampled_signal:
        if bit > mean:
            msg_binario.append(1)
        else:
            msg_binario.append(0)

    # print(msg_binario)
    return msg_binario

def convertirBMPWAV(imagen, audio):


    wav = wave.open(audio, 'wb')

    raw = array.array('B')

    bmp = open(imagen, 'rb')

    i = 0

    while i < 122:
        extra = struct.unpack('B', bmp.read(1))
        # print(extra[0])
        raw.append(extra[0])
        i += 1
    bmp.close()

    img = Image.open(imagen)
    for r, g, b in img.getdata():
        raw.append(r)
        raw.append(g)
        raw.append(b)
        i += 1
        # print("%i" % r, "%i" % g, "%i" % b)
    # img.close()
    wav.setnchannels(1)

    wav.setsampwidth(1)

    wav.setframerate(44100)

    wav.writeframes(raw)

    # print("frames: %i" % i)
    # print("size: %i" % len(raw))

    wav.close()


def colocarFlags(senal, flag):
    resultado = []
    resultado.extend(flag)
    resultado.extend(senal)
    resultado.extend(flag)
    return resultado

def sacarFlags(senal, binary_flag):
    limits = []
    for x in range(len(senal)):
        if senal[x:x+len(binary_flag)] == binary_flag:
            limits.append(x)

    return senal[(limits[0]+len(binary_flag)):limits[1]]

def convertirWAVBMP(audio):
    #wav = wave.open(audio, "rb")

    raw = array.array('B')

    full_image = np.array([[[]]], dtype=int)

    #frames = wav.getnframes()
    #pix = int((int(frames) - 122))

    ancho = 0
    alto = 0


    for i in range(0, 122):
        extra = audio[i]

        if i == 18:
            ancho = extra
        elif i == 19:
            ancho += (extra * 256)
        elif i == 20:
            ancho += (extra * 256 * 256)
        elif i == 21:
            ancho += (extra * 256 * 256 * 256)
        elif i == 22:
            alto = extra
        elif i == 23:
            alto += (extra * 256)
        elif i == 24:
            alto += (extra * 256 * 256)
        elif i == 25:
            alto += (extra * 256 * 256 * 256)


    c_linea = 0
    c_pixel = 0
    flag = 0

    linea = np.array([[[]]], dtype=int)
    pixel = np.array([[[]]], dtype=int)

    for i in range(122, len(audio)):
        extra = audio[i]
        # print(extra)
        if c_pixel == 0:
            # print(extra , i)
            pixel = np.array([[[extra]]])
            c_pixel += 1
        elif c_pixel == 1:
            pixel = np.append(pixel, [[[extra]]], 2)  # append en 2: dentro del array o cuando es el primer valor, append en 1: al lado del array
            c_pixel += 1
        elif c_pixel == 2:
            pixel = np.append(pixel, [[[extra]]], 2)
            c_pixel = 0
            # pixel completo, añado a la horizontal
            if c_linea == 0:  # primer pixel en línea
                linea = pixel
            else:  # píxeles después del primero van en paralelo a este
                linea = np.append(linea, pixel, 0)
            pixel = np.array([[]], dtype=int)
            c_linea += 1
            if c_linea == ancho:  # linea completada
                c_linea = 0
                if flag == 0:
                    full_image = linea  # np.append(full_image, linea, 1)
                    flag = 1
                else:
                    full_image = np.append(full_image, linea, 1)
                linea = np.array([[]], dtype=int)

    full_image = full_image.astype('uint8')
    print('Size total:', len(full_image))

    print(full_image.dtype)
    imagen_final = Image.fromarray(full_image, 'RGB')

    imagen_final = imagen_final.transpose(Image.ROTATE_270)
    imagen_final = imagen_final.transpose(Image.FLIP_LEFT_RIGHT)
    imagen_final.save('output.BMP')
    return 0

def emisor():
    n_bits = 9
    formato_bin = '{:09b}'

    nombreImagen = "mario.bmp"
    nombreAudio = "salidamario.wav"

    convertirBMPWAV(nombreImagen, nombreAudio)

    fs, array_prueba, rango_senal, freqs, t = leer_audio(nombreAudio)

    # flag en binario = 111100001 111000011 110000111 100001111
    flag = [481, 451, 391, 271]

    array_prueba_flag = colocarFlags(array_prueba, flag)
    print('largo sin = {:f} largo con = {:f}'.format(len(array_prueba), len(array_prueba_flag)))
    array_prueba_bin = conversion_binaria(array_prueba_flag, formato_bin)  # array_prueba_flag
    print('n bits = {:f} 8 * len = {:f}'.format(len(array_prueba_bin), 9 * len(array_prueba_flag)))

    fc = 4000
    fc2 = 8000
    Tb = 0.001  # s
    amplitud = 1
    fs = 70000

    tprueba2, array_prueba_fsk = modulacion_digital_fsk(array_prueba_bin, fc, fc2, Tb, amplitud, fs)

    scipy.io.wavfile.write('mario_fsk.wav', fs, np.array(array_prueba_fsk))

def receptor():

    n_bits = 9
    formato_bin = '{:09b}'

    fc = 4000
    fc2 = 8000
    Tb = 0.001  # s
    amplitud = 1
    fs = 70000

    # flag en binario = 111100001 111000011 110000111 100001111
    flag = [481, 451, 391, 271]

    fs, array_prueba_fsk, rango_senal, freqs, t = leer_audio('mario_fsk.wav')


    array_prueba_demod = demodulacion_digital_fsk(np.array(array_prueba_fsk), fc, fc2, Tb, fs)

    array_prueba_deflag = sacarFlags(array_prueba_demod, conversion_binaria(flag, formato_bin))
    array_final = deconversion_binaria(array_prueba_deflag, n_bits)

    convertirWAVBMP(array_final)

def main():
    # emisor()
    # receptor()
    # exit()

    n_bits = 9
    formato_bin = '{:09b}'

    nombreImagen = "mario.bmp"
    nombreAudio = "salidamario.wav"

    convertirBMPWAV(nombreImagen, nombreAudio)

    fs, array_prueba, rango_senal, freqs, t = leer_audio(nombreAudio)

    # flag en binario = 111100001 111000011 110000111 100001111
    flag = [481, 451, 391, 271]

    array_prueba_flag = colocarFlags(array_prueba, flag)
    print('largo sin = {:f} largo con = {:f}'.format(len(array_prueba), len(array_prueba_flag)))
    array_prueba_bin = conversion_binaria(array_prueba_flag, formato_bin)  #array_prueba_flag
    print('n bits = {:f} 8 * len = {:f}'.format(len(array_prueba_bin), 9 * len(array_prueba_flag)))



    fc = 4000
    fc2 = 8000
    Tb = 0.001  # s
    amplitud = 1
    fs = 70000

    tprueba2, array_prueba_fsk = modulacion_digital_fsk(array_prueba_bin, fc, fc2, Tb, amplitud, fs)

    scipy.io.wavfile.write('mario_fsk.wav', fs, np.array(array_prueba_fsk))

    array_prueba_demod = demodulacion_digital_fsk(np.array(array_prueba_fsk), fc, fc2, Tb, fs)
    # print(array_prueba_demod)
    # array_prueba_debin

    len(array_prueba_bin)
    len(array_prueba_demod)
    print(array_prueba_bin)
    print(array_prueba_demod)

    array_prueba_deflag = sacarFlags(array_prueba_demod, conversion_binaria(flag, formato_bin))
    array_final = deconversion_binaria(array_prueba_deflag, n_bits)

    # print(array_final)

    len(array_prueba)
    len(array_final)
    print(array_prueba)
    print(array_final)

    print("prueba error")
    print(np.sum(np.absolute(np.array(array_prueba_bin) - np.array(array_prueba_demod))))

    print(np.sum(np.absolute(np.array(array_prueba) - np.array(array_final))))

    convertirWAVBMP(array_final)

    return 0

main();
