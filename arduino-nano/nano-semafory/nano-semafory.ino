// the setup function runs once when you press reset or power the board

//green
int G1 = 3; //PWM
int G2 = 4; //
int G3 = 5; //PWM
int G4 = 6; //PWM
int G5 = 7; //
int G6 = 8;
//red
int R1 = 9;  //PWM
int R2 = 10; //PWM
int R3 = 11; //PWM
int R4 = 12; 
int R5 = A0;
int R6 = A1; 

int buttonPin = 2;
const byte interruptPin = 2;
volatile byte state = LOW;

//12/13//PWM

int menu = 0; //default

//int led = 9;           // the PWM pin the LED is attached to
int brightness = 0;    // how bright the LED is
int fadeAmount = 5;    // how many points to fade the LED by

void blink1(int led,int lightTime) {
  digitalWrite(led, HIGH);
  delay(lightTime); 
  digitalWrite(led, LOW); 
}

void blink2(int led1,int led2,int lightTime) {
  digitalWrite(led1, HIGH);
  digitalWrite(led2, HIGH);
  delay(lightTime); 
  digitalWrite(led1, LOW); 
  digitalWrite(led2, LOW); 
}

void fade1(int led,int lightTime) {
  //analogWrite(led, brightness);
  //brightness = brightness + fadeAmount;
  //if (brightness <= 0 || brightness >= 255) {
  //  fadeAmount = -fadeAmount;
  for (uint8_t i = 0; i < 255/5; i++)
  { 
    analogWrite(led, i*5);
    delay(30);
  }
  analogWrite(led, 255); 
  delay(lightTime);
  for (uint8_t i = 255/5; i > 0; i--)
  { 
    analogWrite(led, i*5);
    delay(30);
  }
  analogWrite(led, 0);  
}

void test_fade(int tim)
{
  fade1(G1,tim);  
  fade1(G2,tim);
  fade1(G3,tim); 
  fade1(G4,tim); 
  fade1(G5,tim); 
  fade1(G6,tim);    
}

void test_blinkG(int bt)
{
  blink1(G1,bt);
  blink1(G2,bt);
  blink1(G3,bt);
  blink1(G4,bt);
  blink1(G5,bt);
  blink1(G6,bt);
}

void test_blinkR(int bt)
{
  blink1(R1,bt);
  blink1(R2,bt);
  blink1(R3,bt);
  blink1(R4,bt);
  blink1(R5,bt);
  blink1(R6,bt);
}

void test_blinkRG(int bt)
{
  blink2(R1,G1,bt);
  blink2(R2,G2,bt);
  blink2(R3,G3,bt);
  blink2(R4,G4,bt);
  blink2(R5,G5,bt);
  blink2(R6,G6,bt);
}

void test1(){

  for (uint8_t i = 0; i < 3; i++)
  {
  digitalWrite(LED_BUILTIN, HIGH);   
  digitalWrite(G1, HIGH); 
  digitalWrite(G2, LOW);
  digitalWrite(R1, HIGH);    
  delay(500);                       
  digitalWrite(LED_BUILTIN, LOW);
  digitalWrite(G1, LOW);   
  digitalWrite(G2, HIGH);
  digitalWrite(R1, LOW);     
  delay(500); 
  digitalWrite(G1, HIGH); 
  digitalWrite(G2, LOW);
  digitalWrite(G3, HIGH);    
  delay(500);
  digitalWrite(G3, LOW);    
  }
for (uint8_t i = 0; i < 30; i++)
  {
  digitalWrite(LED_BUILTIN, HIGH);   
  digitalWrite(G1, HIGH); 
  digitalWrite(G2, LOW);    
  delay(100);                       
  digitalWrite(LED_BUILTIN, LOW);
  digitalWrite(G1, LOW);   
  digitalWrite(G2, HIGH);     
  delay(100); 
  }

for (int i = 0; i < 500; i++)
  {
  digitalWrite(LED_BUILTIN, HIGH);   
  digitalWrite(G1, HIGH); 
  digitalWrite(G2, LOW);    
  delay(2);                       
  digitalWrite(LED_BUILTIN, LOW);
  digitalWrite(G1, LOW);   
  digitalWrite(G2, HIGH);     
  delay(2); 
  }  
}

int simpleReadButt(){
  //buttonState
  if (digitalRead(buttonPin) == LOW) {
    Serial.println("but1");
    delay(10);
    if (digitalRead(buttonPin) == LOW)
          {
            menu = menu+1;
            if (menu>3){menu = 0;}
          }
    } else {
      Serial.println("but0");
    }
  }

void myInt()
{
 static unsigned long last_interrupt_time = 0;
 unsigned long interrupt_time = millis();
 // If interrupts come faster than 200ms, assume it's a bounce and ignore
 if (interrupt_time - last_interrupt_time > 200)
 {
   doButtInt();
 }
 last_interrupt_time = interrupt_time;  
}

int doButtInt(){
    Serial.println("but_interupt");
    delay(100); 
    menu = menu+1;
    if (menu>3){menu = 0;} 
    Serial.println(menu);
    delay(1000);         
}  
//-----------------------

void setup() {
  Serial.begin(9600);
  Serial.println("Start simple LED driwer test");
  //pinMode(buttonPin, INPUT_PULLUP);
  pinMode(interruptPin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(interruptPin), myInt, FALLING); //CHANGE
  
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(G1, OUTPUT);
  pinMode(G2, OUTPUT);
  pinMode(G3, OUTPUT);
  pinMode(G4, OUTPUT);
  pinMode(G5, OUTPUT);
  pinMode(G6, OUTPUT);
  pinMode(R1, OUTPUT);
  pinMode(R2, OUTPUT);
  pinMode(R3, OUTPUT);
  pinMode(R4, OUTPUT);
  pinMode(R5, OUTPUT);
  pinMode(R6, OUTPUT);
}

// the loop function runs over and over again forever

void loop() {
  //menu = simpleReadButt();
  Serial.print("loop menu:");
  Serial.println(menu);

  if (menu == 0 ){
    Serial.println("test1");
    for (int i = 0; i < 800; i++)
    {  
    test_blinkRG(1);
    }
  }
 
if (menu == 1 ){ 
  
  test_blinkG(300);
  test_blinkR(300); 
}

if (menu == 2 ){   
  test_fade(1000);
}

if (menu == 3 ){   
  int number12 = random(0, 11)+1;
  Serial.print("loop rnd:");
  Serial.println(number12);
}

delay(2000);
                      
}
