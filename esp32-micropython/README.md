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
<pre>
oeLAB-esp32 (DoIt) 2x15 pins:                              [ROBOT Board]:
                          -----------     (GPIO)
                      EN -           - D23 (23)  MOSI
                I36   VP -           - D22 (22)  SCL(I2C)   [I2C_SCL_PIN]
                I39   VN -           - TXD (1)   D2
                I34  D34 -           - RXD (3)   D3
                I35  D35 -           - D21 (21)  SDA(I2C)   [I2C_SDA_PIN]
[ONE_WIRE_PIN] DEV1  D32 -           - D19 (19)
               DEV2  D33 -  (ESP32)  - D18 (18)
          MOTO_12EN  D25 -           - D5  (5)   CS0
          MOTO1A     D26 -           - TX2 (17)  PIN_PWM1 
          MOTO4A     D27 -           - RX2 (16)  PIN_PWM2
          MOTO3A     D14 -           - D4  (4)   PIN_PWM3
          MOTO2A     D12 -           - D2  (2)              [LED_BUILTIN]
          PIN_WS     D13 -           - D15       MOTO_34EN
                     GND -           - GND
                     VIN -           - 3V3 +
                          -----------
</pre>
<hr />



