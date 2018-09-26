#include <APDS9930.h>
#include <Adafruit_NeoPixel.h>

#include "octopusLAB_ROBOT.h"

#define CYCLES_PER_SECOND 200

int speed_forward = 90;
int speed_pidcorrection = 90;

//more in pid file
float kK = 1; //1 - constant of error "quadratic" bending
float pK = 0.75; //0.75 - p constant of pid regulator
float dK = 100; //100-120 - d constant of pid regualtor
float iK = 0; //0 - i constant of pid regulator - in our case non-usable
int n_EMA = 10; //5-10 - the length of sorrection smoothing exponencial moving average

void setup() {
  // the minimal speed depends on CYCLES_PER_SECOND defined
  Serial.begin(230400); 
   //initilize all the robot parts in robot file
  initRobot();
}

//loop global vars
long loop_millis_last = 0;
float error_last = 0;
long echo_detection_millis = 0;

void loop() {

  //you need to press the button for the program to start
  wsSetRed();
  waitForButtonPress();
  wsSetGreen();
  delay(500);

  while (!isButtonPressed()) {

    //for cycle duration purposes
    long microseconds = micros();

    //to keep pid update cycles per second a constant
    while (millis() - loop_millis_last < 1000 / CYCLES_PER_SECOND)
      delayMicroseconds(100);
    loop_millis_last = millis();

    //gets the echo and laser readings
    int echo = updateEcho();
    int laser = getLaserDistance();

    Serial.print("Ech: " + String(echo));
    Serial.print(", Las: " + String(laser));

    //Serial.print(", Btn: " + String(isButtonPressed()));

    //calculates the <-1;1> laser reading error where 
    //0 is 512 laser units reading (wall is a optimal distance from robot)
    //-1 is 0 laser units reading (wall is the closest to the robot)
    //1 is 1024 laser units reading (wall is far away from robot)  
    float error = calcLaserError(laser);

    //calculates the speed correction delta for motors (pid regualtor)
    int delta = calcSpeedCorrection(error, error_last);
    error_last = error;

    Serial.print(", Err: " + String(error));

    int speed_left = 0;
    int speed_right = 0;

    //echo wall in front of logic
    //when echo sees the wall closer than 200 echo units..
    if (echo < 200)
      echo_detection_millis = millis();
      
    //..then try to turn left - and continue to turn left even 
    //50ms after you don't see the wall anymore  
    if (millis() - echo_detection_millis < 50) {
      speed_left = -speed_forward * 1.55;
      speed_right = speed_forward * 1.45;
    }

    //..then for (150 - 50 =) 100ms reduce the pid regulation on half
    else if (millis() - echo_detection_millis < 150) {
      speed_left = speed_forward + delta * 0.5;
      speed_right = speed_forward - delta * 0.5;
    }

    //else if you don't see anything with echo go foward and
    //regulate the direction based on wall laser distance pid regulation
    else {
      speed_left = speed_forward + delta;
      speed_right = speed_forward - delta;
    }

    Serial.print(", Left: " + String(speed_left));
    Serial.print(", Rght: " + String(speed_right));

    //apply the calculated speed to motors (sets the pwm duty cycle for H-bridge)
    motorLeft(speed_left);
    motorRight(speed_right);

    Serial.print(", uS: " + String(micros() - microseconds));

    Serial.println();
  }

  //if the button is pressed stop the motors
  motorLeft(0);
  motorRight(0);
  //and reset
  resetPid();
  //wait for button unpress
  while (isButtonPressed())
    delay(10);

}
