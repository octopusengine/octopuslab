#define LASER_MAX 1024

float _I_sum = 0;

float calcLaserError(int laser) {
  return (double)(laser - LASER_MAX / 2) / (LASER_MAX / 2);
}

float _correction_last = 0;

int calcSpeedCorrection(float error, float error_last) {
  float correction = error;
  if (correction * 1000 >= 0) {
    correction = pow(correction, kK);
  } else {
    correction = pow(correction * (-1), kK) * (-1);
  }
  correction = correction * pK; //P
  _I_sum = (float)(_I_sum + correction * iK); //I
  correction = correction + _I_sum;
  float D_change = (float)(error - error_last); //D
  correction = correction + D_change * dK;
  correction = correction * speed_pidcorrection;

  correction = calcEMACorrection(correction, _correction_last);
  _correction_last = correction;
  return (int)correction;
}

// Popis funkce...
int calcEMACorrection(float correction, float _correction_last) {
  float k_EMA = 2.0 / (n_EMA + 1);
  correction = correction * k_EMA + _correction_last * ((float)(1) - k_EMA);
  return correction;
}

void resetPid() {
  _I_sum = 0;
  _correction_last = 0;
}
