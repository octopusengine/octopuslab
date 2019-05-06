# OctopusLab/ESP32

Development board [ROBOT BOARD]("http://www.octopuslab.cz/index.php/vyvojove-desky/robot-board") - can be used (also) for projects that are in subfolders. This board is mainly targeted for robot development (cars, etc) but can be used for any similar.

## Pins

oeLAB-esp32 (DoIt) 2x15 pins:                               [ROBOT Board]:
                          -----------     (GPIO)
                      EN -           - D23 (23)  MOSI       [SPI_MOSI_PIN] 
[PIN_ANALOG]    (36)  VP -           - D22 (22)  SCL(I2C)   [I2C_SCL_PIN]
[I39_PIN]       (39)  VN -           - TXD (1)   D2
[I34_PIN]            D34 -           - RXD (3)   D3
[I35_PIN]            D35 -           - D21 (21)  SDA(I2C)   [I2C_SDA_PIN]
[ONE_WIRE_PIN] DEV1  D32 -           - D19 (19)  MISO       [SPI_MISO_PIN]
               DEV2  D33 -  (ESP32)  - D18 (18)  SCLK       [SPI_CLK_PIN]
[PIN_MOTOR_12EN]     D25 -           - D5  (5)   CS0        [SPI_CS0_PIN]
[PIN_MOTOR_1A]       D26 -           - TX2 (17)             [PIN_PWM1] /Servo1
[PIN_MOTOR_4A]       D27 -           - RX2 (16)             [PIN_PWM2] /Servo2
[PIN_MOTOR_3A]       D14 -           - D4  (4)              [PIN_PWM3] /Servo3
[PIN_MOTOR_2A]       D12 -           - D2  (2)              [BUILT_IN_LED]
[PIN_MOTOR_34EN]     D13 -           - D15 (15)             [WS_LED_PIN] //v1(13)     
                     GND -           - GND
                     VIN -           - 3V3 +
                          -----------

## Description of the ESP32
240 MHz dual core Tensilica LX6 microcontroller with 600 DMIPS
Integrated 520 KB SRAM
Integrated 802.11 b/g/n HT40 Wi-Fi transceiver, baseband, stack and LWIP
Integrated dual mode Bluetooth (classic and BLE)
16 MB flash, memory-mapped to the CPU code space
2.3V to 3.6V operating voltage
-40°C to +125°C operating temperature
On-board PCB antenna / IPEX connector for external antenna

Sensors	
Ultra-low noise analog amplifier, Hall sensor, 10x capacitive touch interfaces

32 kHz crystal oscillator
34x GPIO, 3 x UARTs, including hardware flow control
3 x SPI, 2 x I2S
12 x ADC input channels
2 x DAC, 2 x I2C
PWM/timer input/output available on every GPIO pin
OpenOCD debug interface with 32 kB TRAX buffer
SDIO master/slave 50 MHz

## Get help

Are you stuck with some problem with code or something similar? Dont worry! Theese links provide more informations and tutorials about this board.

### Usb to serial bridge
driver CP2102: https://www.pololu.com/docs/0J7/all [2018/05-Win10-ok]

### Links
https://github.com/espressif/arduino-esp32
https://randomnerdtutorials.com/getting-started-with-esp32/

### Micropython
https://github.com/octopusengine/octopuslab/tree/master/esp32-micropython
