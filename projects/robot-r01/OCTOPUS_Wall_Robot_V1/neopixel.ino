//octopusLAB - ESP32 ROBOT board (2018/09)
//NeoPixel(c) 2013 Shae Erisson (AdaFruit NeoPixel library)
#define DEBUG
#define NUMPIXELS 8 //for WS strip 1/8/16...

Adafruit_NeoPixel wsLED = Adafruit_NeoPixel(NUMPIXELS, PIN_WS, NEO_GRB + NEO_KHZ800);

//Neopixel setup
void neopixelInit() {
  wsLED.begin(); // This initializes the NeoPixel library.
  wsClear();
}

//sets no color to all neopixels
void wsClear() {
  for (int i = 0; i < NUMPIXELS; i++) {
    wsLED.setPixelColor(i, wsLED.Color(0, 0, 0));
  }
  wsLED.show();
}

//sets the number of pixels on a strip
void wsBar(int num, byte wsR, byte wsG, byte wsB) {
  wsClear();

  int numpx = num; // .../10
  if (numpx < 0) numpx = 0;
  if (numpx > 8) numpx = 8;

  for (int i = 0; i < numpx; i++) {
    wsLED.setPixelColor(i, wsLED.Color(wsG, wsB, wsR));
  }

  wsLED.show();
}

//sets all green strip
void wsSetGreen() {
  for (int i = 0; i < NUMPIXELS; i++) {
    wsLED.setPixelColor(i, wsLED.Color(25, 0, 0));
  }
  wsLED.show();
}

//sets all red strip
void wsSetRed() {
  for (int i = 0; i < NUMPIXELS; i++) {
    wsLED.setPixelColor(i, wsLED.Color(0, 25, 0));
  }
  wsLED.show();
}
