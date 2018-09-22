uart = UART(1, 9600)
uart.init(9600, bits=8, parity=None, stop=1, timeout=1000)

uart.write('C')    #clear
uart.write('W7')   #change color
uart.write('h260') #horizontal line
uart.write('W8')   #color
uart.write('QoctopusLAB-test*')



