#define BUTTON_PIN DEV2

APDS9930 Laser = APDS9930();

void initRobot() {
  initButton();
  neopixelInit();
  Laser.init(); // APDS-9930
  Laser.enableProximitySensor(false); // enable proximity, no interrupt
  initMoto();
}

void initButton() {
  pinMode(BUTTON_PIN, INPUT_PULLUP);
}

void waitForButtonPress() {
  while (!isButtonPressed())
    delay(10);
  while (isButtonPressed())
    delay(10);
}

boolean isButtonPressed() {
  return !digitalRead(BUTTON_PIN);
}

int getLaserDistance() {
  return Laser.readProximity();
}
