#include "octopusLAB_ROBOT.h"

/*
ukazka zapojeni OctopusLab ROBOT Boardu se 4 fazovym krokovym motorem (28BYJ-48)
*/

int stepTimeMicroSeconds = 1100; //cca mene nez 1000 se motor neroztoci

//nastaveni pinu pro 4-fazovy korokovy motor
int in1 = PIN_PWM1;
int in2 = PIN_PWM2;
int in3 = PIN_PWM3;
int in4 = PIN_WS;


void rotConterClockwise(int stepTimeMicroSeconds) { //rotace protismeru hodin, blokujici
  step1();
  delayMicroseconds(stepTimeMicroSeconds);
  step2();
  delayMicroseconds(stepTimeMicroSeconds);
  step3();
  delayMicroseconds(stepTimeMicroSeconds);
  step4();
  delayMicroseconds(stepTimeMicroSeconds);
  step5();
  delayMicroseconds(stepTimeMicroSeconds);
  step6();
  delayMicroseconds(stepTimeMicroSeconds);
  step7();
  delayMicroseconds(stepTimeMicroSeconds);
  step8();
  delayMicroseconds(stepTimeMicroSeconds);
}

void rotClockwise() { //rotace po smeru hodin, blokujici
  step8();
  delayMicroseconds(stepTimeMicroSeconds);
  step7();
  delayMicroseconds(stepTimeMicroSeconds);
  step6();
  delayMicroseconds(stepTimeMicroSeconds);
  step5();
  delayMicroseconds(stepTimeMicroSeconds);
  step4();
  delayMicroseconds(stepTimeMicroSeconds);
  step3();
  delayMicroseconds(stepTimeMicroSeconds);
  step2();
  delayMicroseconds(stepTimeMicroSeconds);
  step1();
  delayMicroseconds(stepTimeMicroSeconds);
}

void step1() {
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
  digitalWrite(in3, LOW);
  digitalWrite(in4, LOW);
}

void step2() {
  digitalWrite(in1, HIGH);
  digitalWrite(in2, HIGH);
  digitalWrite(in3, LOW);
  digitalWrite(in4, LOW);
}
void step3() {
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
  digitalWrite(in3, LOW);
  digitalWrite(in4, LOW);
}
void step4() {
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
  digitalWrite(in3, HIGH);
  digitalWrite(in4, LOW);
}
void step5() {
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
  digitalWrite(in3, HIGH);
  digitalWrite(in4, LOW);
}
void step6() {
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
  digitalWrite(in3, HIGH);
  digitalWrite(in4, HIGH);
}
void step7() {
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
  digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH);
}
void step8() {
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
  digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH);
}

// udela krok podle stepIndex 1 az 8
void rotStepClockwise(int stepIndex) {
  switch (stepIndex) {
    case 1 :
      step8();
      break;
    case 2 :
      step7();
      break;
    case 3 :
      step6();
      break;
    case 4 :
      step5();
      break;
    case 5 :
      step4();
      break;
    case 6 :
      step3();
      break;
    case 7 :
      step2();
      break;
    case 8 :
      step1();
      break;
  }
}

void setup() {
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);
}

// projde vsechny kroky po smeru hodin
void rotClockwiseAllStepsBlocking(int stepTimeMicroSeconds) {
  for (int i = 1; i < 9; i++) {
    rotStepClockwise(i);
    delayMicroseconds(stepTimeMicroSeconds);
  }
}

void loop() {
  for(int i = 0; i < 64 * 8; i++){
      rotClockwiseAllStepsBlocking(stepTimeMicroSeconds);
  }
  
  delay(1000);
}
