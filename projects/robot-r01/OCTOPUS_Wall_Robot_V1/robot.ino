#define BUTTON_PIN DEV2

APDS9930 laser = APDS9930();

//robot setup
void initRobot() {
  initButton();
  neopixelInit();
  laser.init(); // APDS9930 sensor
  laser.enableProximitySensor(false); // enable proximity, no interrupt
  initMotor();
  initEcho();
}

//button setup
void initButton() {
  pinMode(BUTTON_PIN, INPUT_PULLUP);
}

//wait for button press and then unpress
void waitForButtonPress() {
  while (!isButtonPressed())
    delay(10);
  while (isButtonPressed())
    delay(10);
}

//reads the INPUT_PULLUP pin
boolean isButtonPressed() {
  return !digitalRead(BUTTON_PIN);
}

//returns what the APDS9930 sees in some kind of units <0,1024>
int getLaserDistance() {
  return laser.readProximity();
}
