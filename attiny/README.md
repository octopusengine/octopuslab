# 555 je retro - přejděte konenečně na attiny!
octopusLAB - temp_cz<br /><br />
<img src="https://raw.githubusercontent.com/octopusengine/octopuslab/master/images/attiny-schem3-export1.png" alt="attiny" width="500">
<br />

V našich ukázkách budeme používat některý z nejrozšířenějších "osminohých" mikrokotrolerů ATMEL -> Attiny:<br />
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
Pro úvodní výuková zapojení postačí i Attiny13, ale už i pro trochu pokročilejší projekty (sérivá komunikace s <a href ="https://github.com/octopusengine/serial-display">displejem</a>, propojení po I2C/slave) použijeme Attiny85.<br />
<br />
<pre>
             Attiny 13/45/85 
           RST +--U--+ VCC                 oeLAB dev board1                  
 > pinAn (A)P3 |     | P2 (A1)pinDall  (3) i2c Clock 
      Rx (A)P4 |     | P1              (2) > LED 
           GND +-----+ P0              (1) i2c Data 
</pre>
<br /><br />
Podporované základní příkazy (Arduino C):<br />
<pre>
pinMode(pin,mode)
digitalWrite(pin,int)
digitalRead(pin)
analogRead(pin)
analogWrite(int)
shiftOut(int)
pulseIn(pin)
Millis(int)
Micros(int)
delay(int)
delayMicroseconds (int)
</pre>
<br />
Zapojení na oeLAB - DEV BOARD:<br />
<img src="https://raw.githubusercontent.com/octopusengine/octopuslab/master/images/oe-lab-nano-sch1.png" alt="dev0-l3" width="500">
<br /><br />
Detailní výřez - jen přímo propojené spoje na desce:<br />
<img src="https://raw.githubusercontent.com/octopusengine/octopuslab/master/images/oe-lab-1808sch-tiny.png" alt="dev0" width="500">
<br />


<hr />
<a href=https://www.arduinoslovakia.eu/page/attiny85>https://www.arduinoslovakia.eu/page/attiny85</a><br />
<a href=http://www.astromik.org/malymenu/menuraspi.htm>http://www.astromik.org/malymenu/menuraspi.htm</a><br />
<a href=https://www.hackster.io/atmel/products/attiny85>https://www.hackster.io/atmel/products/attiny85</a><br />
<a href=http://dangerousprototypes.com/blog/tag/attiny/>http://dangerousprototypes.com/blog/tag/attiny/</a><br />
<a href=https://hackaday.com/tag/attiny85/>https://hackaday.com/tag/attiny85/</a><br />
<a href=https://valentapetr.wordpress.com/2016/02/03/attiny85/>https://valentapetr.wordpress.com/2016/02/03/attiny85/</a><br />
<a href=https://github.com/XavierBerger/Arduino/tree/master/ATTiny85>https://github.com/XavierBerger/Arduino/tree/master/ATTiny85</a><br />
<br /><br /><br />
Některé základy je dobré vysvětlit i přímo na vnitřní struktuře mikrokontroléru. Nebojte se zdánlivé složitosti. Prostě z paměti programů, čítač postupně bere příkazy, které se dekódují a provádějí - s pomocí registrů, ALU a řídících signálů:<br /><br />
<img src="https://raw.githubusercontent.com/octopusengine/octopuslab/master/images/attiny-schem3-export2.png" alt="attiny" width="500">
<br />
