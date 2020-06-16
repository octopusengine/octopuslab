// https://github.com/z3t0/Arduino-IRremote
// testing with octopusLab roborBoard - pin 33 (DEV2)

#include <IRremote.h>
 
int RECV_PIN = 33;
 
IRrecv irrecv(RECV_PIN);
 
decode_results results;
 
void setup()
{
Serial.begin(9600);
irrecv.enableIRIn(); // Start the receiver
}
 
void loop()
{
if (irrecv.decode(&results))
{
Serial.println(results.value, HEX);
irrecv.resume();
}
}
