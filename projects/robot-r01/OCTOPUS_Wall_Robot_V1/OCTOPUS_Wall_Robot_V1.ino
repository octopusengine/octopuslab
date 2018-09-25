#include <APDS9930.h>
#include <Adafruit_NeoPixel.h>

#include "octopusLAB_ROBOT.h"

APDS9930 Laser = APDS9930();

int speed_forward = 100;
float kK = 1.0;
float pK;
float dK;
float iD;

//echo
const int TRIG_PIN = PIN_PWM1;
const int ECHO_PIN = PIN_PWM2;

int getEchoDistance() {
  digitalWrite(TRIG_PIN, LOW);  // Clears the TRIG_PIN
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH); // Sets the TRIG_PIN on HIGH state for 10 micro seconds
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);  // Reads the ECHO_PIN, returns the sound wave travel time in microseconds
  long duration = pulseIn(ECHO_PIN, HIGH);
  return duration * 0.034 / 2; // Calculating the distance
}


void setup() {
  Serial.begin(115200); // Starts the serial communication
  pinMode(TRIG_PIN, OUTPUT); // Sets the TRIG_PIN as an Output
  pinMode(ECHO_PIN, INPUT); // Sets the ECHO_PIN as an Input

  neopixelInit();

  Laser.init(); // APDS-9930
  Laser.enableProximitySensor(false); // enable proximity, no interrupt

  initMoto();
}

float error_last = 0;

void loop() {
  int echo = getEchoDistance();
  int laser = Laser.readProximity();

  Serial.print("E: " + String(echo));
  Serial.print(", L: " + String(laser));
  Serial.println();

  float error = calcLaserError(laser);
  int delta = calcSpeedCorrection(error, error_last);
  error_last = error;

  motorLeft(speed_forward - delta);
  motorRight(speed_forward + delta);
  
}
