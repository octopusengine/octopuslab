// Házecí kostka

#define off    true
#define on     false

#define Time   2000

#define one  0
#define two    1
#define four  2
#define six   4

#define button 3
#define PULLUP 8

int combination;
unsigned long ButtonTime = 0; //Čas posledního stisknutí
unsigned long TempTime = 0; // Čas posledního hodu

void setup() {
  // put your setup code here, to run once:
  pinMode(one,  OUTPUT);
  pinMode(two,  OUTPUT);
  pinMode(four, OUTPUT);
  pinMode(six,  OUTPUT);
  //DDRB  = 0b00010111;  // outputs on port B ("1" = out ; "0" = in)
  //PORTB = 0b00001000;  // 
  pinMode(button, INPUT_PULLUP);
  combination = 17;
}

void loop() {
  // put your main code here, to run repeatedly:

//if (NextTime (TempTime, Time)) {
//  TempTime = millis();

  //combination += 1;
  //if (combination > 6)
  //  combination = 0;

  //PINB
//if (PINB & 0b00001000 == false) {
if (digitalRead(button) == false) {
  combination += 1;
  if (combination > 6)
    combination = 0;
  delay(500);
}

//}  //if

switch (combination) {
    case 1:
    case 2:
      //do something
      PORTB = ~(combination);// + PULLUP;
      break;
    case 3:
    case 4:
    case 5:
      //do something
      PORTB = ~(combination + 2);// + PULLUP;
      break;
    case 6:
      //do something
      PORTB = ~(combination + 16);// + PULLUP;
      break;
    case 17:
      //do something
      PORTB = ~(combination);// + PULLUP;
      break;
    default:
      // if nothing else matches, do the default
      PORTB = 63; // all off
      // default is optional
    break;
  }

}

bool NextTime(unsigned long LastAction, unsigned long Pause){
  unsigned long ActualTime = millis();
  unsigned long EndTime = LastAction + Pause;  
  if (LastAction <= EndTime){
    if (ActualTime < LastAction or EndTime < ActualTime) return true; else return false; // při nepřetečení při výpočtu EndTime
  } else {
    if (ActualTime < LastAction and EndTime < ActualTime) return true; else return false; // při přetečení při výpočtu EndTime
  }
}
