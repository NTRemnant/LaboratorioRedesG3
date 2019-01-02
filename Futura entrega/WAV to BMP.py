from PIL import Image
from matplotlib import pyplot as plt
import scipy.misc
import numpy as np
import wave
import array
import sys
import math
import binascii
# import scipy.misc


#img = Image.open(sys.argv[1])


#full_image=full_image.astype('uint8')


print(wav.getnchannels())

print(wav.getsampwidth())

print(wav.getframerate())

frames = wav.getnframes()
print("frames: %i" % frames)
pix = int((int(frames)-122))
print("pixeles x 3: %s" % pix)
print("píxeles reales: %i" % (pix//3))

#raw = []

ancho = 0
alto = 0

#header
for i in range(0, 122):
    extra = wav.readframes(1)
    #print(extra[0])

    #print('>%s' % extra[0])
    #print('>%s' % extra[1])
    #print("%s" % extra[0], "%s" % extra[1])
    if i == 18:
        ancho = extra[0]
    elif i == 19:
        ancho += (extra[0] * 256)
    elif i == 20:
        ancho += (extra[0] * 256 * 256)
    elif i == 21:
        ancho += (extra[0] * 256 * 256 * 256)
    elif i == 22:
        alto = extra[0]
    elif i == 23:
        alto += (extra[0] * 256)
    elif i == 24:
        alto += (extra[0] * 256 * 256)
    elif i == 25:
        alto += (extra[0] * 256 * 256 * 256)


print("alto")
print(alto)
print("ancho")
print(ancho)

#ancho=ancho*3
print("ancho efectivo: %i" % (ancho*3))
c_linea = 0
c_pixel = 0
flag = 0

linea = np.array([[[]]], dtype=int)
pixel = np.array([[[]]], dtype=int)

for i in range(0, pix):
    extra = wav.readframes(1)
    #print(extra[0])
    if c_pixel == 0:
        #print(extra , i)
        pixel = np.array([[[extra[0]]]])
        c_pixel += 1
    elif c_pixel == 1:
        pixel = np.append(pixel, [[[extra[0]]]], 2) #append en 2: dentro del array o cuando es el primer valor, append en 1: al lado del array
        c_pixel += 1
    elif c_pixel == 2:
        pixel = np.append(pixel, [[[extra[0]]]], 2)
        c_pixel = 0
        #pixel completo, añado a la horizontal
        if c_linea == 0:    #primer pixel en línea
            linea = pixel
        else:               #píxeles después del primero van en paralelo a este
            linea = np.append(linea, pixel, 0)
        pixel = np.array([[]], dtype=int)
        c_linea += 1
        if c_linea == ancho:    #linea completada
            c_linea = 0
            if flag == 0:
                full_image = linea #np.append(full_image, linea, 1)
                flag = 1
            else:
                full_image = np.append(full_image, linea, 1)
            linea = np.array([[]], dtype=int)



full_image=full_image.astype('uint8')
#full_image=full_image.reshape(900)

#raw.pop()
#scipy.misc.toimage(raw).save('out.bmp')
print('Size total:', len(full_image))

#print('Size 1:', len(full_image[0]))
#print('Size 1:', len(full_image[1]))
#print('Size 2:', len(full_image[2]))


#print(full_image[0])
print(full_image.dtype)


#arr = (np.eye(50)*200).astype(np.uint8)
#im = Image.fromarray(arr) # monochromatic image
#imrgb = im.convert('RGB') # color image
#imrgb.show()
#print(arr)
#imrgb.save('salida.bmp')

#rgb = bytes(raw)
#imagen_final = Image.frombytes("RGB", (300, 100), full_image)
#plt.imshow(full_image, interpolation='nearest')
#plt.show()
#scipy.misc.toimage(full_image, cmin=0.0, cmax=255.0, mode='I').save('outfile.bmp')
imagen_final = Image.fromarray(full_image, 'RGB')
#img_fnl= Image.convert("RGB", imagen_final)
#img_fnl.save('out2.PNG')
imagen_final = imagen_final.transpose(Image.ROTATE_270)
imagen_final = imagen_final.transpose(Image.FLIP_LEFT_RIGHT)
imagen_final.save('output.BMP')
