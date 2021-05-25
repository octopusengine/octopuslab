# basic example: octopusLAB - ESP32 - PLC - MQTT
from time import sleep
from machine import Timer
from gc import mem_free

from utils.wifi_connect import read_wifi_config, WiFiConnect 
from utils.mqtt import MQTT
from utils.pinout import set_pinout
from utils.octopus_lib import i2c_init
from utils.bits import neg, reverse, int2bin, get_bit, set_bit

from components.plc.inputs.dummy import PLC_input_dummy
from components.plc.inputs.fixed import plc_input_fixed_high, plc_input_fixed_low
# from components.plc.elements.rs import PLC_element_RS
from components.plc.elements.rs_pulse import PLC_element_RS_pulse
from components.plc.operands.op_and import PLC_operand_AND
from components.plc.operands.op_or import PLC_operand_OR
from components.lm75 import LM75B
from components.led import Led
from components.rgb import Rgb
from components.i2c_expander import Expander8

print("mqtt-plc.py > mqtt basic example")

print("--- RAM free ---> " + str(mem_free())) 

pinout = set_pinout()
led = Led(pinout.BUILT_IN_LED)

num_neo = 16 # 30 # number of Leds
np = Rgb(pinout.WS_LED_PIN,num_neo) 

ws_r = 0
ws_g = 0
ws_b = 0


IN1, IN2, IN3, IN4     = 0, 1, 2, 3
OUT1, OUT2, OUT3, OUT4 = 4, 5, 6, 7
# OUT4 - signalization

timer_counter = 0
periodic = False
# tim1 = Timer(0)

print("--- PLC shield ---")
print("-"*50)

byte8 = 255 # all leds off

def parse_rgba_msg(msg):
    """
    parse rgba message to dict from following formats:
    #ff00C3
    #ff00C3FF
    RGBA(255,0,200,255) or rgba(255,0,200,255)
    RGB(255,0,200,255) or rgb(255,0,200)
    [255,0,200,255]
    [255,0,200]
    """
    ret = {
        'RED': 0,
        'GREEN': 0,
        'BLUE': 0,
        'ALPHA': 0
    }

    if msg.startswith('#'):
        try:
            #ff00C3
            ret['RED'] = int(msg[1:3],16)
            ret['GREEN'] = int(msg[3:5],16)
            ret['BLUE'] = int(msg[5:7],16)
            try:
                # add alpha if present
                ret['ALPHA'] = int(msg[7:9],16)
            except (IndexError, ValueError):
                ret['ALPHA'] = 255
        except (IndexError, ValueError):
            pass
        else:
            return ret
    components = []
    if (msg.startswith('rgb(') or  msg.startswith('RGB(')) and msg.endswith(')'):
        components = msg[4:-1].split(',')
    if (msg.startswith('rgba(') or  msg.startswith('RGBA(')) and msg.endswith(')'):
        components = msg[5:-1].split(',')
    try:
        ret['RED'] = int(components[0])
        ret['GREEN'] = int(components[1])
        ret['BLUE'] = int(components[2])
        try:
            # add alpha if present
            ret['ALPHA'] = int(components[3])
        except (IndexError, ValueError):
            ret['ALPHA'] = 255

    except (IndexError, ValueError):
        pass
    else:
        return ret
    print("Unable to parse RGBA value", msg)
    return ret


def rgb_color(red,green,blue):
    for i in range(num_neo):
        np.color((red, green, blue),i)

def plc_set(output,value):
     global byte8
     print(output,"->", value)
     byte8 = set_bit(byte8,output,value)
     exp8.write_8bit(byte8)
     sleep(0.1)


print("- I2C:")
i2c = i2c_init(True,200)
print(i2c.scan())
# 34 expander / 73 therm. / 84 eeprom

lm = LM75B(i2c)
temp = lm.get_temp()
print("- Temp: ", temp)

exp8 = Expander8(34,i2c)
print("- PCF:", exp8.read())

# bits4 = "0101"
# exp8.write_8bit(bits4)

plc_set(OUT1,0)
sleep(0.2)
plc_set(OUT2,0)
sleep(0.2)
plc_set(OUT3,0)
sleep(0.5)
exp8.write_8bit(255)


def simple_blink():
    led.value(1)
    sleep(0.5)
    led.value(0)
    sleep(0.5)


def mqtt_handler(topic, msg):
    global byte8
    print("MQTT handler {0}: {1}".format(topic, msg))
    data = bytes.decode(msg)

    if "led" in topic:
        print("led:", end='')        

        if data[0] == '1':  # oN
            print("-> on")
            led.value(1)
        elif data[0] == '0':  # ofF 
            print("-> off")
            led.value(0)
            sleep(0.1)

    if "rgb" in topic:
        # parse message to RGBA 0-255
        data = parse_rgba_msg(bytes.decode(msg))
        print("rgb:", data)
        rgb_color(data['RED'], data['GREEN'], data['BLUE'])


    if "do/1" in topic: # do = digital output
        if data == '1': plc_set(OUT1,0) # on
        elif data == '0': plc_set(OUT1,1) # off
            

    if "do/2" in topic:
        if data == '1': plc_set(OUT2,0)
        elif data == '0': plc_set(OUT2,1)

    if "do/3" in topic:
        if data == '1': plc_set(OUT3,0)
        elif data == '0': plc_set(OUT3,1)


def mqtt_send_temp():
    try:
       temp = lm.get_temp()
       print("- Temp: ", temp)
       c.publish("octopus/device/{0}/temp".format(m.client_id),str(temp)) # topic, message (value) to publish
       
    except:
       print("mqtt_send_temp() Err.")


print("--- wifi_connect >")
net = WiFiConnect()
net.connect()

print("--- mqtt_connnect >")
# c = mqtt_connect_from_config(esp_id)
m = MQTT.from_config()
c = m.client

c.set_callback(mqtt_handler)
c.connect()
c.subscribe("octopus/device/{0}/#".format(m.client_id))
 
print("testing blink")
simple_blink()setup()

print("send alive message")
c.publish("octopus/device", m.client_id) # topic, message (value) to publish

print("--- RAM free ---> " + str(mem_free()))
print("--- main loop >")
loop_count = 0
while True:
    c.check_msg()
  
    sleep(0.1)
    loop_count +=1
    print(".",end="")
    if loop_count == 100:
        mqtt_send_temp()
        loop_count = 0
        print()
