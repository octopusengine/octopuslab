//esp32-08-echo - simple test: one WS2812 rgb LED
//octopusLAB - ESP32 ROBOT board (2018/09)
//NeoPixel(c) 2013 Shae Erisson (AdaFruit NeoPixel library)
#define DEBUG

#define PIN_WS         13
#define NUMPIXELS      8

#define PIN_PWM1    17
#define PIN_PWM2    16
#define PIN_PWM3    4

//echo
const int trigPin = PIN_PWM1;
const int echoPin = PIN_PWM2;
// defines variables
long duration;
int distance;

int getEchoDistance(){
  digitalWrite(trigPin, LOW);  // Clears the trigPin
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH); // Sets the trigPin on HIGH state for 10 micro seconds
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);  // Reads the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(echoPin, HIGH);
  distance= duration*0.034/2;  // Calculating the distance
  return distance;
}

#include <Adafruit_NeoPixel.h>
Adafruit_NeoPixel wsLED = Adafruit_NeoPixel(NUMPIXELS, PIN_WS, NEO_GRB + NEO_KHZ800);
// wsLED.Color takes RGB values, from 0,0,0 up to 255,255,255
int delayval = 1000; // delay for half a second

void wsClear(){
   for(int i=0;i<NUMPIXELS;i++){   
      wsLED.setPixelColor(i, wsLED.Color(0,0,0));}
   wsLED.show();
}

void wsBar(int num,byte wsR,byte wsG,byte wsB){
   int numpx=int(num/10);
   for(int i=0;i<numpx;i++){
    wsLED.setPixelColor(i, wsLED.Color(wsR,wsG,wsB));      
   }
   wsLED.show();
   delay(delayval/2);
   wsClear();
   delay(delayval/10);
}

//------------------------------------------------------------------------------

void setup() {
  Serial.begin(9600); // Starts the serial communication
  pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
  pinMode(echoPin, INPUT); // Sets the echoPin as an Input
  wsLED.begin(); // This initializes the NeoPixel library.
  wsSnake(0,0,50); //test
}

void loop() {
    distance = getEchoDistance();
    wsBar(distance,0,10,0);
    #ifdef DEBUG
        Serial.print("Distance: ");
        Serial.println(distance);
    #endif
}
