// Ultrasonic Meter, using interrupts
// Tested with SR04M module on ESP8266 Wemos D1

//Constants
const byte triggerPin = D1;
const byte echoPing = D2;

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

  Serial.println("TMR Trigger");

  digitalWrite(triggerPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(triggerPin, LOW);

  timer1Last = millis();
}


void loop()
{
  // Shew measured echo length
  if (echoFinished) {
    Serial.print("Length (us): "); Serial.println(echoLength);         // RAW data measured by interrupt
    Serial.print("Length (mm): "); Serial.println(echoLength * 0.17);  // Recalculate to mm by using sound speed way
    Serial.print("Length (mm): "); Serial.println(echoLength / 5.70);  // Recalculate to mm by using micros length way
    echoFinished = false;
  }

  timer1(500);
}
