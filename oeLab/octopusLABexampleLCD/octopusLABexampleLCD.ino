#include <Wire.h>
#include <hd44780.h>                       // main hd44780 header
#include <hd44780ioClass/hd44780_I2Cexp.h> // i2c expander i/o class header

hd44780_I2Cexp lcd; // declare lcd object: auto locate & config exapander chip

// LCD geometry
const int LCD_COLS = 16;
const int LCD_ROWS = 2;
int num=0;

#include "octopusLAB.h"

DigitalPin led(OE_LAB_LED);
DigitalPin piezo(OE_LAB_PIEZZO2);


void setup()
{

  piezo.Beep(100);
  delay(200);
  piezo.Beep(300);  

  int status;
	status = lcd.begin(LCD_COLS, LCD_ROWS);
	if(status) // non zero status means it was unsuccesful
	{
		status = -status; 
		hd44780::fatalError(status); 
	}
	lcd.print("octopusLAB LCD:");
  lcd.setCursor(0,1);
 //print the configured LCD geometry
  lcd.print(LCD_COLS);
  lcd.print("x");
  lcd.print(LCD_ROWS);
  delay(2000);

  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("oeLAB::surikata");
}

//----------------------------
int decimals(int numDec)
{
  int i=0;
  int idec=1;
   do
   {
     i++;
     idec=idec*10;
   } while (numDec>=idec);
   return i;
}

void loop() 
{
  //lcd.clear();
  //lcd.setCursor(0,0);
  //lcd.print("oeLAB::surikata");

  num++; 
  int numDec=decimals(num); 
  lcd.setCursor(LCD_COLS-numDec-3,1);
  lcd.print(num);
  lcd.print("->");
  lcd.print(numDec);
  delay(500);

  led.SetLow();
  //piezo.Beep(20);
  delay(500);
  led.SetHigh();
  
  delay(3000);
  led.FastBlink(7); //test signal alert



    
/*
  lcd.cursor(); // turn on cursor so you can see where it is
  char c = '0'; // start at the character for the number zero
  for(int i = 2*LCD_COLS*LCD_ROWS; i; i--)
  {
    lcd.print(c++);
    delay(100); // slow things down to watch the printing & wrapping
    if(c > 0x7e) // wrap back to beginning of printable ASCII chars
      c = '!'; 
  }
  delay(500);
  lcd.noCursor();
  */ 
}
