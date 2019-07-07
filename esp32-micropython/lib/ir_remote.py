# ir_remote.py - simple ir library
from machine import Pin, Timer
from time import sleep_us
import micropython

Device_dict = {
	"0000000011111111":"DO",
	"0000010000010000":"UPC"}
Buttom_dict = { 
	"0111001110001100":"OK" ,	                  
	"0100100010110111": "UP",
	"0100101110110100":"DOWN",
	"1001100101100110":"LEFT",
	"1000001101111100":"RIGHT",
	"0011000011001111":"1",
	"0001100011100111":"2",
	"0111101010000101":"3",
	"0001000011101111":"4",
	"0011100011000111":"5",
	"0101101010100101":"6",
	"0100001010111101":"7",
	"0100101010110101":"8",
	"0101001010101101":"9",
	"0110100010010111":"0" }

def send_id(out_signal, pin_name):

	L2 = Pin(pin_name, mode=Pin.AF_PP, af=Pin.AF1_TIM2)
	timer = Timer(2,freq = 38000)
	ch = timer.channel(1, Timer.PWM, pin =L2, pulse_width_percent = 0.5)
	sleep_us(9000)	
	ch = timer.channel(1, Timer.PWM, pin =L2, pulse_width_percent = 0)
	sleep_us(4500)

	for i in out_signal:
		if i == "0":
			ch = timer.channel(1, Timer.PWM, pin =L2, pulse_width_percent = 0.5)
			sleep_us(560)
			ch = timer.channel(1, Timer.PWM, pin =L2, pulse_width_percent = 0)
			sleep_us(565)			
		else:
			ch = timer.channel(1, Timer.PWM, pin =L2, pulse_width_percent = 0.5)
			sleep_us(560)
			ch = timer.channel(1, Timer.PWM, pin =L2, pulse_width_percent = 0)
			sleep_us(1690)
			
		ch = timer.channel(1, Timer.PWM, pin =L2, pulse_width_percent = 0.5)
		sleep_us(560)
		ch = timer.channel(1, Timer.PWM, pin =L2, pulse_width_percent = 0)
			
	# send_id("11001101001100100111001110001100",'PA5')

def read_id(pin_name):
	key = ""
	device = ""
	L1 = Pin(pin_name, Pin.IN, Pin.PULL_UP)
	a = []

	#while L1.value() == 1:
	#	pass
	for j in range(30000):
		if L1.value() == 0: break

	sleep_us(13560)	# this for initial time

	for i in range(1000):		
		v = L1.value()
		a.append(v)
		sleep_us(56)
	# print (a, len(a))

	a_c = []
	count = 0

	for i in a:	
		if i == 1:
			count += 1
		elif i == 0:
			if count > 0 :
				a_c.append(count)
			count =0

	for i in range(len(a_c)):
		if a_c[i] > 10:
			a_c[i] = "1"
		else:
			a_c[i] = "0"
	# print (a_c)

	B1 = "".join(a_c) #print (B1) 

	Data_device = B1[0:16]
	#if len(Data_device) > 0: print ("device: " + Data_device)

	Data_buttom = str(B1[16:32])
	#if len(Data_buttom) > 0: print ("button: " + Data_buttom)

	for key_d in Device_dict.keys():
		if  str(Data_device) == str(key_d):
			device = Device_dict[key_d]
			#print (Device_dict[key_d], end = ' ')

	if Data_buttom in Buttom_dict.keys():
		key = Buttom_dict[Data_buttom]        
		#print(key)

	return Data_device, Data_buttom, device, key

#while True:
#    f = read_id(33)
#    print("key: " + f[3])
#    # send_id(f[1])