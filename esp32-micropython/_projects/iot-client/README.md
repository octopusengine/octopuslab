<pre>
>>>
MPY: soft reboot
      ,'''`.
     /      \
     |(@)(@)|
     )      (
    /,'))((`.\
   (( ((  )) ))
   )  \ `)(' / (


------------------------------
[--- 1 ---] boot device >
iot-client.py > ESP32
ver: 0.52 / 5.7.2019 (c)octopusLAB
id: 807d3af7e8d8
Free: 54048

------------------------------
[--- 2 ---] init - variables and functions >
        I / O    (interfaces)
==============================
     led [1] - built in LED diode
      ws [8] - WS RGB LED 0/1/8/...n
    led7 [1] - SPI max 8x7 segm.display
    led8 [0] - SPI max 8x8 matrix display
    oled [1] - I2C oled display
     lcd [0] - I2C LCD 0/2/4 row
     tft [0] - SPI 128x160 color display
      sm [0] - UART - serial monitor (display)
    temp [1] - temperature Dallas sens.
   light [0] - I2C light sens. (lux)
    mois [0] - A/D moisture sensor
   cmois [0] - A/D capacit. moisture sensor
     ad0 [0] - A/D input voltage
     ad1 [0] - A/D x / photoresistor
     ad2 [0] - A/D y / thermistor
  keypad [0] - Robot I2C+expander 4x4 keypad
  button [0] - DEV2 Button
     fet [0] - MOS FET PWM (IoTboard)
   relay [0] - Relay (IoTboard)
   servo [0] - PWM pins (both Robot and IoT have by default)
 stepper [0] - Stepper motor (ROBOTboard)
   motor [0] - DC motor (ROBOTboard)
        M Q T T  (config)
==============================
hostName:wood

init i2c >
Free: 47360
WS RGB LED init neopixel >
WS RGB LED test >
Traceback (most recent call last):
  File "main.py", line 657, in <module>
  File "util/ws_rgb.py", line 72, in neopixelTest
  ...
</pre>  
