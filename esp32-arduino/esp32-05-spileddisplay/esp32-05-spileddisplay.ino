#include <LEDMatrixDriver.hpp>
#include "led_charmap.h"

const uint8_t LEDMATRIX_CS_PIN = 5;
const uint8_t NO_OF_DRIVERS = 1;

LEDMatrixDriver lmd(NO_OF_DRIVERS, LEDMATRIX_CS_PIN);


//==============================================================
//======================= DISPLAY ==============================
//==============================================================


void display_text(String value) {
  display_text(value, true);
}
void display_text(String value, bool display_show) {
#ifdef DEBUG
  Serial.print(F("LED Show: "));
  Serial.println(value);
#endif

  byte digit;
  byte digit_value = 0;
  for (digit = 0; digit < 8; digit++) {
    if ( digit >= value.length() ) {
      digit_value = 0x00;
    } else if (value[digit] >= 'A' and value[digit] <= 'Z') {
      digit_value = ALPHA[value[digit] - 'A'];
    } else if (value[digit] >= 'a' and value[digit] <= 'z') {
      digit_value = alpha[value[digit] - 'a'];
    } else if (value[digit] >= '0' and value[digit] <= '9') {
      digit_value = digits[value[digit] - '0'];
    } else {
      switch (value[digit]) {
        case '.':
        case '_':
          digit_value = special[0];
          break;
        case '-':
        case ':':
          digit_value = special[1];
          break;
        case '~':
          digit_value = special[2];
          break;
        case '°':
          digit_value = special[3];
          break;
        case '=':
          digit_value = special[11];
          break;
        case '^':
          digit_value = special[12];
          break;
        case '&':
          digit_value = special[13];
          break;
        case '#':
          digit_value = special[14];
          break;
        case '[':
        case '(':
          digit_value = special[15];
          break;
        case ']':
        case ')':
          digit_value = special[16];
          break;
        case '/':
          digit_value = special[17];
          break;
        case '\\':
          digit_value = special[18];
          break;
        case '{':
          digit_value = special[19];
          break;
        case '}':
          digit_value = special[20];
          break;
        default:
          digit_value = 0x00;
          break;
      }
    }

#ifdef DEBUG
    Serial.print(F("Setting digit ")); Serial.print(7 - digit); Serial.print(F(" to value ")); Serial.println(digit_value);
#endif
    lmd.setDigit(7 - digit, digit_value);
  }

  if (display_show) {
    lmd.display();
  }
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  
  Serial.println(F("Setting up LED Display..."));
  lmd.setEnabled(true);
  lmd.setIntensity(7);
  lmd.setScanLimit(7);
  lmd.setDecode(0x00);
  lmd.clear();

  display_text("octopus");
}

void loop() {


}

