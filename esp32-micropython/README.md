# MicroPython - ESP32 with ROBOTboard

---
https://www.instagram.com/p/Boo4LTRALBZ/?taken-by=octopusengine

https://boneskull.com/micropython-on-esp32-part-1/


## PINout:
<pre>
oeLAB-esp32 (DoIt) 2x15 pins:                               [ROBOT Board]:::
                          -----------     (GPIO)
                      EN -           - D23 (23)  MOSI       [SPI_MOSI_PIN] 
[PIN_ANALOG]    (36)  VP -           - D22 (22)  SCL(I2C)   [I2C_SCL_PIN]
[I39_PIN]       (39)  VN -           - TXD (1)   D2
[I34_PIN]            D34 -           - RXD (3)   D3
[I35_PIN]            D35 -           - D21 (21)  SDA(I2C)   [I2C_SDA_PIN]
[ONE_WIRE_PIN] DEV1  D32 -           - D19 (19)  MISO       [SPI_MISO_PIN]
               DEV2  D33 -  (ESP32)  - D18 (18)  SCLK       [SPI_CLK_PIN]
[MOTOR_12EN]         D25 -           - D5  (5)   CS0        [SPI_CS0_PIN]
[MOTOR_1A]           D26 -           - TX2 (17)             [PIN_PWM1] /Servo1
[MOTOR_4A]           D27 -           - RX2 (16)             [PIN_PWM2] /Servo2
[MOTOR_3A]           D14 -           - D4  (4)              [PIN_PWM3] /Servo3
[MOTOR_2A]           D12 -           - D2  (2)              [BUILT_IN_LED]
[MOTOR_34EN]         D13 -           - D15 (15)             [WS_LED_PIN] //v1(13)     
                     GND -           - GND
                     VIN -           - 3V3 +
                          -----------
</pre>     



## Windows:
- install Python3 
- download MicroPython [1] https://micropython.org/download#esp32
- install esptool.py [2] https://github.com/espressif/esptool
- install ampy [3] https://github.com/adafruit/ampy <pre>
set AMPY_PORT=COM6
ampy ls
AMPY_BAUD=115200
</pre>
- connect ESP32 and detect COM port
- erase FLASH: <pre>esptool.py --chip esp32 -p /COM6 erase_flash</pre>
- upload Micropython bin: <pre>esptool.py --chip esp32 -p /COM6 write_flash -z 0x1000 ./down/esp32-20180821-v1.9.4-479-g828f771e3.bin</pre>

</pre>

https://github.com/octopusengine/octopuslab/blob/master/esp32-micropython/deploy.bat

---
a) deploy (.sh for Linux or .bat fo Windows) 
> copy "all" files

b) prepare (.sh for Linux or .bat fo Windows) 
> copy only:
 util/setup > setup wifi, connect wifi, 
 util/wifi_connect.py
 boot_prepare.py
 > automaticaly download and instal from .tar file

c) webrepl
d) blockly and webrepl

---



<pre>
--+--assets
  |
  +--config (json config files - device/wifi/...)
  |
  +--lib 
  |
  +--pinouts (boards and soc type)
  |
  +--util-----+--setup
  |           +--led/buzzer 
  |           +--...
  ...
</pre>


---
simple examples - categories:

01 - basic test

02 - simple experiment

03 - i/o test - sensor

04 - special sensors

05 - spi/i2c devices

06 - basic motor test

07 - mechatronics

08 - wifi/bf/ir - remote (setup or control)

09 - project, complex examples








