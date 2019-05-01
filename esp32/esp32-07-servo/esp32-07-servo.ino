//test servo
#include "octopusLAB_ROBOT.h"

#include <ESP32_Servo.h>

Servo myservo;  // creates servo object to control a servo
                // Up to 16 servo objects can be created on the ESP32

int pos = 0;    // variable to store the servo position
// Recommended PWM GPIO pins on the ESP32 include 2,4,12-19,21-23,25-27,32-33 
int servoPin = PIN_PWM1;

void setup() {
  myservo.attach(servoPin);   // attaches the servo on pin 18 to the servo object
                              // using default min/max of 1000us and 2000us
                              // different servos may require different min/max settings
                              // for an accurate 0 to 180 sweep
}

void loop() {
  for (pos = 0; pos <= 180; pos += 1) { // goes from 0 degrees to 180 degrees
    // in steps of 1 degree
    myservo.write(pos);              // tell servo to go to position in variable 'pos'
    delay(15);                       // waits 15ms for the servo to reach the position
  }
  for (pos = 180; pos >= 0; pos -= 1) { // goes from 180 degrees to 0 degrees
    myservo.write(pos);              // tell servo to go to position in variable 'pos'
    delay(15);                       // waits 15ms for the servo to reach the position
  }
}
