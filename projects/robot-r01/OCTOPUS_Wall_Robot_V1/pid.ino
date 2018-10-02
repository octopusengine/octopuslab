#define LASER_MAX 1024 //laser reads values <0;1024>

//Integration sum
float _I_sum = 0;

//calculates the <-1;1> wall distance error
float calcLaserError(int laser) {
  return (double)(laser - LASER_MAX / 2) / (LASER_MAX / 2);
}

float _correction_last = 0;

//THE pid regulator
int calcSpeedCorrection(float error, float error_last) {
  float correction = error;

  //"qadratic" deformation of the otherwise linear error
  if (correction * 1000 >= 0) {
    //if the correction is positive
    correction = pow(correction, kK);
  } else {
    //if the correction is positive
    correction = -pow(-correction, kK);
  }
  correction = correction * pK; //Proportional part
  _I_sum = (float)(_I_sum + correction * iK); //Integration part
  correction = correction + _I_sum; //appliing the I regulation part (filtering)
  float D_change = (float)(error - error_last); //Derivation part
  correction = correction + D_change * dK; //appliing the D part (reaction to changes)
  correction = correction * speed_pidcorrection; //correction -> motor speed delta

  correction = calcEMACorrection(correction, _correction_last); //D part peak smoothing
  _correction_last = correction;
  return (int)correction;
}

//EMA correction peak smoothing 
int calcEMACorrection(float correction, float _correction_last) {
  //google financial EMA calculation 
  float k_EMA = 2.0 / (n_EMA + 1.0);
  correction = correction * k_EMA + _correction_last * (1.0 - k_EMA);
  return correction;
}

//clears the internal stuff
void resetPid() {
  _I_sum = 0;
  _correction_last = 0;
}
