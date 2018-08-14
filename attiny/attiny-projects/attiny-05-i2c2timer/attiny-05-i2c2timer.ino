/*
attiny-05-i2c2timer.ino
Octopus engine - oeLAB - 2018/07 TEST

ATtiny85 as an I2C Slave  BroHogan 2011/12
 * Example of ATtiny I2C slave receiving and sending data to an Arduino master.
 * SETUP:
 * NOTE! - It's very important to use pullups on the SDA & SCL lines!
 * http://astromik.org/raspi/i2cmultiplex/attiny_1.ino

                Attiny 85 
                RST =--U--= VCC         oeLAB dev board1                  
 > pinAn/Rx (A) P3 =     = P2 (A1) (3) i2c Clock 
        /Tx (A) P4 =     = P1 /    (2) > LED 
               GND =     = P0 /  > (1) i2c Data 
               
> Arduino UNO serial display TTF 320x240                
*/

#include "TinyWireS.h"                  // wrapper class for I2C slave routines

#define I2C_SLAVE_ADDR  0x52            // i2c slave address 51/52/53 (51hex je 80?)
#define LED1_PIN         1              // ATtiny 
#define LED2_PIN         3              // ATtiny Pin

//--------------------------timers
int num1=0; //timer1
long timerTempTime1;

void handleTimer1(long timerTime) {
 if ((millis() - timerTime)>timerTempTime1)
 {
     timerTempTime1 = millis();
     Blink(LED1_PIN,1); 
     //led.SetLow();
     //delay(50);    
     /*    
      num1++;
     if (num1>9999) num1=0;
     
     //piezo.Beep(20);
     led.SetHigh();*/  
  }
}

void Blink(byte led, byte times){ // poor man's display
  for (byte i=0; i< times; i++){
    digitalWrite(led,HIGH);
    delay (100);
    digitalWrite(led,LOW);
    delay (200);
  }
}

void setup(){
  pinMode(LED1_PIN,OUTPUT);             // for general DEBUG use
  //pinMode(LED2_PIN,OUTPUT);             // for verification
  Blink(LED1_PIN,3);                    // show it's alive
  TinyWireS.begin(I2C_SLAVE_ADDR);      // init I2C Slave mode

  timerTempTime1 = millis();
}

void loop(){
//timer1
  handleTimer1(5000); // 1000=1sec.
  //fast loop
  ///handleFlashButton();
  
  byte byteRcvd = 0;
  if (TinyWireS.available()){           // got I2C input!
    byteRcvd = TinyWireS.receive();     // get the byte from master
    //Blink(LED1_PIN,byteRcvd);           // master must wait for this to finish before calling Wire.requestFrom
    byteRcvd += 10;                     // add 10 to what's received
    TinyWireS.send(byteRcvd);           // send it back to master

    //Blink(LED1_PIN,1);                  // show we transmitted
  }
}
