import ujson

io_conf_file = 'config/io.json'
io_menu_layout = [
    {'attr': 'led', 'descr': 'built in LED diode'},
    {'attr': 'ws', 'descr': 'WS RGB LED 0/1/8/...n'},
    {'attr': 'piezzo', 'descr': 'Piezzo buzzer'},
    {'attr': 'led7', 'descr': 'SPI max 8x7 segm.display'},
    {'attr': 'led8', 'descr': 'SPI max 8x8 matrix display'},
    {'attr': 'oled', 'descr': 'I2C oled display'},
    {'attr': 'lcd', 'descr': 'I2C LCD 0/2/4 row'},
    {'attr': 'tft', 'descr': 'SPI 128x160 color display'},
    {'attr': 'sm', 'descr': 'UART - serial monitor (display)'},
    {'attr': 'temp', 'descr': 'temperature Dallas sens.'},
    {'attr': 'light', 'descr': 'I2C light sens. (lux)'},
    {'attr': 'mois', 'descr': 'A/D moisture sensor'},
    {'attr': 'cmois', 'descr': 'A/D capacit. moisture sensor'},
    {'attr': 'ad0', 'descr': 'A/D input voltage'},
    {'attr': 'ad1', 'descr': 'A/D x / photoresistor'},
    {'attr': 'ad2', 'descr': 'A/D y / thermistor'},
    {'attr': 'exp8', 'descr': 'I2C+expander PCF8574'},
    {'attr': 'keypad', 'descr': 'Robot I2C+expander 4x4 keypad'},
    {'attr': 'button', 'descr': 'DEV2 Button'},
    {'attr': 'ir', 'descr': 'DEV2 ir remote'},
    {'attr': 'fet', 'descr': 'MOS FET PWM (IoTboard)'},
    {'attr': 'relay', 'descr': 'Relay (IoTboard)'},
    {'attr': 'servo', 'descr': 'PWM pins (both Robot and IoT have by default)'},
    {'attr': 'stepper', 'descr': 'Stepper motor (ROBOTboard)'},
    {'attr': 'motor', 'descr': 'DC motor (ROBOTboard)'}
]

def get_from_file():
    try:
        with open(io_conf_file, 'r') as f:
            d = f.read()
            f.close()
            io_config = ujson.loads(d)
    except OSError:
        # FileNotFound
        io_config = {}
    return io_config
