
#define LMOTO_FORWARD MOTO1A
#define LMOTO_BACKWARD MOTO2A
#define LMOTO_PWM MOTO_12EN

#define PMOTO_FORWARD MOTO3A
#define PMOTO_BACKWARD MOTO4A
#define PMOTO_PWM MOTO_34EN


#define PWM_FREQ 500                   
#define PWM_RES 8
#define LMOTO_CHAN 0
#define PMOTO_CHAN 1



// motor_left(speed);
//
void motorLeft(int speed) {

  int forward = true;
  if (speed > 255) speed = 255;
  if (speed < -255) speed = -255;
  if (speed < 0) {
    forward = false;
    speed = -speed;
  }

  digitalWrite(LMOTO_FORWARD, forward);
  digitalWrite(LMOTO_BACKWARD, !forward);
  ledcWrite(LMOTO_CHAN, speed);
}

// motor_right(speed);
//
void motorRight(int speed) {

  int forward = true;
  if (speed > 255) speed = 255;
  if (speed < -255) speed = -255;
  if (speed < 0) {
    forward = false;
    speed = -speed;
  }

  digitalWrite(PMOTO_FORWARD, forward);
  digitalWrite(PMOTO_BACKWARD, !forward);
  ledcWrite(PMOTO_CHAN, speed);
}

void initMoto() {
  pinMode(LMOTO_FORWARD, OUTPUT); // Lmotor FORWARD
  pinMode(LMOTO_BACKWARD, OUTPUT); // Lmotor BACKWARD

  pinMode(PMOTO_FORWARD, OUTPUT); // Rmotor FORWARD
  pinMode(PMOTO_BACKWARD, OUTPUT); // Rmotor BACKWARD

  ledcSetup(LMOTO_CHAN, PWM_FREQ, PWM_RES);
  ledcSetup(PMOTO_CHAN, PWM_FREQ, PWM_RES);

  ledcAttachPin(LMOTO_PWM, LMOTO_CHAN); // Lmotor PWM
  ledcAttachPin(PMOTO_PWM, PMOTO_CHAN); // Rmotor PWM

  motorLeft(0);
  motorRight(0);

}
