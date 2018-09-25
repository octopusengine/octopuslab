#include <APDS9930.h>
#include <Adafruit_NeoPixel.h>

#include "octopusLAB_ROBOT.h"

#define CYCLES_PER_SECOND 200

int speed_forward = 90;
int speed_pidcorrection = 90;

float kK = 1;
float pK = 0.75;
float dK = 100;
float iK = 0; //Nechat na 0 - potřebuje dodělat
int n_EMA = 10;

void setup() {
  Serial.begin(115200); // Starts the serial communication
  initRobot();
}

long loop_millis_last = 0;
float error_last = 0;

void loop() {

  wsSetRed();
  waitForButtonPress();
  wsSetGreen();
  delay(500);

  while (!isButtonPressed()) {

    long microseconds = micros();

    while (millis() - loop_millis_last < 1000 / CYCLES_PER_SECOND) {
      delayMicroseconds(100);
    }

    loop_millis_last = millis();

    int echo = updateEcho();
    int laser = getLaserDistance();
    
    Serial.print("Ech: " + String(echo));
    Serial.print(", Las: " + String(laser));

    //Serial.print(", Btn: " + String(isButtonPressed()));
   
    float error = calcLaserError(laser);
    int delta = calcSpeedCorrection(error, error_last);
    error_last = error;

    //Serial.print(", Err: " + String(error));

    int speed_left = speed_forward + delta;
    int speed_right = speed_forward - delta;

    //Serial.print(", Left: " + String(speed_left));
    //Serial.print(", Rght: " + String(speed_right));

    motorLeft(speed_left);
    motorRight(speed_right);

    Serial.println(", uS: " + String(micros() - microseconds));

    Serial.println();
  }

  motorLeft(0);
  motorRight(0);
  while (isButtonPressed())
    delay(10);

}
