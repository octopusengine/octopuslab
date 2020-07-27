# TODO add steering which achieve speed (for real transport, for example racing cars)

class Steering:
    '''
    Very simple steering
    '''
    def __init__(self, motor_l, motor_r):
        self.motor_l = motor_l
        self.motor_r = motor_r

    def left(self, value):
        self.motor_l.speed(0)
        self.motor_r.speed(value)

    def right(self, value):
        self.motor_r.speed(0)
        self.motor_l.speed(value)

    def center(self, value):
        self.motor_l.speed(value)
        self.motor_r.speed(value)
