// For graphs you can use plotter function in arduino

int VINMES = 36;    // RobotBoard v2
int sensorValue = 0;

void setup() {
  // declare the ledPin as an OUTPUT:
  Serial.begin(115200);

  Serial.println("Init");
}

void loop() {
  // read the value from the sensor:
  sensorValue = analogRead(VINMES);

  Serial.print("Analog: ");
  Serial.println(sensorValue);
  delay(50);
}
