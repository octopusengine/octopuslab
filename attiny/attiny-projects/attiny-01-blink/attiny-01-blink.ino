/*
Octopus engine - lab - 2018/07 TEST

           Attiny 13/85 
           RST =--U--= VCC                  oeLAB dev board1                  
 > pinAn (A)P3 =     = P2 (A1) pinDall      (3) i2c Clock 
 Strobe2 (A)P4 =     = P1 / pinRX           (2) > LED 
           GND =     = P0 / pinTX >         (1) i2c Data 
*/

int ledR = 1;
int ledB = 3;

// the setup function runs once when you press reset or power the board
void setup() {
  // initialize digital pin LED_BUILTIN as an output.
  pinMode(ledR, OUTPUT); //LED_BUILTIN
  pinMode(ledB, OUTPUT);
}

// the loop function runs over and over again forever
void loop() {
  digitalWrite(ledR, HIGH);   // turn the LED on (HIGH is the voltage level)
  digitalWrite(ledB, LOW);
  delay(1000);                       // wait for a second
  digitalWrite(ledR, LOW);    // turn the LED off by making the voltage LOW
  digitalWrite(ledB, HIGH);
  delay(1000);                       // wait for a second
}
