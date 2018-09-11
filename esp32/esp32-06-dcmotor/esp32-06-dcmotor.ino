
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
  //  pinMode(MOTO_34EN, OUTPUT);

  pinMode(MOTO1A, OUTPUT);
  pinMode(MOTO2A, OUTPUT);

  //  pinMode(MOTO3A, OUTPUT);
  //  pinMode(MOTO4A, OUTPUT);

  //digitalWrite(MOTO_34EN, HIGH);

  Serial.println("Turning MOTO 1 cw");
  digitalWrite(MOTO1A, LOW);
  digitalWrite(MOTO2A, HIGH);
}


void loop() {
  Serial.println("Turning EN on");
  digitalWrite(MOTO_12EN, HIGH);

  delay(pause);
  digitalWrite(MOTO_12EN, LOW);
  delay(pause);
}
