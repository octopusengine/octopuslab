// octopusLAB - arduino NANO / UNIboard / ULN LED driver
// 7.1.2019 - ok - first patterns
// MIT (c) Jan Copak

//ULN1
#define G1 3 //PWM
#define G2 4 //
#define G3 5 //PWM
#define G4 6 //PWM
#define G5 7 //
#define G6 8
//ULN2
#define R1 9  //PWM
#define R2 10 //PWM
#define R3 11 //PWM
#define R4 12 
#define R5 A0
#define R6 A1

const byte pins[] = {
  G1, G2, G3, G4, G5, G6,
  R1, R2, R3, R4, R5, R6
}; 

const byte pinsR[] = {
  G1, G3, G5,
  R1, R3, R5
}; 

const byte pinsG[] = {
  G2, G4, G6,
  R2, R4, R6
}; 

const byte interruptPin = 2;

int menu = 1; //default

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

void blink_allG(int bt)
{
for (int i = 0; i < 6; i++) 
    {        
          blink1(pinsG[i],bt);
    }
}

void blink_allR(int bt)
{
for (int i = 0; i < 6; i++) 
    {        
          blink1(pinsR[i],bt);
    }
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

void ligtMultiAll(int tim){
  Serial.println("> ligtMultiAll");
  for (int i = 0; i < tim; i++) //800 cca 1-2sec
    {    test_blinkRG(1);    }
}

void ligtMultiR(int tim){
  Serial.println("> ligtMultiR");
  for (int i = 0; i < tim; i++) //800 cca 1-2sec
    {    blink_allR(1);    }
}

void ligtMultiG(int tim){
  Serial.println("> ligtMultiG");
  for (int i = 0; i < tim; i++) //800 cca 1-2sec
    {    blink_allG(1);    }
}

void sw_fade(int led,int lightTime) {
  int maxi = 300;
  int multH = 5;
  int multL = 20;
  for (int i = 1; i < maxi; i++)
  {
      digitalWrite(led, HIGH);
      delayMicroseconds(i*multH); 
      digitalWrite(led, LOW); 
      delayMicroseconds((maxi-i)*multL); 
  }
  digitalWrite(led, HIGH);
  delay(lightTime); 
  digitalWrite(led, LOW);
  for (int i = 1; i < maxi; i++)
  {
      digitalWrite(led, HIGH);
      delayMicroseconds((maxi-i)*multH); 
      digitalWrite(led, LOW); 
      delayMicroseconds(i*multL); 
  }  
}

//----------butt int
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
    Serial.print("butt_interupt > ");
    delay(100); 
    menu = menu+1;
    if (menu>3){menu = 1;} 
    Serial.println(menu);
    
    delay(500);
    sw_fade(pins[menu-1],1000);
    delay(500);
    sw_fade(pins[menu-1],1000); 
    delay(500);
    sw_fade(pins[menu-1],1000); 
    delay(1000);          
}  
//---------------------------------------------------------------- ==================

void setup() {
  Serial.begin(9600);
  Serial.println("----- Simple LED driwer < Arduino Nano, ULN, UNIboard -----");
  
  Serial.println("Setup interrupt");
  pinMode(interruptPin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(interruptPin), myInt, FALLING); //CHANGE

  Serial.print("Setup PINS: ");
  pinMode(LED_BUILTIN, OUTPUT);
  for (int i = 0; i < 12; i++) 
    {     pinMode(pins[i], OUTPUT);   
          Serial.print(i, pins[i]);
    }
  Serial.println();  
}

void loop() {   // the loop function runs over and over again forever =============== 
if (menu == 1 ){ 
  Serial.println("go-menu1");
  blink1(LED_BUILTIN,500); 
  ligtMultiAll(1500);  
  ligtMultiR(1500);
  ligtMultiG(1500);        
}

if (menu == 2 ){ 
  Serial.println("go-menu2"); 
  blink1(LED_BUILTIN,200);  delay(200);
  blink1(LED_BUILTIN,200);  
 
  int number12 = random(0, 11); //0,11=all
  Serial.print("> loop rnd:");
  Serial.println(number12);
  sw_fade(pins[number12],3500);
}

if (menu == 3 ){ 
  Serial.println("go-menu3"); 
  blink1(LED_BUILTIN,150);delay(200);
  blink1(LED_BUILTIN,150);delay(200);
  blink1(LED_BUILTIN,150);

  Serial.println("> blink all R / G"); 
  blink_allG(1500);
  blink_allR(1500);
  delay(1000);
 }                     
}
