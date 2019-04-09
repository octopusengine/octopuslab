# poznámky k instalaci a provozování

9. 4. 2019

přenastavit si COM na COM6 >

esptool.py --chip esp32 -p /COM6 erase_flash
esptool.py --chip esp32 -p /COM6 write_flash -z 0x1000 ./down/esp32-20190409-v1.10-271-g74ed06828.bin

pak:
prepare.bat COM6

---

setup() - ds, sw, cw, sdo
verze sdo: latest.tar - size 101 376 B

octopus() - jede jen po čerstvém rebootu - bez předchozícho spuštěného setup()

---
