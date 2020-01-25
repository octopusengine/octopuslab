# L1,L2 simple 2 servos draw bot
from time import sleep_ms
from util.transform import invkin2, move_2d_line
# invkin2(point2d, angleMode=DEGREES, l1=l1,l2=l2)



print("servos init")
from config import Config
setup = Config("draw2servos")
setup.print_all()
try:
    L1 = int(setup.get("L1"))
    L2 = int(setup.get("L2"))
except:
    print("config.Err")
print("L1, L2: " + str(L1) + ", "+ str(L2) )


print("servos init")
from util.servo import Servo
s1 = Servo(17)
s2 = Servo(16)

s1.set_degree(90)
s2.set_degree(0)


def move_servo2(p1, p2, delay=5):
    steps = move_2d_line(p1, p2)
    for step in steps:
        
        alfa, beta = invkin2(step, L1, L2)
        print(step, alfa, beta)

        s1.set_degree(alfa)
        s2.set_degree(beta)
        sleep_ms(delay)


aa = 50
xa = 50
ya = 50

def run_sqare():
    """
    p1 = 0, 0 # strart point
    p2 = 50, 50 # stop point    
    move_servo2(p1, p2)
    """

    move_servo2((xa,ya),(xa,ya+aa))
    move_servo2((xa,ya+aa),(xa+aa,ya+aa))
    move_servo2((xa+aa,ya+aa),(xa+aa,ya))
    move_servo2((xa+aa,ya),(xa,ya))

for _ in range(12):
   run_sqare()

while True:
    y = int(input("x? "))
    x = int(input("y? "))
    point2d = x, y

    alfa, beta = invkin2(point2d, L1, L2)
    print(alfa, beta)

    s1.set_degree(alfa)
    s2.set_degree(beta)

    print("-"*12)
