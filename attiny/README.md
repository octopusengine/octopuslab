# octopuslab - attiny
temp_cz
V našich ukázkách budeme používat některý z nejjozšířenějších "osminohých" mikrokotrolerů ATMEL -> Attiny:<br />
<pre>
Attiny      13     45    85
Flash [kB]   1      4     8
SRAM  [B]   64    256   512 
EEPROM      64    256   512 
HW_UART      x     v     v   
HW_SPI       x     v     v
HW_I2C       x     v     v
</pre>
Celá <a href=https://en.wikipedia.org/wiki/Atmel_AVR_ATtiny_comparison_chart>tabulka</a><br />
Pro jednotlivá samostatná zapojení postačí Attiny13. Pro pokročilejší projekty (propojení po I2C/slave) použijeme Attiny85.<br />
<br />
<pre>
             Attiny 13/85 
           RST =--U--= VCC                  oeLAB dev board1                  
 > pinAn (A)P3 =     = P2 (A1) pinDall      (3) i2c Clock 
 Strobe2 (A)P4 =     = P1 / pinRX           (2) > LED 
           GND =     = P0 / pinTX >         (1) i2c Data 
</pre>

<img src="https://raw.githubusercontent.com/octopusengine/octopuslab/master/images/oe-lab-nano-sch2.png " alt="dev0-l3" width="500">



<hr />
<a href=https://www.arduinoslovakia.eu/page/attiny85>https://www.arduinoslovakia.eu/page/attiny85</a><br />
<a href=http://www.astromik.org/malymenu/menuraspi.htm>http://www.astromik.org/malymenu/menuraspi.htm</a><br />
<a href=https://www.hackster.io/atmel/products/attiny85>https://www.hackster.io/atmel/products/attiny85</a><br />
<a href=http://dangerousprototypes.com/blog/tag/attiny/>http://dangerousprototypes.com/blog/tag/attiny/</a><br />
<a href=https://hackaday.com/tag/attiny85/>https://hackaday.com/tag/attiny85/</a><br />
<a href=https://valentapetr.wordpress.com/2016/02/03/attiny85/>https://valentapetr.wordpress.com/2016/02/03/attiny85/</a><br />
<a href=https://github.com/XavierBerger/Arduino/tree/master/ATTiny85>https://github.com/XavierBerger/Arduino/tree/master/ATTiny85</a><br />
