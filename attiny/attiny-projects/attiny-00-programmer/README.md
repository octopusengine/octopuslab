# octopuslab - Arduino nano > Attiny programmer
programování Attiny (základ SPI)
<pre>
    oeLAB dev board1:
        Attiny 13/85 >> ((Arduino Nano)) 
((10 )) RST =--U--= VCC ((+5V))                   
         P3 =     = P2  ((13)) SCK 
         P4 =     = P1  ((12)) MISO 
        GND =     = P0  ((11)) MOSI 
</pre>
<br />
1) naprogramujeme NANO:<br />
<pre>
Arduino/Soubo/Příklady/ArduinoISP 
</pre>
<br />
<br />
<i>a připojíme kondenzátor 10uF mezi RESEET a GND</i><br />
2) rozšíříme Arduino vývojové prostředí o Attiny:<br />
(jedna z možností attiny45/85)<br />
<pre>
http://honzasmolik.cz/attiny45_85.zip</pre>
<br />
<br />
<br />
<a href=http://honzasmolik.cz/ISPprog.html>Arduino jako ISP programátor > http://honzasmolik.cz/ISPprog.html</a><br />

<br />
