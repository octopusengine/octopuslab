#MicroPython - ESP32 with ROBOTboard
<hr>
Ne. Zatím to není úplně jednoduché. Viděl jsem návodů několik a nakonec, kdy jsem nenašel nic triviálního, nějak jsem to teda rozchodil (Většina se dělá v terminálu / cmd / příkazové řádce):<br />
Nainstaloval jsem python3 – hezky popsáno v [7]<br />
Pak jsem jel částečně podle [6] (kde je to pro Linux – musel jsem krapet ohýbat pro okna)<br />
Je nutno stáhnout micropython – vybíral jsem z [5] a nahrál jsem ho „vedle“ do adresáře /down<br />
Pak nainstalovat esptool [2]<br />
Připojí se ESP (na Win jsem detekoval port /COM6)<br />
<br />
Smaže se FLASH:
<pre>esptool.py --chip esp32 -p /COM6 erase_flash</pre>
Pak se stažená binárka z  [5] opět pomocí esptool  [2] z příkazové řádky uploadne do ESP32:
<pre>esptool.py --chip esp32 -p /COM6 write_flash -z 0x1000 ./down/esp32-20180821-v1.9.4-479-g828f771e3.bin</pre>
Testy lze provádět podle  [1] – což jsem dělal přes terminál v Putty (je to tam tuším také popsáno).
A soubory se nahrávají pomocí Ampy [8] – zde např boot.py (základ, co jede po spuštění):<br />

set AMPY_PORT=COM6<br />
ampy ls<br />
AMPY_BAUD=115200<br />
...
<pre>
ampy -p /COM6 get boot.py
# This file is executed on every boot (including wake-boot from deepsleep)
</pre>
..uf. No a microPython – to už je pohoda.

[1] https://naucse.python.cz/lessons/beginners/micropython/<br />
[2] https://github.com/espressif/esptool<br />
[3] http://iot-bits.com/esp32/esp32-flash-download-tool-tutorial/<br />
[4] https://www.14core.com/micropython-flashing-programming/<br />
[5] https://micropython.org/download#esp32<br />
[6] https://boneskull.com/micropython-on-esp32-part-1/<br />
[7] https://naucse.python.cz/course/pyladies/beginners/install/<br />
[8] https://github.com/adafruit/ampy<br />
