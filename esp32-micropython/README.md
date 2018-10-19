# MicroPython - ESP32 with ROBOTboard

<hr />
https://www.instagram.com/p/Boo4LTRALBZ/?taken-by=octopusengine
<br />
https://boneskull.com/micropython-on-esp32-part-1/<br />
<br />


## Windows:
- install Python3 <br />
- download MicroPython [1] https://micropython.org/download#esp32<br />
- install esptool.py [2] https://github.com/espressif/esptool<br />
- install ampy [3] https://github.com/adafruit/ampy<br />
- connect ESP32 and detect COM port<br /> 
- erase FLASH:
<pre>esptool.py --chip esp32 -p /COM6 erase_flash</pre>
<br /> 
- upload Micropython bin: 
<pre>esptool.py --chip esp32 -p /COM6 write_flash -z 0x1000 ./down/esp32-20180821-v1.9.4-479-g828f771e3.bin</pre>

<pre>
set AMPY_PORT=COM6<br />
ampy ls<br />
AMPY_BAUD=115200<br />
...
</pre>
- copy *.py file to ESP<br />
<pre>
ampy -p /COM6 get boot.py
# This file is executed on every boot (including wake-boot from deepsleep)
</pre>
<hr />


