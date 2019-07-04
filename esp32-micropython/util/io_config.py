import ujson

io_conf_file = 'config/io.json'
io_menu_layout = [
    {'attr': 'oled', 'descr': 'oled'},
    {'attr': 'temp', 'descr': 'temperature'},
    {'attr': 'light', 'descr': 'light (lux)'},
    {'attr': 'mois', 'descr': 'moisture'},
    {'attr': 'ad0', 'descr': 'A/D input voltage'},
    {'attr': 'ad1', 'descr': 'A/D x / photoresistor'},
    {'attr': 'ad2', 'descr': 'A/D y / thermistor'},
    {'attr': 'keypad', 'descr': 'Robot I2C+expander 4x4 keypad'},
    {'attr': 'button', 'descr': 'DEV2 Button'},
    {'attr': 'servo', 'descr': 'Have PWM pins (both Robot and IoT have by default)'},
    {'attr': 'stepper', 'descr': 'Stepper motor'},
    {'attr': 'fet', 'descr': 'Have FET'},
    {'attr': 'relay', 'descr': 'Have Relay'},
    {'attr': 'ws', 'descr': 'WS RGB LED 0/1/8/...n'},
    {'attr': 'led7', 'descr': 'SPI max 8x7 segm.display'},
    {'attr': 'led8', 'descr': 'SPI max 8x8 matrix display'},
    {'attr': 'oled', 'descr': 'I2C'},
    {'attr': 'lcd', 'descr': 'I2C'},
    {'attr': 'tft', 'descr': '128x160'},
    {'attr': 'sm', 'descr': 'UART - serial monitor (display)'}
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
