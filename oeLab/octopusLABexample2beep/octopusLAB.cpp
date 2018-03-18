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

void DigitalPin::BeepNote1(void)
{
       int noteDuration = 50;
       tone(_pin, NOTE_C6, noteDuration);
       int pauseBetweenNotes = noteDuration * 1.30;
       delay(pauseBetweenNotes);
       noTone(_pin);
}

void DigitalPin::BeepNote2(void)
{
       int noteDuration = 100;
       tone(_pin, NOTE_E6, noteDuration);
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

//----------------------------melody1--------------------
int melody1[] = {  NOTE_C5, NOTE_G4, NOTE_G4, NOTE_A4, NOTE_G4, 0};
int noteDurations1[] = {4, 8, 8, 4, 4, 4};

void DigitalPin::playMelody1(void)
{
for (int thisNote = 0; thisNote < 8; thisNote++) {

    // to calculate the note duration, take one second divided by the note type.
    //e.g. quarter note = 1000 / 4, eighth note = 1000/8, etc.
    int noteDuration = 1000 / noteDurations1[thisNote];
    tone(_pin, melody1[thisNote], noteDuration);

    // to distinguish the notes, set a minimum time between them.
    // the note's duration + 30% seems to work well:
    int pauseBetweenNotes = noteDuration * 1.30;
    delay(pauseBetweenNotes);
    // stop the tone playing:
    noTone(_pin);
   }
}
//--------------------------/melody1-------------------------

//---------------------------melody2--------------------
int melody2[] = {  NOTE_C5, NOTE_E5, NOTE_G5, NOTE_A4, NOTE_G4, 0};
int noteDurations2[] = {8, 8, 8, 4, 4, 4};

void DigitalPin::playMelody2(void)
{
for (int thisNote = 0; thisNote < 8; thisNote++) {
    int noteDuration = 1000 / noteDurations2[thisNote];
    tone(_pin, melody2[thisNote], noteDuration);
    int pauseBetweenNotes = noteDuration * 1.30;
    delay(pauseBetweenNotes);
    noTone(_pin);
   }
}
//--------------------------/melody2-------------------------



//https://www.arduino.cc/en/Hacking/LibraryTutorial
