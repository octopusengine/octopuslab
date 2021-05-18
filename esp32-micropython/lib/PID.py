__author__ = 'beau'
__version__ = "1.0.0"

from time import ticks_ms

class PID:
    """
    Discrete PID control
    """

    def __init__(self,input_fun, output_fun, P=3., I=0.01, D=0.0):

        self.Kp=P
        self.Ki=I
        self.Kd=D

        self.I_value = 0
        self.P_value = 0
        self.D_value = 0

        self.I_max=100.0
        self.I_min=0

        self.set_point=0.0

        self.prev_value = 0

        self.output = 0

        self.output_fun = output_fun
        self.input_fun = input_fun

        self.last_update_time = ticks_ms()


    def update(self):

        if ticks_ms()-self.last_update_time > 500:
            """
            Calculate PID output value for given reference input and feedback
            """
            current_value = self.input_fun()
            self.error = self.set_point - current_value
            self.P_value = self.Kp * self.error
            self.D_value = self.Kd * ( current_value-self.prev_value)

            lapsed_time = ticks_ms()-self.last_update_time
            lapsed_time/=1000. #convert to seconds
            self.last_update_time = ticks_ms()

            self.I_value += self.error * self.Ki

            if self.I_value > self.I_max:
                self.I_value = self.I_max
            elif self.I_value < self.I_min:
                self.I_value = self.I_min

            self.output = self.P_value + self.I_value + self.D_value

            if self.output<0:
                self.output = 0.0
            if self.output>100:
                self.output = 100.0

            self.output_fun(self.output/100.0)

            self.last_update_time=ticks_ms()
            self.prev_value = current_value
