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

<pre>
programátor Attiny - 5 drátků:
Arduino Nano –> ATtiny85
5V –> Vcc (Attiny má na desce 3V napájecí větev přerušenou "mikro jumperem")
Pin 13 –> Pin 2
Pin 12 –> Pin 1
Pin 11 –> Pin 0
Pin 10 –> Reset
Gnd = Gnd (to už je propojeno)
</pre>
na desku DEV BOARD1 neosazovat NIC dalšího! Tiny se programuje při 5V a napájení má 3V
my musíme provést drobný "nebezpečný hack", kdy pro tiny spojíme 3 na 5 (mikro JPM "3V3" nepropojovat!)...<br />

<br />
1) naprogramujeme NANO:<br />
<pre>
Arduino/Soubor/Příklady/ArduinoISP 
</pre>
<br />
<i>a připojíme kondenzátor 10uF mezi RESEET a GND</i><br />
<br />
2) rozšíříme Arduino vývojové prostředí o Attiny:<br />
(jedna z možností attiny45/85)<br />
<pre>
http://honzasmolik.cz/attiny45_85.zip</pre>
<br />
<br />
3) Attiny programujeme podle typu - z nabídky Tools–Board, + Arduino jako ISP 
<br /><br />

<hr />
<a href=http://honzasmolik.cz/ISPprog.html>Arduino jako ISP programátor > http://honzasmolik.cz/ISPprog.html</a><br />

<br />
