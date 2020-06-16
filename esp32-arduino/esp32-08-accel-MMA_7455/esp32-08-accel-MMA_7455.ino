// Uses library MMA_7455.h
// Moritz Kemper, IAD Physical Computing Lab
// moritz.kemper@zhdk.ch
// ZHdK, 03/04/2012
// Released under Creative Commons Licence

#include <Wire.h>
#include <MMA_7455.h> //Include the MMA_7455 library

MMA_7455 mySensor = MMA_7455();

// Convert unsigned char to signed short
union {
  unsigned char ch;
  int8_t sint;
} xVal, yVal, zVal;

void setup()
{
  Serial.begin(115200);

  // Set the sensitivity you want to use
  // 2 = 2g, 4 = 4g, 8 = 8g
  mySensor.initSensitivity(4);
}

// In arduiono IDE you can use "Serial plotter" to visualise data

void loop()
{
  xVal.ch = mySensor.readAxis('x'); //Read out the 'x' Axis
  yVal.ch = mySensor.readAxis('y'); //Read out the 'y' Axis
  zVal.ch = mySensor.readAxis('z'); //Read out the 'z' Axis
  
  Serial.print("X = ");
  Serial.print(xVal.sint, DEC);
  Serial.print("   Y = ");
  Serial.print(yVal.sint, DEC);
  Serial.print("   Z = ");
  Serial.println(zVal.sint, DEC);
  
  delay(10);
}
