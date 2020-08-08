# PWM fade for LED light
# sw (sleep_us) / hw (pwm duty/freq)

from time import sleep_us, sleep_ms


def fade_in_sw(p, r, m): # PIN - range - multipl
     for i in range(r):
          p.value(0)
          sleep_us((r-i)*m*2) # multH/L *2
          p.value(1)
          sleep_us(i*m)


def fade_out_sw(p, r, m): # pin - range - multipl
     for i in range(r):
          p.value(1)
          sleep_us((r-i)*m)
          p.value(0)
          sleep_us(i*m*2)


# fade_in(pwm_fet, 500) -> fade_in(PWM, lightIntensity)
def fade_in(pwm_fet, r, m = 5, fmax = 3000):
    # duty max - multipl us (2=2us) - fmax
    f = 100
    rs = 35

    pwm_fet.freq(f)
    pwm_fet.duty(1)
    sleep_ms(rs*2)

    pwm_fet.duty(5)
    sleep_ms(rs)

    for i in range(5,rs):
        pwm_fet.duty(i)
        pwm_fet.freq(f)
        sleep_ms(m*(rs-i+1))
        f += int(fmax/rs) 

    pwm_fet.freq(fmax)
    for i in range(rs, r):
        pwm_fet.duty(i)
        sleep_ms(m)