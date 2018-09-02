#include <Wire.h>

int i2cAddr = 0x20;//0x20; //HHH 0x3F/27;//LLL 0x38/20;///?
int i=0;

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  Wire.begin();
  Serial.begin(9600);  
  Serial.println("I2C Master ready!");
}

void loop() { 
  digitalWrite(LED_BUILTIN, HIGH);  
  /*delay(50);
  Serial.println("Write data");
  Wire.beginTransmission(i2cAddr);
  Wire.write(0);
  Wire.endTransmission();
  Serial.println("Receive data");
  Wire.requestFrom(i2cAddr,3);
  String response = "";
  while (Wire.available()) {
      char b = Wire.read();
      response += b;
  }
  Serial.println(response);
  */
 
  Wire.beginTransmission(0x20); 
  Wire.write(i++ ^ 0xFF);
  Wire.endTransmission();

  delay(300);
  Serial.println(i);
  if (i>255) {i=0;}
  
  digitalWrite(LED_BUILTIN, LOW);
  delay(300);
}


