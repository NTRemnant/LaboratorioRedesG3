from PIL import Image
import wave
import array
import sys
import struct

img = Image.open(sys.argv[1])

wav = wave.open(sys.argv[2], 'wb')

raw = array.array('B')

bmp = open(sys.argv[1], 'rb')

i = 0
#
# print('Type_1: %i' % struct.unpack('b', bmp.read(1)))
# print('Type_2: %i' % struct.unpack('b', bmp.read(1)))
# print('Size: %s' % struct.unpack('I', bmp.read(4)))
# print('Reserved 1: %s' % struct.unpack('H', bmp.read(2)))
# print('Reserved 2: %s' % struct.unpack('H', bmp.read(2)))
# print('Offset: %s' % struct.unpack('I', bmp.read(4)))
#
# print('DIB Header Size: %s' % struct.unpack('I', bmp.read(4)))
# print('Width: %s' % struct.unpack('I', bmp.read(4)))
# print('Height: %s' % struct.unpack('I', bmp.read(4)))
# print('Colour Planes: %s' % struct.unpack('H', bmp.read(2)))
# print('Bits per Pixel: %s' % struct.unpack('H', bmp.read(2)))
# print('Compression Method: %s' % struct.unpack('I', bmp.read(4)))
# print('Raw Image Size: %s' % struct.unpack('I', bmp.read(4)))
# print('Horizontal Resolution: %s' % struct.unpack('I', bmp.read(4)))
# print('Vertical Resolution: %s' % struct.unpack('I', bmp.read(4)))
# print('Number of Colours: %s' % struct.unpack('I', bmp.read(4)))
# print('Important Colours: %s' % struct.unpack('I', bmp.read(4)))
# exit()
while i < 122:
    extra = struct.unpack('B', bmp.read(1))
    #print(extra[0])
    raw.append(extra[0])
    i += 1


for r, g, b in img.getdata():
    raw.append(r)
    raw.append(g)
    raw.append(b)
    i += 1
    #print("%i" % r, "%i" % g, "%i" % b)

wav.setnchannels(1)

wav.setsampwidth(1)

wav.setframerate(44100)

wav.writeframes(raw)

print("frames: %i" % i)
print("size: %i" % len(raw))

wav.close()
