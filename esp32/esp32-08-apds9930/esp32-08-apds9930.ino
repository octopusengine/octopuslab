//esp32-08-apds9930 - simple test: one distance senzor
//octopusLAB - ESP32 ROBOT board (2018/09)

#define DEBUG

#include "octopusLAB_ROBOT.h"
//#define PIN_WS  13

#include <APDS9930.h>
APDS9930 apds = APDS9930();

void setup() {
  apds.init(); // APDS-9930
  apds.enableProximitySensor(false); // enable proximity, no interrupt

  Serial.begin(57600);
}

void loop() {
  while (true) {
    Serial.println((String("Vzdalenost: ") + String(apds.readProximity())));
    delay(50);
  }
}
