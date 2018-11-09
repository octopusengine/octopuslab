"""
This example of SSD1306 OLED display over I2C usage is drawing image and writing text on position
needs external driver ssd1306.py from https://github.com/micropython/micropython/blob/master/drivers/display/ssd1306.py

Set your SCL and SDA pins in constants

upload your test_image.pbm
How to create .pbm? https://forum.micropython.org/viewtopic.php?t=4901#p29699
"GIMP -> Set dimensions -> Index 1bit image -> Export pbm -> Binary" should get you there

Set your image WIDTH and HEIGHT in constants

Installation:
ampy -p /dev/ttyUSB0 put ./octopus_robot_board.py
ampy -p /dev/ttyUSB0 mkdir lib
ampy -p /dev/ttyUSB0 put ./lib/ssd1306.py lib/ssd1306.py
ampy -p /dev/ttyUSB0 mkdir assets
ampy -p /dev/ttyUSB0 put ./assets/octopus_image.pbm assets/octopus_image.pbm
ampy -p /dev/ttyUSB0 put ./05-oled-image.py main.py
# reset device
"""

import framebuf
import machine
import time
from lib import ssd1306

import octopus_robot_board as o #octopusLab main library - "o" < octopus

IMAGE_WIDTH = 63
IMAGE_HEIGHT = 63

i2c = machine.I2C(-1, machine.Pin(o.I2C_SCL_PIN), machine.Pin(o.I2C_SDA_PIN))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# test_whole display
oled.fill(1)
oled.show()

time.sleep_ms(300)

# reset display
oled.fill(0)
oled.show()


with open('assets/octopus_image.pbm', 'rb') as f:
    f.readline() # Magic number
    f.readline() # Creator comment
    f.readline() # Dimensions
    data = bytearray(f.read())
    fbuf = framebuf.FrameBuffer(data, IMAGE_WIDTH, IMAGE_HEIGHT, framebuf.MONO_HLSB)

    # To display just blit it to the display's framebuffer (note you need to invert, since ON pixels are dark on a normal screen, light on OLED).
    oled.invert(1)
    oled.blit(fbuf, 0, 0)

oled.text("Octopus", 66,6)
oled.text("Lab", 82,16)
oled.text("Micro", 74,35)
oled.text("Python", 70,45)
oled.show()
