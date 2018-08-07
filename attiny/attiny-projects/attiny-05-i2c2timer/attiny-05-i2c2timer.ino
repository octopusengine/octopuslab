/* ATtiny85 as an I2C Slave            BroHogan                           1/12/11
 * Example of ATtiny I2C slave receiving and sending data to an Arduino master.
 * Gets data from master, adds 10 to it and sends it back.
 * SETUP:
 * ATtiny Pin 1 = (RESET) N/U                      ATtiny Pin 2 = (D3) N/U
 * ATtiny Pin 3 = (D4) to LED1                     ATtiny Pin 4 = GND
 * ATtiny Pin 5 = I2C SDA on DS1621  & GPIO        ATtiny Pin 6 = (D1) to LED2
 * ATtiny Pin 7 = I2C SCK on DS1621  & GPIO        ATtiny Pin 8 = VCC (2.7-5.5V)
 * NOTE! - It's very important to use pullups on the SDA & SCL lines!
 * Current Rx & Tx buffers set at 32 bytes - see usiTwiSlave.h
 * Credit and thanks to Don Blake for his usiTwiSlave code.
 * More on TinyWireS usage - see TinyWireS.h
 */
//http://astromik.org/raspi/i2cmultiplex/attiny_1.ino
//
/*
    Attiny 13/85 
           RST =--U--= VCC                  oeLAB dev board1                  
 > pinAn (A)P3 =     = P2 (A1) pinDall      (3) i2c Clock 
 Strobe2 (A)P4 =     = P1 / pinRX           (2) > LED 
           GND =     = P0 / pinTX >         (1) i2c Data 

 */

#include "TinyWireS.h"                  // wrapper class for I2C slave routines

#define I2C_SLAVE_ADDR  0x52            // i2c slave address 51/52/53 (51hex je 80?)
#define LED1_PIN         1              // ATtiny 
#define LED2_PIN         3              // ATtiny Pin


//--------------------------timers
int num1=0; //timer1
int timerTempTime1;

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

/*
//==============================================================
//======================= BUTTON FLASH =========================
//==============================================================
int flashButtonPressedTime = 0;
bool flashButtonDown = false;

void handleFlashButton() {
  if (!digitalRead(FLASH_BUTTON) and !flashButtonDown) {
    Serial.println(F("FLASH Pressed"));
    flashButtonPressedTime = millis();
    flashButtonDown = true;

    octopusDisplay(6,"butt");

    piezo.Beep(100);
    delay(100);
  }

  if (digitalRead(FLASH_BUTTON) and flashButtonDown) {
    flashButtonDown = false;
    Serial.print(F("Flash button holded for "));
    Serial.print(millis() - flashButtonPressedTime);
    Serial.println(F(" ms"));
    processFlashButton(millis() - flashButtonPressedTime);
  }

  if (!digitalRead(FLASH_BUTTON) and flashButtonDown) {
    //lmd.setDigit(7, alpha['f' - 'a']);
    //display((millis() - flashButtonPressedTime) / 100, -1);
  }
}

void processFlashButton(int pressedTime) {
  // 50ms - 200ms sec - rotate coin
  if (pressedTime > 50 and pressedTime < 200) {
    //next_page();
    Serial.println(F("Next page"));
  }

  // 200ms - 1 sec - Show IP
  if (pressedTime > 200 and pressedTime < 1000) {
    Serial.println(F("Network information"));
  }

  // 1.5 - 3 sec - OTA Activate
  if (pressedTime > 1500 and pressedTime < 3000) {
    //start_update_web_ota();
  }

  // 5 - 10 sec - Reset wifi settings
  if (pressedTime > 5000 and pressedTime < 10000) {
    Serial.print(F("Reset wifi settings"));
    //display_text(F("wifi rst"));
    //wifiManager.resetSettings();
    //delay(1000);
    //ESP.reset();
  }
}
*/

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


