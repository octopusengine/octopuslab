// Example OLED display
// Using U8G2 library

#include <U8g2lib.h>
#include <Wire.h>

U8G2_SSD1306_128X64_NONAME_F_HW_I2C u8g2(U8G2_R0);

void init_oled() {
  u8g2.begin();

  u8g2.setFontMode(0);
  u8g2.setFont(u8g2_font_cu12_hr);
}

void setup()
{
  Serial.begin(115200);

  init_oled();

  u8g2.clearBuffer();
  u8g2.setCursor(0,15);
  u8g2.print("octopusLab");
  u8g2.sendBuffer();
}

//Timer 1
unsigned long timer1Last = 0;
void timer1(int interval) {
  if (millis() < timer1Last+interval) {
    return;
  }
  timer1Last = millis();

  u8g2.setCursor(0, 35);
  u8g2.print("Up: ");
  u8g2.print("         "); // clear

  u8g2.setCursor(30, 35);
  u8g2.print(millis());

  u8g2.sendBuffer();
}

void loop()
{
  timer1(500);
}
