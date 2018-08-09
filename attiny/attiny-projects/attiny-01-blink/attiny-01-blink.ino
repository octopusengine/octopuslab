/*
attiny-01-blink.ino
Octopus engine - oeLAB - 2018/07 TEST (916B)

                Attiny 13/85 
                RST =--U--= VCC         oeLAB dev board1                  
 > pinAn/Rx (A) P3 =     = P2 (A1) (3) i2c Clock 
        /Tx (A) P4 =     = P1 /    (2) > LED 
               GND =     = P0 /  > (1) i2c Data 
*/
#define LED1_PIN        1  //LED_BUILTIN = Led2            
#define LED2_PIN        3  //

// the setup function runs once when you press reset or power the board
void setup() {  
  pinMode(LED1_PIN, OUTPUT); // initialize digital pin as an output
  pinMode(LED2_PIN, OUTPUT);
}

// the loop function runs over and over again forever
void loop() {
  digitalWrite(LED1_PIN, HIGH);   // turn the LED on (HIGH is the voltage level)
  digitalWrite(LED2_PIN, LOW);
  delay(50);                    // wait for a second
  digitalWrite(LED1_PIN, LOW);    // turn the LED off by making the voltage LOW
  digitalWrite(LED2_PIN, HIGH);
  delay(50);                       
}
