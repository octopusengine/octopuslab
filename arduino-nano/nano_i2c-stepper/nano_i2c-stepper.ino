#include <Wire.h>

int i2cAddr = 0x20;//0x20; //HHH 0x3F/27;//LLL 0x38/20;///?

int i=0;
int speedTime = 500; //300 už nesíhá
int angle = 360;


void rotCV() { //rotacePoSmeru
  step2();
  step3();
  step4();
  step5();
  step6();
  step7();
  step8();
}

void rotCCV() { //rotaceProtiSmeru
  step8();
  step7();
  step6();
  step5();
  step4();
  step3();
  step2();
  step1();
}

void step1(){
  //digitalWrite(in1, HIGH);
  //digitalWrite(in2, LOW);
  //digitalWrite(in3, LOW);
  //digitalWrite(in4, LOW);
  Wire.beginTransmission(i2cAddr); 
  Wire.write(0b0001);
  Wire.endTransmission();
  delayMicroseconds(speedTime);
}

void step2(){
  //digitalWrite(in1, HIGH);
  //digitalWrite(in2, HIGH);
  //digitalWrite(in3, LOW);
  //digitalWrite(in4, LOW);
  Wire.beginTransmission(i2cAddr); 
  Wire.write(0b0011);
  Wire.endTransmission();
  delayMicroseconds(speedTime);
}
void step3(){
  //digitalWrite(in1, LOW);
  //digitalWrite(in2, HIGH);
  //digitalWrite(in3, LOW);
  //digitalWrite(in4, LOW);
  Wire.beginTransmission(i2cAddr); 
  Wire.write(0b0010);
  Wire.endTransmission();
  delayMicroseconds(speedTime);
}
void step4(){
  //digitalWrite(in1, LOW);
  //digitalWrite(in2, HIGH);
  //digitalWrite(in3, HIGH);
  //digitalWrite(in4, LOW);
  Wire.beginTransmission(i2cAddr); 
  Wire.write(0b0110);
  Wire.endTransmission();
  delayMicroseconds(speedTime);
}
void step5(){
  //digitalWrite(in1, LOW);
  //digitalWrite(in2, LOW);
  //digitalWrite(in3, HIGH);
  //digitalWrite(in4, LOW);
  Wire.beginTransmission(i2cAddr); 
  Wire.write(0b0100);
  Wire.endTransmission();
  delayMicroseconds(speedTime);
}
void step6(){
  //digitalWrite(in1, LOW);
  //digitalWrite(in2, LOW);
  //digitalWrite(in3, HIGH);
  //digitalWrite(in4, HIGH);
  Wire.beginTransmission(i2cAddr); 
  Wire.write(0b1100);
  Wire.endTransmission();
  delayMicroseconds(speedTime);
}
void step7(){
  //digitalWrite(in1, LOW);
  //digitalWrite(in2, LOW);
  //digitalWrite(in3, LOW);
  //digitalWrite(in4, HIGH);
  Wire.beginTransmission(i2cAddr); 
  Wire.write(0b1000);
  Wire.endTransmission();
  delayMicroseconds(speedTime);
}
void step8(){
  //digitalWrite(in1, HIGH);
  //digitalWrite(in2, LOW);
  //digitalWrite(in3, LOW);
  //digitalWrite(in4, HIGH);
  Wire.beginTransmission(i2cAddr); 
  Wire.write(0b1001);
  Wire.endTransmission();
  delayMicroseconds(speedTime);
}


void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  Wire.begin();
  Serial.begin(9600);  
  Serial.println("I2C Master ready!");
}


void loop() { 
  digitalWrite(LED_BUILTIN, HIGH);  
  
  //test "sweep"
  speedTime = 500;
  for(int i=0;i<(angle*64/45);i++){
    rotacePoSmeru();
  }
  delay(1000);
 
  digitalWrite(LED_BUILTIN, LOW);

  for(int i=0;i<(angle*64/45);i++){
    rotCCV();
  } 
  delay(1000);

  speedTime = 750;
  for(int i=0;i<(angle*64/45);i++){
    rotCV();
  }
  delay(1000);
 
  digitalWrite(LED_BUILTIN, LOW);

  for(int i=0;i<(angle*64/45);i++){
    rotCCV();
  } 
  delay(1000);

  speedTime = 1000;
  for(int i=0;i<(angle*64/45);i++){
    rotCV();
  }
  delay(1000);
 
  digitalWrite(LED_BUILTIN, LOW);

  for(int i=0;i<(angle*64/45);i++){
    rotaceProtiSmeru();
  } 
  delay(1000);
}


