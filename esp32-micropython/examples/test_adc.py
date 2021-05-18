from machine import ADC,Pin
from time import sleep_ms, sleep_us

a = ADC(Pin(34))
a.atten(ADC.ATTN_2_5DB)

def get_adc_aver(self, num=10):
    sumAn = 0
    for i in range(num):
        an = a.read()
        sumAn += an
        sleep_us(10)
    return int(sumAn/num)


while True:
    get_adc_aver(100)
    sleep_ms(200)
