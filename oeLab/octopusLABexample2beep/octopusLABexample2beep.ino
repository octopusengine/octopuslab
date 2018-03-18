#include "octopusLAB.h"

DigitalPin led(OE_LAB_LED);
DigitalPin piezo(OE_LAB_PIEZZO2);

void setup()
{  
}

void loop()
{
  led.SetLow();
  delay(500);
  led.SetHigh();
  
  delay(3000);
  led.FastBlink(7); 
  delay(1000);
  piezo.playMelody2();   
}
