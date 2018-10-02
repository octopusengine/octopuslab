
// PIN as on octopusLAB ESP32 RobotBoard
#define MOTO_12EN 25
// Select version of robot board
//#define MOTO_34EN 15 // Robot Board v1
#define MOTO_34EN 13 // Robot Board v2
#define MOTO1A 26
#define MOTO2A 12
#define MOTO3A 14
#define MOTO4A 27


#define PWM_FREQ 500 //this can be almost whatever you want
#define PWM_RES 8    //no need to be more precise
#define MOTO1_CHAN 0
#define MOTO2_CHAN 1

int pause = 1000;

//the setup function runs once when you press reset or power the board
void setup() {
  Serial.begin(115200);

  Serial.println("Initializing motors");
  //directions: L293D
  ledcSetup(MOTO1_CHAN, PWM_FREQ, PWM_RES); // ESP32 pwm setup
  ledcSetup(MOTO2_CHAN, PWM_FREQ, PWM_RES); // ESP32 pwm setup

  ledcAttachPin(MOTO_12EN, MOTO1_CHAN); // MOTO 1 PWM
  ledcAttachPin(MOTO_34EN, MOTO2_CHAN); // MOTO 2 PWM

  pinMode(MOTO1A, OUTPUT);
  pinMode(MOTO2A, OUTPUT);

  pinMode(MOTO3A, OUTPUT);
  pinMode(MOTO4A, OUTPUT);
  delay(pause);

  Serial.println("Turn off motors");
  ledcWrite(MOTO1_CHAN, 0);
  ledcWrite(MOTO2_CHAN, 0);

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
  ledcWrite(MOTO1_CHAN, 220);
  ledcWrite(MOTO2_CHAN, 0);
  delay(pause);

  Serial.println("MOTO2");
  ledcWrite(MOTO1_CHAN, 0);
  ledcWrite(MOTO2_CHAN, 128);
  delay(pause);
}
