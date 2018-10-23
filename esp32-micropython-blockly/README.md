esptool.py --chip esp32 -p /COM6 erase_flash
esptool.py --chip esp32 -p /COM6 write_flash -z 0x1000 ./down/esp32-20181020-v1.9.4-665-g7795b2e5c.bin 

cd _yenda/micropy

ampy -p /COM6 ls
ampy -p /COM6 put boot.py
ampy -p /COM6 get boot.py
ampy -p /COM6 put 05-oled-image.py boot.py
