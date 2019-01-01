# 11 700 ms - direct write to TFT without FrameBuffer, RGB888 BMP 3 Byte per pixel
import struct
import utime

start = utime.ticks_ms()
f = open("octopuslogo-120w-3.bmp", "rb")

magic, size, res1,res2, imgoffset = struct.unpack('<2sIHHI', f.read(14))
imgheadersize, w, h, planes, bits, comp, imgdatasize, xres,yres, ncol, icol = struct.unpack('<IiiHHIIiiII', f.read(40))

rowSize = (w * 3 + 3) & ~3;


for row in range(0, h):
    pos = imgoffset + (h - 1 - row) * rowSize
    f.seek(pos)
    for col in range(0, w):
        b = ord(f.read(1))
        g = ord(f.read(1))
        r = ord(f.read(1))
        tft.pixel(col, row, color565(r,g,b))

print("Took: {0}ms".format(utime.ticks_ms()-start))


#-------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------


# 11 500 ms - direct write to TFT without FrameBuffer, RGB565 BMP 2 Byte per pixel
import struct
import utime

start = utime.ticks_ms()
f = open("octopuslogo-120w-565rgb.bmp", "rb")

magic, size, res1,res2, imgoffset = struct.unpack('<2sIHHI', f.read(14))
imgheadersize, w, h, planes, bits, comp, imgdatasize, xres,yres, ncol, icol = struct.unpack('<IiiHHIIiiII', f.read(40))

rowSize = (w * 2 + 2) & ~2;

for row in range(0, h):
    pos = imgoffset + (h - 1 - row) * rowSize
    f.seek(pos)
    for col in range(0, w):
        data = struct.unpack('<H', f.read(2))[0]
        tft.pixel(col, row, data)

print("Took: {0}ms".format(utime.ticks_ms()-start))


#-------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------


# 450ms write to global FrameBuffer and flush to TFT once
import struct
import utime

start = utime.ticks_ms()
f = open("octopuslogo-120w-565rgb.bmp", "rb")

magic, size, res1,res2, imgoffset = struct.unpack('<2sIHHI', f.read(14))
imgheadersize, w, h, planes, bits, comp, imgdatasize, xres,yres, ncol, icol = struct.unpack('<IiiHHIIiiII', f.read(40))

fr = f.read
fs = f.seek
sunp = struct.unpack
fbp = fb.pixel

rowSize = (w * 2 + 2) & ~2;

for row in range(0, h):
    pos = imgoffset + (h - 1 - row) * rowSize
    fs(pos)
    for col in range(0, w):
        data = sunp('>H', fr(2))[0]
        fbp(col, row, data)

tft.blit_buffer(fb, 0, 0, 128, 160)
print("Took: {0}ms".format(utime.ticks_ms()-start))


#-------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------


# 500ms, writing to temp FrameBuffer and direct flush to TFT per row
import struct
import utime

start = utime.ticks_ms()
f = open("octopuslogo-120w-565rgb.bmp", "rb")

magic, size, res1,res2, imgoffset = struct.unpack('<2sIHHI', f.read(14))
imgheadersize, w, h, planes, bits, comp, imgdatasize, xres,yres, ncol, icol = struct.unpack('<IiiHHIIiiII', f.read(40))

rowSize = (w * 2 + 2) & ~2;

fr = f.read
fs = f.seek
sunp = struct.unpack

tmpfb = framebuf.FrameBuffer(bytearray(rowSize), w, 1, framebuf.RGB565)
tmpfbp = tmpfb.pixel
tftbb = tft.blit_buffer

for row in range(0, h):
    pos = imgoffset + (h - 1 - row) * rowSize
    fs(pos)    
    for col in range(0, w):
        data = sunp('>H', fr(2))[0]
        tmpfbp(col, 0, data)

    tftbb(tmpfb, 0, row, w, 1)

print("Took: {0}ms".format(utime.ticks_ms()-start))


#-------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------


# 317ms, writing to temp FrameBuffer and direct flush to TFT per row
# Using 2 byte read, do not use struct.unpack but shift bites
import struct
import utime

start = utime.ticks_ms()
f = open("octopuslogo-120w-565rgb.bmp", "rb")

magic, size, res1,res2, imgoffset = struct.unpack('<2sIHHI', f.read(14))
imgheadersize, w, h, planes, bits, comp, imgdatasize, xres,yres, ncol, icol = struct.unpack('<IiiHHIIiiII', f.read(40))

rowSize = (w * 2 + 2) & ~2;

