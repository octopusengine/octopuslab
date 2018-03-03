/*
  octopusLAB.h - Library for interface NodeMcu octopus Board.
  Created by Yenda (Honza S. Copak - 2017/18)
  Released into the public domain.
*/

#include "Arduino.h"
#include "octopusLAB.h"

//#define FLASH_BUTTON 0


DigitalPin::DigitalPin(int pin)
{
  pinMode(pin, OUTPUT);
  _pin = pin;
}

void DigitalPin::SetOn()
{
  digitalWrite(_pin, HIGH);    
}

void DigitalPin::SetOff()
{
  digitalWrite(_pin, LOW);
}

void DigitalPin::SetHigh()
{
  digitalWrite(_pin, HIGH);    
}

void DigitalPin::SetLow()
{
  digitalWrite(_pin, LOW);
}

void DigitalPin::FastBlink(int num)
{
  int i;
  for (i=0; i<num; i++)
  {
    digitalWrite(_pin, LOW);
    delay(20);
    digitalWrite(_pin, HIGH);
    delay(100);    
  }
  digitalWrite(_pin, HIGH);
}

void DigitalPin::Beep(int delayTime)
{
  digitalWrite(_pin, HIGH);
  delay(delayTime);
  digitalWrite(_pin, LOW);
}

void DigitalPin::BeepNote(void)
{
       int noteDuration = 1000 / 300;
       tone(_pin, NOTE_C6, noteDuration);
       int pauseBetweenNotes = noteDuration * 1.30;
       delay(pauseBetweenNotes);
       noTone(_pin);
}

//---------------------
Morse::Morse(int pin)
{
  pinMode(pin, OUTPUT);
  _pin = pin;
}

void Morse::dot()
{
  digitalWrite(_pin, HIGH);
  delay(250);
  digitalWrite(_pin, LOW);
  delay(250);  
}

void Morse::dash()
{
  digitalWrite(_pin, HIGH);
  delay(1000);
  digitalWrite(_pin, LOW);
  delay(250);
}

//https://www.arduino.cc/en/Hacking/LibraryTutorial
