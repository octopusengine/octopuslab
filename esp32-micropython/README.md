<pre>For czech readme, use the following link:
Pro české readme použijte následující link:
https://github.com/octopusengine/octopuslab/blob/master/esp32-micropython/README.CS_cz.md</pre>

# MicroPython - ESP32 - ROBOTboard / IoTboard

---
https://www.instagram.com/p/Boo4LTRALBZ/?taken-by=octopusengine

https://boneskull.com/micropython-on-esp32-part-1/


## PINout:
<pre>
oeLAB-esp32 (DoIt) 2x15 pins:                                [ROBOT Board]:::
                           -----------     (GPIO)
                       EN -           - D23 (23)  MOSI       [SPI_MOSI_PIN]
[PIN_ANALOG]     (36)  VP -           - D22 (22)  SCL(I2C)   [I2C_SCL_PIN]
[I39_PIN]        (39)  VN -           - TXD (1)   D2
[I34_PIN]             D34 -           - RXD (3)   D3
[I35_PIN]             D35 -           - D21 (21)  SDA(I2C)   [I2C_SDA_PIN]
[ONE_WIRE_PIN]   DEV1 D32 -           - D19 (19)  MISO       [SPI_MISO_PIN]
              T8 DEV2 D33 -  (ESP32)  - D18 (18)  SCLK       [SPI_CLK_PIN]
[MOTOR_12EN]          D25 -           - D5  (5)   CS0        [SPI_CS0_PIN]
[MOTOR_1A]            D26 -           - TX2 (17)             [PIN_PWM1] /Servo1
[MOTOR_4A]    T7      D27 -           - RX2 (16)             [PIN_PWM2] /Servo2
[MOTOR_3A]    T6      D14 -           - D4  (4)          T0  [PIN_PWM3] /Servo3
[MOTOR_2A]    T5      D12 -           - D2  (2)          T2  [BUILT_IN_LED]
[MOTOR_34EN]  T4      D13 -           - D15 (15)         T3  [WS_LED_PIN] //v1(13)     
                      GND -           - GND
                      VIN -           - 3V3 +
                           -----------
</pre>     


* install Python3 - https://www.python.org/downloads/
* download MicroPython - https://octopusengine.org/download/micropython/micropython-octopus.bin 
* install esptool - https://github.com/espressif/esptool  `pip install esptool`
* install ampy - `pip install adafruit-ampy` read more on https://github.com/adafruit/ampy

## Windows:
* connect ESP32 and detect COM port
* erase FLASH - During this phase the BOOT button needs to be pressed down until connection is established.
    <pre>esptool.py --chip esp32 -p /COM6 erase_flash</pre>
* upload Micropython bin:
    <pre>esptool.py --chip esp32 -p /COM6 write_flash -z 0x1000 ./down/esp32-_FileVersion_.bin</pre>
