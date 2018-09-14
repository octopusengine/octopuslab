# octopuslab - esp8266
temp_cz
LoLin / Wemos / ...

<br />
<hr />
oeLAB - esp8266 pins:<br />
<pre>
     -----------   (GPIO)
 A0 -           - D0(16)     PIEZZO 1k 
  G -           - D1(05)   > I2C-CLK
 VU -           - D2(04)  <> I2C-DATA
 S3 -           - D3(00)   < FLASH/BTN
 S2 -  NodeMcu  - D4(02)  <> DIN-ONEWIRE/LED
 S1 -           - 3V         +
 SC -  (Lolin)  - G          x/GND
 S0 -           - D5(14)   > SPI-CLK
 SK -           - D6(12)     CS2/PIEZZO2  
  G -           - D7(13)  <> SPI-DATA
 3V -           - D8(15)   > SPI-CS1
 EN -           - RX(03)   > RX
RST -           - TX(01)   < TX
  G -           - G          GND
VIN -           - 3V         +
     -----------
</pre>
<br />
<pre>
     -----------   (GPIO)
 TX -           - RST
 RX -           - A0 / ADC
 D1 -           - D0
 D2 -           - D5
 D3 -   WeMos   - D6
 D4 -           - D7         
GND -           - D8          
 5V -           - 3V         +
     -----------
</pre>
<br />


<hr />
Arduino IDE
http://arduino.esp8266.com/stable/package_esp8266com_index.json<br />
<br /><br />
<hr />
Micropython<br />
win:<br />
https://github.com/nodemcu/nodemcu-flasher<br /> > flash bin:
http://micropython.org/download#esp8266<br />
esp8266-20180511-v1.9.4.bin (elf, map) (latest)<br />
https://docs.micropython.org/en/latest/esp8266/esp8266/tutorial/intro.html<br />
<a href = https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html>putty</a>: COM port / Serial / Speed: 115200 / Flow Control: None<br />
<br />
https://naucse.python.cz/2018/pyladies-brno-podzim/beginners/micropython/<br />


