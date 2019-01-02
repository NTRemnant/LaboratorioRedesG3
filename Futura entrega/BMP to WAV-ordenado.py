from PIL import Image
import wave
import array
import sys
import struct

def convertirWavBin(wav):
    

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