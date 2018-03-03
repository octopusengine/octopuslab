#include "octopusLAB.h"

DigitalPin led(OE_LAB_LED);
DigitalPin piezzo(OE_LAB_PIEZZO);
//Morse morse(2);

void setup()
{
  /*morse.dot(); morse.dot(); morse.dot();
  morse.dash(); morse.dash(); morse.dash();
  morse.dot(); morse.dot(); morse.dot();
  */
}

void loop()
{
  led.SetLow();
  piezzo.Beep(20);
  delay(500);
  led.SetHigh();
  
  delay(3000);
  led.FastBlink(7); //test signal alert
  delay(2000);
  piezzo.BeepNote(); //test - need PWM!
}
