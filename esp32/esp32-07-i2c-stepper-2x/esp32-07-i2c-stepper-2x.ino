//polargraph test - two sepper motors and servo
//octopusLAB - ESP32 ROBOT board (2018/09)

#include <Wire.h>
#include "octopusLAB_ROBOT.h" 

int i2cAddr1 = 0x23;//0x20; //HHH 0x3F/27;//LLL 0x38/20;///?
int i2cAddr2 = 0x27;


int speedTime = 700; //500 ok// 300 už nesíhá
int angle = 3; //360;
int pauseSteps = 200;
int i=0;


//single motor
void rotCV(int  addr,int mot) { //rotacePoSmeru
  step1(addr,mot);
  step2(addr,mot);
  step3(addr,mot);
  step4(addr,mot);
  step5(addr,mot);
  step6(addr,mot);
  step7(addr,mot);
  step8(addr,mot);
}

void rotCCV(int  addr,int mot) { //rotaceProtiSmeru
  step8(addr,mot);
  step7(addr,mot);
  step6(addr,mot);
  step5(addr,mot);
  step4(addr,mot);
  step3(addr,mot);
  step2(addr,mot);
  step1(addr,mot);
}

//two motors
void rotCVCV(int  addr,int mot1, int mot2) { 
  step1(addr,mot1);
  step1(addr,mot2);
  step2(addr,mot1);
  step2(addr,mot2);
  step3(addr,mot1);
  step3(addr,mot2);
  step4(addr,mot1);
  step4(addr,mot2);
  step5(addr,mot1);
  step5(addr,mot2);
  step6(addr,mot1);
  step6(addr,mot2);
  step7(addr,mot1);
  step7(addr,mot2);
  step8(addr,mot1);
  step8(addr,mot2);
}

void rotCVCCV(int  addr,int mot1, int mot2) { 
  step1(addr,mot1);
  step8(addr,mot2);
  step2(addr,mot1);
  step7(addr,mot2);
  step3(addr,mot1);
  step6(addr,mot2);
  step4(addr,mot1);
  step5(addr,mot2);
  step5(addr,mot1);
  step4(addr,mot2);
  step6(addr,mot1);
  step3(addr,mot2);
  step7(addr,mot1);
  step2(addr,mot2);
  step8(addr,mot1);
  step1(addr,mot2);
}

void rotCCVCV(int  addr,int mot1, int mot2) { 
  step8(addr,mot1);
  step1(addr,mot2);
  step7(addr,mot1);
  step2(addr,mot2);
  step6(addr,mot1);
  step3(addr,mot2);
  step5(addr,mot1);
  step4(addr,mot2);
  step4(addr,mot1);
  step5(addr,mot2);
  step3(addr,mot1);
  step6(addr,mot2);
  step2(addr,mot1);
  step7(addr,mot2);
  step1(addr,mot1);
  step8(addr,mot2);
}

void rotCCVCCV(int  addr,int mot1, int mot2) { 
  step8(addr,mot1);
  step8(addr,mot2);
  step7(addr,mot1);
  step7(addr,mot2);
  step6(addr,mot1);
  step6(addr,mot2);
  step5(addr,mot1);
  step5(addr,mot2);
  step4(addr,mot1);
  step4(addr,mot2);
  step3(addr,mot1);
  step3(addr,mot2);
  step2(addr,mot1);
  step2(addr,mot2);
  step1(addr,mot1);
  step1(addr,mot2);
}
//-------------------------------------

void step1(int addr,int mot){
  //digitalWrite(in1, HIGH);
  //digitalWrite(in2, LOW);
  //digitalWrite(in3, LOW);
  //digitalWrite(in4, LOW);
  Wire.beginTransmission(addr);
  if (mot==1) Wire.write(0b0001);
  else Wire.write(0b00010000);
  Wire.endTransmission();
  delayMicroseconds(speedTime);
}

