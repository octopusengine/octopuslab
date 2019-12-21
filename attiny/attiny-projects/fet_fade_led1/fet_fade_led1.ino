/*
attiny-45/85
Octopus engine - oeLAB - 2018/07 TEST (916B)
                Attiny 13/85 
                RST =--U--= VCC         oeLAB dev board1                  
 > pinAn/Rx (A) P3 =     = P2 (A1) (3) i2c 
        /Tx (A) P4 =     = P1 /    (2) >         
               GND =     = P0 /  > (1) i2c Data  
*/

#define LED1_PIN        1  //LED_BUILTIN = Led2 
#define S2_PIN          3  // GRE S2 // GRE 
#define S1_PIN          4  // RED S1 // RED

int ledState = 0;
int button1State = 0;
int button2State = 0; 
int cycle = 0;
int fade_speed = 50 ; //fade_speed delay ms

// the setup function runs once when you press reset or power the board
void setup() {  
  pinMode(LED1_PIN, OUTPUT); // initialize digital pin as an output
  pinMode(S1_PIN, INPUT_PULLUP);
  pinMode(S2_PIN, INPUT_PULLUP);

  fade1(LED1_PIN);
  fade0(LED1_PIN);
}


// the loop function runs over and over again forever
void loop() {
  //*
  button2State = digitalRead(S2_PIN);
  if (button2State == LOW) {
    if (ledState == 0){
        fade1(LED1_PIN);
        digitalWrite(LED1_PIN, HIGH);
        ledState = 1;
        delay(100); 
    }  
    else
    {
        fade0(LED1_PIN);
        digitalWrite(LED1_PIN, LOW);
        ledState = 0;
        delay(100); 
    }
    }
 
  //*/ 
  delay(50);
  //cycle++;
  //if (cycle > 100){
  //  cycle = 0;
  //  fade0(LED1_PIN);
  //  digitalWrite(LED1_PIN, LOW);
  //}
      
}

// --------------------------------------------------
void blink(int pause) {
  digitalWrite(LED1_PIN, HIGH); // turn the LED on (HIGH is the voltage level)
  delay(pause);                 // wait for a second
  digitalWrite(LED1_PIN, LOW);  // turn the LED off by making the voltage LOW
  delay(pause);          
}


//analogWrite(led, brightness);
//brightness = brightness + fadeAmount;
//if (brightness <= 0 || brightness >= 255) {
//  fadeAmount = -fadeAmount;


void fade1(int led) {
  for (uint8_t i = 0; i < 252/3; i++)
  { 
    analogWrite(led, i*3);
    delay(fade_speed);
  }
  analogWrite(led, 255);
}


void fade0(int led) {
  for (uint8_t i = 255/5; i > 0; i--)
  { 
    analogWrite(led, i*5);
    delay(fade_speed);
  }
  analogWrite(led, 0);  
}