fr = f.read
fs = f.seek

tmpfb = framebuf.FrameBuffer(bytearray(rowSize), w, 1, framebuf.RGB565)
tmpfbp = tmpfb.pixel
tftbb = tft.blit_buffer

for row in range(0, h):
    pos = imgoffset + (h - 1 - row) * rowSize
    fs(pos)
    for col in range(0, w):
        data = fr(2)
        tmpfbp(col, 0, (data[0] << 8) + data[1])

    tftbb(tmpfb, 0, row, w, 1)

print("Took: {0}ms".format(utime.ticks_ms()-start))


#-------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------

# 250ms Just read, nothing else, no FrameBuffer no TFT write

import struct
import utime

start = utime.ticks_ms()
unp = struct.unpack
fr = f.read
fs = f.seek

for row in range(0, h):
    pos = imgoffset + (h - 1 - row) * rowSize
    fs(pos)
    for col in range(0, w):
        data = unp('>H', fr(2))[0]

print("Took: {0}ms".format(utime.ticks_ms()-start))


#-------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------

# 194ms Just read, nothing else, no FrameBuffer no TFT write

import struct
import utime

f = open("octopuslogo-120w-565rgb.bmp", "rb")

magic, size, res1,res2, imgoffset = struct.unpack('<2sIHHI', f.read(14))
imgheadersize, w, h, planes, bits, comp, imgdatasize, xres,yres, ncol, icol = struct.unpack('<IiiHHIIiiII', f.read(40))

rowSize = (w * 2 + 2) & ~2;

unp = struct.unpack
fr = f.read
fs = f.seek
o = ord # 227ms if ord not preloaded

start = utime.ticks_ms()

for row in range(0, h):
    pos = imgoffset + (h - 1 - row) * rowSize
    fs(pos)
    for col in range(0, w):
        data = (o(fr(1)) << 8) + o(fr(1))

print("Took: {0}ms".format(utime.ticks_ms()-start))

#-------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------

# 110ms Just read, nothing else, no FrameBuffer no TFT write

import struct
import utime

f = open("octopuslogo-120w-565rgb.bmp", "rb")

magic, size, res1,res2, imgoffset = struct.unpack('<2sIHHI', f.read(14))
imgheadersize, w, h, planes, bits, comp, imgdatasize, xres,yres, ncol, icol = struct.unpack('<IiiHHIIiiII', f.read(40))

rowSize = (w * 2 + 2) & ~2;

unp = struct.unpack
fr = f.read
fs = f.seek
o = ord # 227ms if ord not preloaded

start = utime.ticks_ms()

for row in range(0, h):
    pos = imgoffset + (h - 1 - row) * rowSize
    fs(pos)
    for col in range(0, w):
        dataread = fr(2)
        data = (dataread[0] << 8) + dataread[1]

print("Took: {0}ms".format(utime.ticks_ms()-start))


#-------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------

#  102ms Just read, nothing else, no FrameBuffer no TFT write

import struct
import utime

f = open("octopuslogo-120w-565rgb.bmp", "rb")

magic, size, res1,res2, imgoffset = struct.unpack('<2sIHHI', f.read(14))
imgheadersize, w, h, planes, bits, comp, imgdatasize, xres,yres, ncol, icol = struct.unpack('<IiiHHIIiiII', f.read(40))

rowSize = (w * 2 + 2) & ~2;

unp = struct.unpack
fr = f.read
fs = f.seek

start = utime.ticks_ms()

for row in range(0, h):
    pos = imgoffset + (h - 1 - row) * rowSize
    fs(pos)
    for col in range(0, w):
        data1 = fr(1)
        data2 = fr(1)

print("Took: {0}ms".format(utime.ticks_ms()-start))

#-------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------

#  67ms Just read, nothing else, no FrameBuffer no TFT write

import struct
import utime

f = open("octopuslogo-120w-565rgb.bmp", "rb")

magic, size, res1,res2, imgoffset = struct.unpack('<2sIHHI', f.read(14))
imgheadersize, w, h, planes, bits, comp, imgdatasize, xres,yres, ncol, icol = struct.unpack('<IiiHHIIiiII', f.read(40))

rowSize = (w * 2 + 2) & ~2;

unp = struct.unpack
fr = f.read
fs = f.seek

start = utime.ticks_ms()

for row in range(0, h):
    pos = imgoffset + (h - 1 - row) * rowSize
    fs(pos)
    for col in range(0, w):
        data = fr(2)

print("Took: {0}ms".format(utime.ticks_ms()-start))
