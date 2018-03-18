#include "octopusLAB.h"

DigitalPin led(OE_LAB_LED);
DigitalPin piezo(OE_LAB_PIEZZO2);
//Morse morse(2);

void setup()
{
  /*morse.dot(); morse.dot(); morse.dot();
  morse.dash(); morse.dash(); morse.dash();
  morse.dot(); morse.dot(); morse.dot();
  */
  //test kHz
  //piezo.Beep(100);
  //delay(200);
  ///ok piezo.playMelody1();  
}

void loop()
{
  led.SetLow();
  //piezo.Beep(20);
  delay(500);
  led.SetHigh();
  
  delay(3000);
  led.FastBlink(7); //test signal alert
  delay(1000);
  //piezo.BeepNote1(); //test - need PWM!
  // delay(1000);
  //piezo.BeepNote2();
   piezo.playMelody2();  
  
}
