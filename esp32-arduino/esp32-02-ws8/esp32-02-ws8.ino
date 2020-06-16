//esp32-02-ws8 - simple test: one WS2812 rgb LED
//octopusLAB - ESP32 ROBOT board (2018/09)
//NeoPixel(c) 2013 Shae Erisson (AdaFruit NeoPixel library)

#include <Adafruit_NeoPixel.h>

#define PIN_WS         13
#define NUMPIXELS      8
Adafruit_NeoPixel wsLED = Adafruit_NeoPixel(NUMPIXELS, PIN_WS, NEO_GRB + NEO_KHZ800);
// wsLED.Color takes RGB values, from 0,0,0 up to 255,255,255
int delayval = 1000; // delay for half a second

void wsOneRGBtest(){
    wsLED.setPixelColor(0, wsLED.Color(150,0,0));
    wsLED.show();
    delay(delayval/5);
    
    wsLED.setPixelColor(0, wsLED.Color(0,150,0));
    wsLED.show();
    delay(delayval/5);

    wsLED.setPixelColor(0, wsLED.Color(0,0,150));
    wsLED.show();
    delay(delayval/5);    
  }

void wsClear(){
   for(int i=0;i<NUMPIXELS;i++){   
      wsLED.setPixelColor(i, wsLED.Color(0,0,0));}
   wsLED.show();
}

void wsSnake(byte wsR,byte wsG,byte wsB){
   for(int i=0;i<NUMPIXELS;i++){
    wsLED.setPixelColor(i, wsLED.Color(wsR,wsG,wsB));
    wsLED.show();
    delay(delayval/10);
    wsLED.setPixelColor(i, wsLED.Color(0,0,0));
    wsLED.show();
   }
}

void wsNavigate(byte wsR,byte wsG,byte wsB){
    wsLED.setPixelColor(0, wsLED.Color(wsR,wsG,wsB));
    wsLED.setPixelColor(7, wsLED.Color(wsR,wsG,wsB));
    wsLED.show();
    delay(delayval/2);
    wsLED.setPixelColor(0, wsLED.Color(0,0,0));
    wsLED.setPixelColor(7, wsLED.Color(0,0,0));
    wsLED.show();
    delay(delayval);
}

void wsPolice(byte wsR,byte wsG,byte wsB){
    wsLED.setPixelColor(0, wsLED.Color(wsR,wsG,wsB));
    wsLED.setPixelColor(1, wsLED.Color(wsR,wsG,wsB));
    wsLED.setPixelColor(2, wsLED.Color(wsR,wsG,wsB));
    wsLED.setPixelColor(3, wsLED.Color(wsR,wsG,wsB));
    wsLED.setPixelColor(4, wsLED.Color(0,0,0));
    wsLED.setPixelColor(5, wsLED.Color(0,0,0));
    wsLED.setPixelColor(6, wsLED.Color(0,0,0));
    wsLED.setPixelColor(7, wsLED.Color(0,0,0));
    wsLED.show();
    delay(delayval/10);
    wsLED.setPixelColor(0, wsLED.Color(0,0,0));
    wsLED.setPixelColor(1, wsLED.Color(0,0,0));
    wsLED.setPixelColor(2, wsLED.Color(0,0,0));
    wsLED.setPixelColor(3, wsLED.Color(0,0,0));
    wsLED.setPixelColor(4, wsLED.Color(wsR,wsG,wsB));
    wsLED.setPixelColor(5, wsLED.Color(wsR,wsG,wsB));
    wsLED.setPixelColor(6, wsLED.Color(wsR,wsG,wsB));
    wsLED.setPixelColor(7, wsLED.Color(wsR,wsG,wsB));
    wsLED.show();
    delay(delayval/5);
}

void setup() {
  wsLED.begin(); // This initializes the NeoPixel library.
}

void loop() {
    wsSnake(50,0,0);
    wsSnake(0,50,0);
    wsSnake(0,0,50);

    delay(1000); 
    
    for(int i=0;i<3;i++){wsNavigate(50,0,0);}

    for(int i=0;i<5;i++){wsPolice(0,0,100);}
    wsClear();
    //wsOneRGBtest();
    delay(1000);
}
