/*
  Example for remote controled WS led using Android application RoboRemo

  ESP32
  ESP8266

  (c) 2018/10 Petrkr
*/

#include "octopusLAB_ROBOT.h"

const char *wifi_ssid = "Wifi SSID";
const char *wifi_pass = "secretPassword";
#define WIFI_MAX_RETRY 60


// Wifi and network includes
#include <WiFiClient.h>
#include <WiFiUdp.h>

// ESP8266 specific includes
#ifdef ESP8266
#include <ESP8266WiFi.h>
#endif


// ESP32 specific includes
#ifdef ESP32
#include <WiFi.h>
#endif

// WS LED
#include <Adafruit_NeoPixel.h>
#define NUMPIXELS      1
Adafruit_NeoPixel wsLED = Adafruit_NeoPixel(NUMPIXELS, PIN_WS, NEO_GRB + NEO_KHZ800);

// UDP Listener
WiFiUDP WSUDPListener;
unsigned int WSUDPPort = 12811;
byte WSpacketBuffer[512];


void banner() {
  Serial.print(F("SDK: ")); Serial.println(ESP.getSdkVersion());
#ifdef ESP8266
  Serial.print(F("SN: ")); Serial.println(String(ESP.getChipId(), HEX));
  Serial.print(F("Core: ")); Serial.println(ESP.getCoreVersion());
  Serial.print(F("Checksum: ")); Serial.println(ESP.getSketchMD5());
#endif
}

void network_connect_wait() {
  uint16_t retry = 0;
  while (WiFi.status() != WL_CONNECTED) {
    delay(250);
    Serial.print(F("."));
    retry++;
    if (retry > WIFI_MAX_RETRY) {
      Serial.println(F(" Failed to connect to wifi"));
      break;
    }
  }
}

void network_setup() {
  Serial.println(F("Setting up Networking"));

  Serial.print(F("  Wifi mode... "));
  WiFi.mode(WIFI_STA);
  Serial.println(F("OK"));

#ifdef ESP8266
  ETS_UART_INTR_DISABLE();
  wifi_station_disconnect();
  ETS_UART_INTR_ENABLE();
#endif

  Serial.print(F("  trying connect to ")); Serial.print(wifi_ssid);
  WiFi.begin(wifi_ssid, wifi_pass);

  network_connect_wait();

  // Connection to wifi network success
  if (WiFi.status() == WL_CONNECTED)
  {
    Serial.println(F("OK"));
    Serial.println(F("Network information"));
    Serial.print(F("  IP address: "));
    Serial.println(WiFi.localIP());
  } else {
    Serial.println(F("Connection failed"));
  }
}

void setup() {
  Serial.begin(115200);

  banner();
  Serial.println();
  Serial.println(F("Booting up..."));

  pinMode(LED_BUILTIN, OUTPUT);
#ifdef ESP8266
  digitalWrite(LED_BUILTIN, HIGH);
#endif

  Serial.println("Setting up WS LED...");
  wsLED.begin();

  // Init black
  wsLED.setPixelColor(0, wsLED.Color(0, 0, 0));
  wsLED.show();

  // Network setup - WS BLUE
  wsLED.setPixelColor(0, wsLED.Color(0, 0, 255));
  wsLED.show();

  network_setup();

  if (WiFi.status() == WL_CONNECTED) {
    WSUDPListener.begin(WSUDPPort);

    // Network OK - Green
    wsLED.setPixelColor(0, wsLED.Color(0, 255, 0));
    wsLED.show();

    Serial.println(F("Ready to go!"));
    delay(1000);

    // Turn off WS led
    wsLED.setPixelColor(0, wsLED.Color(0, 0, 0));
    wsLED.show();
  }
  else {
    // Network Error - RED
    wsLED.setPixelColor(0, wsLED.Color(255, 0, 0));
    wsLED.show();
  }

}

byte ws_red = 0;
byte ws_green = 0;
byte ws_blue = 0;

void handleWSUDPServer() {
  int cb = WSUDPListener.parsePacket();
  if (cb) {
    WSUDPListener.read(WSpacketBuffer, cb);

    String value = "";
    for (int i = 1; i < cb; i++) {
      value += (char)WSpacketBuffer[i];
    }

    switch (WSpacketBuffer[0]) {
      case 'R':
        Serial.print("RED: ");
        ws_red = value.toInt();
        break;
      case 'G':
        Serial.print("GREEN: ");
        ws_green = value.toInt();
        break;
      case 'B':
        Serial.print("BLUE: ");
        ws_blue = value.toInt();
        break;
      case 'T':
        Serial.print("Toggle Built in LED state");
        digitalWrite(BUILTIN_LED, !digitalRead(BUILTIN_LED));
        break;
      default:
        Serial.print("Unknown command: ");
        Serial.print((char)WSpacketBuffer[0]);
        Serial.println(value);
    }

    Serial.println(value);
    wsLED.setPixelColor(0, wsLED.Color(ws_red, ws_green, ws_blue));
    wsLED.show();
  }
}

void loop() {
  // If there is no Wifi connected, it make no sense continue program
  if (WiFi.status() != WL_CONNECTED) {
    return;
  }

  handleWSUDPServer();

}
