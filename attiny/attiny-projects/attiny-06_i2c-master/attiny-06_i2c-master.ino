#include "TinyWireM.h"

void setup() {
  TinyWireM.begin();
  pinMode(1, OUTPUT);
}

uint8_t i;
void loop() {
  digitalWrite(1, HIGH);

  TinyWireM.beginTransmission(0x20);
  TinyWireM.write(i++ ^ 0xFF);
  TinyWireM.endTransmission();

  delay(250);
  
  digitalWrite(1, LOW);
  delay(250);
}