* Now choose one of these options:
    * [Prepare](https://github.com/octopusengine/octopuslab/blob/master/esp32-micropython/prepare.bat)
        <pre>  - requires fewer initial files(1)
        - copies only files necesarry for initial setup
        - finishes quicker than Deploy</pre>
        <pre>You can pass your port ID (for instance COM3) as first parameter
        if you're running the script from command line.</pre>
    * [Deploy](https://github.com/octopusengine/octopuslab/blob/master/esp32-micropython/deploy.bat)
        <pre>  - requires whole directory
        - copies all files from root director
        - takes longer than Prepare</pre>
        <pre>You can pass your port ID (for instance COM3) as first parameter
        if you're running the script from command line.</pre>
    * webrepl1
    * blockly and webrepl


## Linux (for all distors based on Debian)

Serial port is usually `/dev/ttyUSB0`, if not sure or does not work, you can read it in last line of `dmesg | tail` just after plugging USB

To connect to REPL terminal use command `screen /dev/ttyUSB0 115200`

Exiting terminal is little tricky, you need to use screen control sequence: <kbd>CTRL+A</kbd> <kbd>K</kbd>, then confirm pressing <kbd>y</kbd>
If you exit any other way, connection may stay open and block other interaction (uploading files, reattaching to the REPL), safe way to fix this is to unplug USB and plug again.

    
## Mac
1. Install Drivers: 
Download newest driver for Mac https://www.pololu.com/docs/0J7/all
Unpack, Install and don´t forget to ALLOW in Security & Privacy settings

2. Detect Device
Go to About This Mac >> System Report and under Hardware/USB find your device in USB tree

3. Find the name of the Device in Terminal:
Terminal change directory: cd dev (press Enter) 
Terminal list: ls 

4. Find your device in list as tty.(something)

5. In our case we used:
screen /dev/tty.SLAB_USBtoUART 115200


### Things you need to have

Before anything else please make sure you have theese packages installed on your system:

1. build-essential
2. libreadline-dev
3. libffi-dev
4. git
5. pkg-config (At least Ubuntu on version 14.04 or higher).

### Installation

To install theese packages (excluding git) use this command:

```
sudo apt-get install build-essential libreadline-dev libffi-dev git pkg-config
```

Clone Micropython repo using this command:

```
git clone --recurse-submodules https://github.com/micropython/micropython.git
```

Move to the build direcory > cd ./micropython/ports/unix
Make executable > make axtls, make

To run the executable file type ./micropython .

### Other distors

For other distros please use this link: https://github.com/micropython/micropython/wiki/Getting-Started

### Port etc.
Serial port: /dev/ttyUSB0
Tetminal: screen /dev/ttyUSB0 115200 > press ENTER 
CTRL+A, K, (y) => screen, kill 


### Next steps

Other steps for linux are the same as for Windows (see other sections)



## Initial setup

* Prepare
    * From our Micropython frok run:
>>> octopus_initial.setup()

w > setup wifi (SSID and PSW)
cw > connect wifi
sd > system download

<pre>
      ,'''`.
     /      \
     |(@)(@)|
     )      (
    /,'))((`.\
   (( ((  )) ))
   )  \ `)(' / (

Hello, this will help you initialize your ESP
2019/03 (c)octopusLAB
Press Ctrl+C to abort

"==============================
        S E T U P
"===============================
[w]   - wifi submenu
[cw]  - connect wifi
[sd]  - system downloa
[x]   - exit setup
"==============================
</pre>
    * select <b>w</b> (set wifi) to assign wifi credentials
    * select <b>ds</b> (device setting), then choose which board you're using    
    * select <b>cw</b> (connect wifi) to reach the internets!
    * select <b>sd</b> (system downloads) to download and apply the rest of files
<pre>
next:
setup()

"==================================================
        S E T U P - I / O    (interfaces)
"==================================================
[ 1] -      led [1] - built in LED diode
[ 2] -       ws [1] - WS RGB LED 0/1/8/...n
[ 3] -     led7 [0] - SPI max 8x7 segm.display
[ 4] -     led8 [0] - SPI max 8x8 matrix display
[ 5] -     oled [0] - I2C oled display
[ 6] -      lcd [0] - I2C LCD 0/2/4 row
[ 7] -      tft [0] - SPI 128x160 color display
[ 8] -       sm [0] - UART - serial monitor (display)
[ 9] -     temp [0] - temperature Dallas sens.
[10] -    light [0] - I2C light sens. (lux)
[11] -     mois [0] - A/D moisture sensor
[12] -    cmois [0] - A/D capacit. moisture sensor
[13] -      ad0 [0] - A/D input voltage
[14] -      ad1 [0] - A/D x / photoresistor
[15] -      ad2 [0] - A/D y / thermistor
[16] -   keypad [0] - Robot I2C+expander 4x4 keypad
[17] -   button [0] - DEV2 Button
[18] -      fet [0] - MOS FET PWM (IoTboard)
[19] -    relay [0] - Relay (IoTboard)
[20] -    servo [0] - PWM pins (both Robot and IoT have by default)
[21] -  stepper [0] - Stepper motor (ROBOTboard)
[22] -    motor [0] - DC motor (ROBOTboard)
...
</pre>

## File structure

<pre>

root
 ╟─ boot.py
 ╟─ main.py
 ║
 ╠═ assets
 ║
 ╠═ config (json config files - device/wifi/...)
 ║
 ╠═ lib
 ║
 ╠═ pinouts (boards and soc type)
 ║
 ╠═ util ═╦═ setup
 ║        ╠═ led/buzzer
 ╠═ ...   ╠═ ...
</pre>
