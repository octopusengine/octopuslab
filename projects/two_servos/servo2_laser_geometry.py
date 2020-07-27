# servo laser pointer - example
# draw sguare, triangle and circle

# ampy -p /COM6 put ./examples/servo2_laser_geometry.py main.py

from time import sleep_ms
from utils.transform import *

from components.servo import Servo
# todo: PWM double setup error

s1 = Servo(17)
s2 = Servo(16)

dist = 100 # distance and size of "board"
delay = 3


def move_servo2(p1, p2, delay=delay):
    steps = move_2d_line(p1, p2)
    for step in steps:
        alfa = cosangle(step[0], dist, dist)[0]
        beta = cosangle(step[1], dist, dist)[0]
        print(step, alfa, beta)

        s1.set_degree(alfa)
        s2.set_degree(beta)
        sleep_ms(delay)


def move_laser_point(p1):
        alfa = cosangle(p1.x, dist, dist)[0]
        beta = cosangle(p1.y, dist, dist)[0]
        print(p1, alfa, beta)

        s1.set_degree(alfa)
        s2.set_degree(beta)


move = Point2D(30, 30)  
rr = 30 # radius

def run_circle():
    p1 = Point2D()
    p2 = Point2D()
    p1.x, p1.y = polar2cart(rr, 0)
    p1 += move

    for ang in range(360): # 36*2*10
        p2.x, p2.y = polar2cart(rr, ang)
        p2 += move
        try:
            #ove_servo2((p1.x,p1.y),(p2.x,p2.y))
            move_laser_point(p2)
        except:
            print("Err >")
        print(ang, p1, p2)
        # p1.x, p1y = p2.x, p2.y
        sleep_ms(1)


aa = 50
def run_sqare():
    """
    p1 = 0, 0 # strart point
    p2 = 50, 50 # stop point    
    move_servo2(p1, p2)
    """

    move_servo2((0,0),(0,aa))
    move_servo2((0,aa),(aa,aa))
    move_servo2((aa,aa),(aa,0))
    move_servo2((aa,0),(0,0))


def run_triangle():
    move_servo2((0,0),(0,aa))
    move_servo2((0,aa),(aa,aa/2))
    move_servo2((aa,aa/2),(0,0))


# ----------------------------------
while True:
    for i in range(2):
        run_sqare()
    sleep_ms(1000)
   
    for i in range(2):
        run_circle()    
    sleep_ms(1000)

    for i in range(2):
        run_triangle()    
    sleep_ms(1000)
