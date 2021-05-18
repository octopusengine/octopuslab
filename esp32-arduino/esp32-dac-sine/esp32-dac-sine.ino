// Create a sine wave on an oscilloscope using a 8 bit DAC
// (C) XTronical 2018
// Use in any way you wish!
//
 
// As we're using an 8 bit value for the DAC 0-255 (256 parts) that means for us
// there are 256 'bits' to a complete circle not 360 (as in degrees) or even 2PI Radians
// (There are 2*PI Radians in a circle and computers love to work in Radians!)
// The computer works in radians for SIN, COSINE etc. so we must convert our 0 -255 value
// to radians, the comments in the code show this.
 
int SineValues[256];       // an array to store our values for sine
 
void setup()
{
  float ConversionFactor=(2*PI)/256;        // convert my 0-255 bits in a circle to radians
                                            // there are 2 x PI radians in a circle hence the 2*PI
                                            // Then divide by 256 to get the value in radians
                                            // for one of my 0-255 bits.
  float RadAngle;                           // Angle in Radians
  // calculate sine values
  for(int MyAngle=0;MyAngle<256;MyAngle++) {
    RadAngle=MyAngle*ConversionFactor;               // 8 bit angle converted to radians
    SineValues[MyAngle]=(sin(RadAngle)*127)+128;  // get the sine of this angle and 'shift' up so
                                            // there are no negative values in the data
                                            // as the DAC does not understand them and would
                                            // convert to positive values.
  }
}
 
void loop()
{
  for(int i=0;i<256;i++)
    dacWrite(26,SineValues[i]);
}
