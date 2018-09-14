// I2C Scanner

#include <Wire.h>

void setup() {
  Serial.begin (115200);

  Wire.begin();
}

void loop() {
  byte count = 0;

  Serial.println ();
  Serial.println ("I2C scanner. Scanning ...");
  for (byte i = 8; i < 120; i++)
  {
    Wire.beginTransmission (i);
    if (Wire.endTransmission () == 0)
    {
      Serial.print ("Found address: ");
      Serial.print (i, DEC);
      Serial.print (" (0x");
      Serial.print (i, HEX);
      Serial.println (")");
      count++;
      delay (1);
    } 
  } 
  Serial.println ("Done.");
  Serial.print ("Found ");
  Serial.print (count, DEC);
  Serial.println (" device(s).");

  delay(1000);
}
