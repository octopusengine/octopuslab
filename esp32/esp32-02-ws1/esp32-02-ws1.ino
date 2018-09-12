//esp32-02-ws1 - simple test: one WS2812 rgb LED
//octopusLAB - ESP32 ROBOT board (2018/09)
//NeoPixel(c) 2013 Shae Erisson (AdaFruit NeoPixel library)

#include <Adafruit_NeoPixel.h>

#define PIN_WS         13
#define NUMPIXELS      1
Adafruit_NeoPixel wsLED = Adafruit_NeoPixel(NUMPIXELS, PIN_WS, NEO_GRB + NEO_KHZ800);

int delayval = 2000; // delay for half a second

void setup() {
  wsLED.begin(); // This initializes the NeoPixel library.
}

void loop() {
/*
  for(int i=0;i<NUMPIXELS;i++){
    // pixels.Color takes RGB values, from 0,0,0 up to 255,255,255
    pixels.setPixelColor(i, pixels.Color(150,0,0));
    pixels.show();
    delay(delayval);
    }
*/
    wsLED.setPixelColor(0, wsLED.Color(150,0,0));
    wsLED.show();
    delay(delayval);
    
    wsLED.setPixelColor(0, wsLED.Color(0,150,0));
    wsLED.show();
    delay(delayval);

    wsLED.setPixelColor(0, wsLED.Color(0,0,150));
    wsLED.show();
    delay(delayval);  
}
