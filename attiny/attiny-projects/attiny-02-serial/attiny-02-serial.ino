/*
attiny-02-serial.ino
Octopus engine - oeLAB - 2018/07 TEST
                Attiny 13/85 
                RST =--U--= VCC         oeLAB dev board1                  
 > pinAn/Rx (A) P3 =     = P2 (A1) (3) i2c Clock 
        /Tx (A) P4 =     = P1 /    (2) > LED 
               GND =     = P0 /  > (1) i2c Data 
               
> Arduino UNO serial display TTF 320x240                
*/

#include <SoftwareSerial.h>

#define RX    3   // *** D3
#define TX    4   // *** D4
SoftwareSerial TSerial(RX, TX); //TSerial for Attiny

#define LED1_PIN        1              
#define LED2_PIN        3  

void setup() {
  // initialize digital pin LED_BUILTIN as an output.
  pinMode(LED1_PIN, OUTPUT); //LED_BUILTIN
  //pinMode(ledB, OUTPUT);
  //digitalWrite(ledB, LOW);
  
   delay(5000); //waiting for serial display init
   TSerial.begin(9600);
   //communication with serial monitor:
   TSerial.println("C"); //clear display
   delay(50);
   
   TSerial.print("W7");  //change color
   TSerial.print("h");   //horizontal line
   TSerial.print(10);    //set y position 
   delay(20);
   TSerial.print("h");   //horizontal line
   TSerial.print(180);   //set y position
   delay(20);
   TSerial.print("R1QAttiny - serial display*");
   TSerial.print("R9Qoctopusengine.org*");
   delay(20);
 
   TSerial.print("R5W1R5Q...*");   
}

int cnt = 0;
// the loop function runs over and over again forever
void loop() {
  digitalWrite(LED1_PIN, HIGH);   // turn the LED on (HIGH is the voltage level)
  //digitalWrite(ledB, LOW);
  delay(200);                       // wait for a second
  digitalWrite(LED1_PIN, LOW);    // turn the LED off by making the voltage LOW
  //digitalWrite(ledB, HIGH);
  delay(300);                      // wait for a second

  TSerial.print("Q");
  TSerial.print(String(cnt));
  TSerial.print("*");

  cnt++;
}
