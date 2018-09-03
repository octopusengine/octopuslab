// Ultrasonic Meter, using interrupts and show length on I2C conneted LED BAR
// Tested with SR04M module on ESP8266 Wemos D1


#include <Wire.h>

//Constants
const byte triggerPin = D5;
const byte echoPing = D6;
const byte I2C_address = 0x21;

// interrupt handling variables
volatile long startEcho = 0;
volatile long echoLength = 0;
volatile bool echoFinished = false;


// Handle interrupt - read pulse length
void handleEcho() {
  if (digitalRead(echoPing) == HIGH) {
    startEcho = micros();
  } else {
    echoLength = micros() - startEcho;
    echoFinished = true;
  }
}


void setup()
{
  Serial.begin(115200);
  Wire.begin();

  // Attach Echo PIN to interrupt
  attachInterrupt(digitalPinToInterrupt(echoPing), handleEcho, CHANGE);
  pinMode(triggerPin, OUTPUT);
  digitalWrite(triggerPin, LOW);
}

//Timer 1
unsigned long timer1Last = 0;
void timer1(int interval) {
  if (millis() < timer1Last+interval) {
    return;
  }

  digitalWrite(triggerPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(triggerPin, LOW);

  timer1Last = millis();
}


void loop()
{
  // Shew measured echo length
  if (echoFinished) {
    echoFinished = false;

    int toWrite = 255 - (pow(2, constrain(map(echoLength / 5.70, 200, 600, 0, 8), 0, 8)) - 1);
    Serial.print("Length (mm): "); Serial.println(echoLength / 5.70);  // Recalculate to mm by using micros length way

    Wire.beginTransmission(I2C_address);
    Wire.write(toWrite);
    Wire.endTransmission();
  }

  timer1(50);
}
