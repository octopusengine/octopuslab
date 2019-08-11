<pre>For english readme, use the following link:
Pro anglické readme použijte následující link:
https://github.com/octopusengine/octopuslab/blob/master/esp32-micropython/README.md
</pre>

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

## Windows:
* nainstalujte si Python3 - https://www.python.org/downloads/
* stáhněte si MicroPython - https://micropython.org/download#esp32 
   nebo stabilní a odzkoušenou verzi z: https://octopusengine.org/download/micropython-octopus.bin
* nainstalujte si esptool - https://github.com/espressif/esptool `pip install esptool`
* nainstalujte si ampy - https://github.com/adafruit/ampy `pip install adafruit-ampy`
* připojte ESP32 a zjistěte si na kterém COM portu je připojený
* smažte FLASH - Pro tuto fázi je potřeba podržet tlačítko BOOT až do doby než se naváže spojení. (connected)
    <pre>esptool.py --chip esp32 -p /COM6 erase_flash</pre>
* nahrajte na ESP32 Micropython bin: 
    <pre>esptool.py --chip esp32 -p /COM6 write_flash -z 0x1000 ./down/esp32-_FileVersion_.bin</pre>
* vyberte <b>jednu</b> z možností instalace:
    * [Příprava](https://github.com/octopusengine/octopuslab/blob/master/esp32-micropython/prepare.bat)
        <pre>  - vyžaduje méně souborů(1)
        - na ESP zkopíruje jen soubory potřebné k prvostnímu nastavení
        - trvá kratší dobu než Nasazení</pre>
        <pre>Při spuštění batového skriptu za pomoci příkazové řádky 
        můžete nastavit název portu jako první parametr.</pre>
    * [Nasazení](https://github.com/octopusengine/octopuslab/blob/master/esp32-micropython/deploy.bat)
        <pre>  - vyžaduje stažený celý adresář
        - kopíruje všechny soubory z hlavního adresáře
        - trvá déle než Příprava</pre>
        <pre>Při spuštění batového skriptu za pomoci příkazové řádky 
        můžete nastavit název portu jako první parametr.</pre>
    * webrepl1
    * blockly and webrepl

(1) Soubory potřebné k Přípravě jsou následující: (i s adresáři)
<pre> boot_prepare.py
 /config/device.json
 /util/setup.py
 /util/sys_info.py
 /util/wifi_connect.py
</pre>

## Prvotní nastavení

* Příprava
      prepare.bat 
      * Po nabootovní za pomoci Putty (nebo podobného software), zadejte příkaz setup()
        <pre>
        ==============================
                S E T U P
        ==============================
         [w]   - wifi submenu
         [cw]  - connect wifi
         [sdp] - system download > petrkr (update octopus modules from URL)
         [sdo] - system download > octopus (update octopus modules from URL)
         [ds]  - device setting
         .....
         [e]   - exit setup
        ==============================</pre>
    * vyberte <b>ds</b> (device setting), poté vyberte které nastavení budete používat
    * vyberte <b>sw</b> (set wifi) pro nastavení přístupových údajů na wifi
    * vyberte <b>cw</b> (connect wifi) pro připojení k wifi
    * vyberte <b>sd</b> (system downloads) aby se stáhl zbytek souborů
    
* Nasazení
    deploy.bat
    * Po nabootovní za pomoci Putty (nebo podobného software), zadejte příkaz Octopus()
        <pre>
        

## Struktura souborů

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







