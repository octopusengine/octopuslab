
// PIN as on octopusLAB ESP32 RobotBoard
#define MOTO_12EN 25
#define MOTO_34EN 15
#define MOTO1A 26
#define MOTO2A 12
#define MOTO3A 14
#define MOTO4A 27


int pause = 1000;

//the setup function runs once when you press reset or power the board
void setup() {
  Serial.begin(115200);

  Serial.println("Initializing motors");
  //directions: L293D
  pinMode(MOTO_12EN, OUTPUT);
  pinMode(MOTO_34EN, OUTPUT);

  pinMode(MOTO1A, OUTPUT);
  pinMode(MOTO2A, OUTPUT);

  pinMode(MOTO3A, OUTPUT);
  pinMode(MOTO4A, OUTPUT);
  delay(pause);

  Serial.println("Turn off motors");
  digitalWrite(MOTO_12EN, LOW);
  digitalWrite(MOTO_34EN, LOW);
  delay(pause);

  Serial.println("Turning MOTO 1 cw");
  digitalWrite(MOTO1A, LOW);
  digitalWrite(MOTO2A, HIGH);
  delay(pause);

  Serial.println("Turning MOTO 2 ccw");
  digitalWrite(MOTO3A, HIGH);
  digitalWrite(MOTO4A, LOW);
  delay(pause);

  Serial.println("Main program go in delay");
  delay(pause);
}


void loop() {
  Serial.println("MOTO1");
  digitalWrite(MOTO_12EN, HIGH);
  digitalWrite(MOTO_34EN, LOW);
  delay(pause);

  Serial.println("MOTO2");
  digitalWrite(MOTO_12EN, LOW);
  digitalWrite(MOTO_34EN, HIGH);
  delay(pause);
}
