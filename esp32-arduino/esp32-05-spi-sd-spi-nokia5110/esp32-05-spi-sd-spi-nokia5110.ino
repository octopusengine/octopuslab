/*
   Robot Board SD Card test
   Connection SD-->RobotBoard:
   MISO, MOSI, SCK to OctoBUS SPI header on RobotBoard
   CS to OctoBUS D1 on RobotBoard
*/
#include "FS.h"
#include "SD.h"

#include <U8g2lib.h>
#include <SPI.h>

#include "octopusLAB_ROBOT.h"

// Define CS pin, D1 on OctoBUS
#define SD_CS OB_D1

// Display init
U8G2_PCD8544_84X48_F_4W_HW_SPI u8g2(U8G2_R2, SS, 32);


void readFile(fs::FS &fs, const char * path) {
  Serial.printf("Reading file: %s\n", path);

  File file = fs.open(path);
  if (!file) {
    Serial.println("Failed to open file for reading");
    return;
  }

  Serial.print("Read from file: ");
  while (file.available()) {
    Serial.write(file.read());
  }
  file.close();
}


void setup() {
  Serial.begin(115200);

  Serial.println("Init LCD");
  u8g2.begin();
  u8g2.clearBuffer();
  u8g2.setContrast(130);
  u8g2.setFont(u8g2_font_ncenB08_tr);
  u8g2.drawStr(15, 8, "SD CARD");

  u8g2.setFont(u8g2_font_5x7_tr);
  u8g2.setCursor(0, 17);
  u8g2.print("Type: ");
  u8g2.sendBuffer();

  Serial.println("Init SD");
  if (!SD.begin(SD_CS)) {
    Serial.println("Card Mount Failed");
    u8g2.println("FAILED");
    u8g2.sendBuffer();
    return;
  }
  uint8_t cardType = SD.cardType();

  if (cardType == CARD_NONE) {
    u8g2.println("NO SD");
    u8g2.sendBuffer();
    Serial.println("No SD card attached");
    return;
  }

  Serial.print("SD Card Type: ");
  if (cardType == CARD_MMC) {
    u8g2.println("MMC");
    Serial.println("MMC");
  } else if (cardType == CARD_SD) {
    u8g2.println("SDSC");
    Serial.println("SDSC");
  } else if (cardType == CARD_SDHC) {
    u8g2.println("SDHC");
    Serial.println("SDHC");
  } else {
    u8g2.println("UNKNOWN");
    Serial.println("UNKNOWN");
  }
  
  u8g2.sendBuffer();

  uint64_t cardSize = SD.cardSize() / (1024 * 1024);

  Serial.printf("SD Card Size: %lluMB\n", cardSize);
  Serial.printf("Used space: %lluMB\n", SD.usedBytes() / (1024 * 1024));
  Serial.printf("Free space: %lluMB\n", (SD.totalBytes()-SD.usedBytes()) / (1024 * 1024));

  u8g2.setCursor(0, 24);
  u8g2.printf("Size: %lluMB\n", cardSize);
  u8g2.setCursor(0, 31);
  u8g2.printf("Used: %lluMB\n", SD.usedBytes() / (1024 * 1024));
  u8g2.setCursor(0, 38);
  u8g2.printf("Free: %lluMB\n", (SD.totalBytes()-SD.usedBytes()) / (1024 * 1024));

  u8g2.drawFrame(0, 40, 84, 8);
  u8g2.drawBox(1,41, map(SD.usedBytes() / 1024, 0, SD.totalBytes() / 1024, 0, 82), 7);
  
  u8g2.sendBuffer();

}

void loop() {

}
