/*
attiny-01-blink.ino
Octopus engine - oeLAB - 2018/07 TEST (484B)
                Attiny 13/85 
                RST =--U--= VCC         oeLAB dev board1                  
 > pinAn/Rx (A) P3 =     = P2 (A1) (3) i2c Clock 
        /Tx (A) P4 =     = P1 /    (2) > LED 
               GND =     = P0 /  > (1) i2c Data 
*/

void setup() {
  DDRB  = 0b00000010;  // port B - signal seup ("1" = output ; "0" = input)
  //PORTB = 0b00001100;  // pull-up fot input
}

void loop()
{
//if ((PINB & 0b00000100) == 0)  
  delay(500); 
  PORTB &= 0b11111101; // only PB1 to LOW 
  delay(500); 
  PORTB |= 0b00000010; // only PB1 to HIGH
}
