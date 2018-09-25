#include <APDS9930.h>
#include <Adafruit_NeoPixel.h>

#include "octopusLAB_ROBOT.h"

#define CYCLES_PER_SECOND 100

int speed_forward = 90;
int speed_pidcorrection = 90;

float kK = 1;
float pK = 0.75;
float dK = 120;
float iK = 0;
int n_EMA = 10;

void setup() {
  Serial.begin(115200); // Starts the serial communication
  initRobot();
}

float error_last = 0;

void loop() {

  wsSetRed();
  waitForButtonPress();
  wsSetGreen();
  delay(500);
  
  while (!isButtonPressed()) {
    int echo = updateEcho();
    int laser = getLaserDistance();

    Serial.print("Btn: " + String(isButtonPressed()));

    Serial.print(", Ech: " + String(echo));
    Serial.print(", Las: " + String(laser));

    float error = calcLaserError(laser);
    int delta = calcSpeedCorrection(error, error_last);
    error_last = error;

    Serial.print(", Err: " + String(error));

    int speed_left = speed_forward + delta;
    int speed_right = speed_forward - delta;

    Serial.print(", Left: " + String(speed_left));
    Serial.print(", Rght: " + String(speed_right));

    motorLeft(speed_left);
    motorRight(speed_right);

    Serial.println();
  }

  motorLeft(0);
  motorRight(0);
  while (isButtonPressed())
  delay(10);

}
