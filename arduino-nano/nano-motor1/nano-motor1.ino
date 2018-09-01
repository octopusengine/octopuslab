#define LED1_PIN 11
#define LED2_PIN 12

int pause=1000;

//the setup function runs once when you press reset or power the board
void setup() {
  // initialize digital pin LED_BUILTIN as an output.
  //directions: L293D
  pinMode(LED1_PIN, OUTPUT);
  pinMode(LED2_PIN, OUTPUT);
}

//the loop function runs over and over again forever
void loop() {
  //cw
  digitalWrite(LED1_PIN, HIGH);   
  delay(pause);                       
  digitalWrite(LED1_PIN, LOW);    
  delay(pause);                       

  //ccw
  digitalWrite(LED2_PIN, HIGH);   
  delay(pause);                       
  digitalWrite(LED2_PIN, LOW);    
  delay(pause);                       
}
