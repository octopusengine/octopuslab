#include <ETH.h>

// TODO: Pin# of the enable signal for the external crystal oscillator (-1 to disable for internal APLL source)
#define ETH_POWER_PIN   -1
#define ETH_ADDR        1


static bool eth_connected = false;

void WiFiEvent(WiFiEvent_t event) {
  switch (event) {
    case SYSTEM_EVENT_ETH_START:
      Serial.println("ETH Started");
      //set eth hostname here
      ETH.setHostname("esp32-ethernet");
      break;
    case SYSTEM_EVENT_ETH_CONNECTED:
      Serial.println("ETH Connected");
      digitalWrite(2, HIGH); //Builtin LED ON
      break;
    case SYSTEM_EVENT_ETH_GOT_IP:
      Serial.print("ETH MAC: ");
      Serial.print(ETH.macAddress());
      Serial.print(", IPv4: ");
      Serial.print(ETH.localIP());
      if (ETH.fullDuplex()) {
        Serial.print(", FULL_DUPLEX");
      }
      Serial.print(", ");
      Serial.print(ETH.linkSpeed());
      Serial.println("Mbps");
      eth_connected = true;
      break;
    case SYSTEM_EVENT_ETH_DISCONNECTED:
      Serial.println("ETH Disconnected");
      eth_connected = false;
      digitalWrite(2, LOW); // Builtin LED OFF
      break;
    case SYSTEM_EVENT_ETH_STOP:
      Serial.println("ETH Stopped");
      eth_connected = false;
      break;
    default:
      break;
  }
}
#include <WiFiClientSecure.h>

void testClient(const char * host, uint16_t port, const char * url) {
  Serial.print("\nconnecting to ");
  Serial.println(host);

  WiFiClient client;
  if (!client.connect(host, port)) {
    Serial.println("connection failed");
    return;
  }
  client.printf("GET %s HTTP/1.1\r\nHost: %s\r\n\r\n", url, host);
  while (client.connected() && !client.available());
  while (client.available()) {
    Serial.write(client.read());
  }

  Serial.println("closing connection\n");
  client.stop();
}

void setup() {
  Serial.begin(115200);

  //Built in LED
  pinMode(4, OUTPUT);
  pinMode(15, OUTPUT);
  digitalWrite(4, LOW);
  digitalWrite(15, LOW);

  Serial.println("Program RUN");
  WiFi.onEvent(WiFiEvent);
  ETH.begin(ETH_ADDR, ETH_POWER_PIN, ETH_PHY_MDC, ETH_PHY_MDIO, ETH_PHY_TYPE, ETH_CLOCK_GPIO17_OUT);
}

long previousKeepAliveMillis = 0;
void handleKeepAlive() {
  if (millis() - previousKeepAliveMillis >= 1000) {
    previousKeepAliveMillis = millis();

    Serial.println("Keep Alive");
  }
}

long previousTimer1 = 0;
void handleTimer1() {
  if (millis() - previousTimer1 >= 5000) {
    previousTimer1 = millis();

    if (eth_connected) {
      digitalWrite(15, HIGH);
      testClient("ifconfig.co", 80, "/json");
      digitalWrite(15, LOW);
    }

  }
}

void loop() {
  digitalWrite(4, eth_connected);

  handleKeepAlive();

  handleTimer1();
}
