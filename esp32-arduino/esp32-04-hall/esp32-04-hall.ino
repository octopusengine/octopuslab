// ESP32 má hallovu sondu - testujte magnetem
// esp32-04-hall - simple test: magnetic field detection


void setup() {  
  Serial.begin(115200);
  Serial.println("READY");
}

void loop() {
  Serial.println(hallRead());
  delay(250);
}