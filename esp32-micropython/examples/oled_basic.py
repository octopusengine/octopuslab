def oled_init():

    from utils.pinout import set_pinout
    from machine import Pin, I2C
    import ssd1306

    pinout = set_pinout()
    i2c = I2C(0, scl=Pin(pinout.I2C_SCL_PIN), sda=Pin(pinout.I2C_SDA_PIN), freq=100000)

    oled = ssd1306.SSD1306_I2C(128, 64, i2c, 0x3c)
    return oled

oled = oled_init()
oled.text("octopusLAB", 0, 0)
oled.show()