void step2(int addr,int mot){
  //digitalWrite(in1, HIGH);
  //digitalWrite(in2, HIGH);
  //digitalWrite(in3, LOW);
  //digitalWrite(in4, LOW);
  Wire.beginTransmission(addr); 
  if (mot==1) Wire.write(0b0011);
  else Wire.write(0b00110000);
  Wire.endTransmission();
  delayMicroseconds(speedTime);
}
void step3(int addr,int mot){
  //digitalWrite(in1, LOW);
  //digitalWrite(in2, HIGH);
  //digitalWrite(in3, LOW);
  //digitalWrite(in4, LOW);
  Wire.beginTransmission(addr); 
  if (mot==1) Wire.write(0b0010);
  else Wire.write(0b00100000);
  Wire.endTransmission();
  delayMicroseconds(speedTime);
}
void step4(int addr,int mot){
  //digitalWrite(in1, LOW);
  //digitalWrite(in2, HIGH);
  //digitalWrite(in3, HIGH);
  //digitalWrite(in4, LOW);
  Wire.beginTransmission(addr); 
  if (mot==1) Wire.write(0b0110);
  else Wire.write(0b01100000);
  Wire.endTransmission();
  delayMicroseconds(speedTime);
}
void step5(int addr,int mot){
  //digitalWrite(in1, LOW);
  //digitalWrite(in2, LOW);
  //digitalWrite(in3, HIGH);
  //digitalWrite(in4, LOW);
  Wire.beginTransmission(addr); 
  if (mot==1) Wire.write(0b0100);
  else Wire.write(0b01000000);
  Wire.endTransmission();
  delayMicroseconds(speedTime);
}
void step6(int addr,int mot){
  //digitalWrite(in1, LOW);
  //digitalWrite(in2, LOW);
  //digitalWrite(in3, HIGH);
  //digitalWrite(in4, HIGH);
  Wire.beginTransmission(addr); 
  if (mot==1) Wire.write(0b1100);
  else Wire.write(0b11000000);
  Wire.endTransmission();
  delayMicroseconds(speedTime);
}
void step7(int addr,int mot){
  //digitalWrite(in1, LOW);
  //digitalWrite(in2, LOW);
  //digitalWrite(in3, LOW);
  //digitalWrite(in4, HIGH);
  Wire.beginTransmission(addr); 
  if (mot==1) Wire.write(0b1000);
  else Wire.write(0b10000000);
  Wire.endTransmission();
  delayMicroseconds(speedTime);
}
void step8(int addr,int mot){
  //digitalWrite(in1, HIGH);
  //digitalWrite(in2, LOW);
  //digitalWrite(in3, LOW);
  //digitalWrite(in4, HIGH);
  Wire.beginTransmission(addr); 
  if (mot==1) Wire.write(0b1001);
  else Wire.write(0b10010000);
  Wire.endTransmission();
  delayMicroseconds(speedTime);
}


//-------------------------basic movement:
void left(int num){
  for(int i=0;i<(angle*64/45*num);i++)
  {rotCVCV(i2cAddr1,1,2);}
  delay(pauseSteps);
}

void down(int num){
  for(int i=0;i<(angle*64/45*num);i++)
  {rotCCVCV(i2cAddr1,1,2);}
  delay(pauseSteps);
}

void right(int num){
  for(int i=0;i<(angle*64/45*num);i++)
  {rotCCVCCV(i2cAddr1,1,2);}
  delay(pauseSteps);
}

void up(int num){
  for(int i=0;i<(angle*64/45*num);i++)
  {rotCVCCV(i2cAddr1,1,2);}
  delay(pauseSteps);
}

void rup(int num){
  for(int i=0;i<(angle*64/45*num);i++)
  {rotCV(i2cAddr1,1);}
  delay(pauseSteps);
}

void rdown(int num){
  for(int i=0;i<(angle*64/45*num);i++)
  {rotCV(i2cAddr1,2);}
  delay(pauseSteps);
}

void lup(int num){
  for(int i=0;i<(angle*64/45*num);i++)
  {rotCCV(i2cAddr1,2);}
  delay(pauseSteps);
}

void xx(int num){
  for(int i=0;i<(angle*64/45*num);i++)
  {rotCCV(i2cAddr1,1);}
  delay(pauseSteps);
}

//------------------------------/basic

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  Wire.begin();
  Serial.begin(9600);  
  Serial.println("I2C Master ready!");

  int vel = 10;
  for(int i=0;i<8;i++)
  {
  down((6-i)*vel);
  left((6-i)*vel);
  up((6-i)*vel);
  right((6-i)*vel); 
  }  
}


void loop() {
  
  /*left(6);
  up(3);
  rdown(3);
  right(3);
  down(6);
  rup(5);
  lup(3);
  xx(10);
  delay(500);
   */
}
