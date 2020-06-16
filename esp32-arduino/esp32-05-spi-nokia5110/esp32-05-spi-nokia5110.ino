/*
 * ESP32 Nokia 5110 LCD display test
 * 
*/
#include <U8g2lib.h>
#include <SPI.h>

#include "octopus_40.h"
#include "octopus_60.h"

U8G2_PCD8544_84X48_F_4W_HW_SPI u8g2(U8G2_R0, /* cs=*/ SS, /* dc=*/ 32);

void setup(void) {
  u8g2.begin();
  u8g2.clearBuffer();
  u8g2.setContrast(130);
  u8g2.setFont(u8g2_font_ncenB08_tr);
  u8g2.drawStr(10,8,"OctopusLAB");
  
  u8g2.setFont(u8g2_font_5x7_tr);
  u8g2.drawStr(0,17,"powered by");
  u8g2.drawStr(0,24,"octopusengine.org");
  u8g2.drawXBM(15,27, octopus_40_width, octopus_40_height, octopus_40_bits);
  u8g2.sendBuffer();
  delay(5000);
  
  u8g2.clearBuffer();
  u8g2.drawStr(20,8,"OctopusLAB");
  u8g2.drawXBM(10,12, octopus_60_width, octopus_60_height, octopus_60_bits);
  u8g2.sendBuffer();
}

void loop(void) {

}

