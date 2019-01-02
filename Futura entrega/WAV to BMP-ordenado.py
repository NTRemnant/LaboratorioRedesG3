from PIL import Image
from matplotlib import pyplot as plt
import scipy.misc
import numpy as np
import wave
import array
import sys
import math
import binascii



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
        extra = audio(i)
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

    full_image = full_image.astype('uint8'))
    print('Size total:', len(full_image))

    print(full_image.dtype)
    imagen_final = Image.fromarray(full_image, 'RGB')

    imagen_final = imagen_final.transpose(Image.ROTATE_270)
    imagen_final = imagen_final.transpose(Image.FLIP_LEFT_RIGHT)
    imagen_final.save('output.BMP')
    return 0