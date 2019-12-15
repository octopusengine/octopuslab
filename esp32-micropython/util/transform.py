import math

"""
octopusLAB - basic lib. transform math
2019/11
inspir: https://github.com/aquila12/me-arm-ik
todo
class: point2d / point3d
gimbal: 2 x pol / const r
IK: invers kinematics
for robotic arm (3/5 axes)
drawbot and polar graph math.

from util.transform import *
ampy -p /COM6 put ./util/transform.py util/transform.py
"""

point0_2d = 0, 0
point0_3d = 0, 0, 0

# point: p = x, y
def distance2(p1, p2, rr = 3):  # default round rr
    # x1 = p1[0], y2 = p1[1]
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    return round(math.sqrt(dx*dx + dy*dy), rr)


def move_2d_line(p_start, p_stop, steps = 100, max_dist = 100, debug = False): # default: one step per one unit
    unit = max_dist/steps
    move_dist = distance2(p_start, p_stop)
    move_steps = move_dist/unit
    if debug:
        print(unit, move_dist, move_steps)

    x = p_start[0]
    y = p_start[1]
    dx = p_stop[0] - x
    dy = p_stop[1] - y
    ddx = dx/move_steps
    ddy = dy/move_steps
        
    points = []
    for step in range(move_steps):
        if debug:
            print(step, x, y) # test / debug
        points.append((x, y))
        x += ddx
        y += ddy
    
    points.append((p_stop[0], p_stop[1]))
    return points


def polar2cart(r, alfa, rr = 3):
    x = r * math.cos(math.radians(alfa))
    y = r * math.sin(math.radians(alfa))
    return round(x, rr), round(y, rr)


def cart2polar(point):
    x = point[0]
    y = point[1]
    r = distance2((0, 0), point)
    c = x / r
    s = y / r
    
    #Safety!
    if(s > 1): s = 1
    if(c > 1): c = 1
    if(s < -1): s = -1
    if(c < -1): c = -1
    
    alfa = math.degrees(math.acos(c))
    if(s < 0): alfa *= -1
    
    return(r, alfa)


def cosangle(opp, adj1, adj2):
    # cosangle(1,1,1) => 60, True

    # Cosine rule:
    # C^2 = A^2 + B^2 - 2*A*B*cos(angle_AB)
    # cos(angle_AB) = (A^2 + B^2 - C^2)/(2*A*B)
    # C is opposite
    # A, B are adjacent

    alfa = 0
    direct = True

    den = 2*adj1*adj2
    if(den==0): 
        direct = False
        return alfa, direct

    c = (adj1*adj1 + adj2*adj2 - opp*opp)/den

    if(c>1 or c<-1): 
        direct = False
        return alfa, direct

    alfa = math.degrees(math.acos(c))

    return alfa, direct

arm = 20

def arm2d_2angles(point, l1=arm, l2=arm, rr = 6, debug = True): # for l1 = l2
    # 2 servos in 2D - arm l1, l2
    # diff**2 = l**2 - dist**2
    # dist = distance2(point0_2d, point, 5)
    dist, alfa = cart2polar(point)
    max_dist = (l1 + l2) / math.sqrt(2)
    if debug:
        print("point, arm: ", point, l1)
        print("polar: ", dist, alfa)
        print("max.dist: ", max_dist)
    if dist < max_dist:
        try:
            diff = math.sqrt(l1**2 - dist**2/4)
            epsilon = cosangle(diff, dist/2, l1)[0]
            beta = 2 * cosangle(dist/2, diff, l1)[0]
        except Exception as e:
            print("Err: ", e)

        if debug:
            print("diff: ",diff) 
            print("epsilon: ", epsilon) # temp angle
            print("beta: ", beta)
        return alfa - epsilon, beta
    else:
        print("Err. max distance is ", max_dist)
        return 0, 0
    


def distance3(x1, y1, z1, x2, y2, z2):
    dx = x2 - x1
    dy = y2 - y1
    dz = z2 - z1
    return dx*dx + dy*dy + dz*dz


# test >>>
# print(math.radians(180 / math.pi)) # def 1 rad: 360 / 2pi
# math.degrees(math.pi) # > 180.0
# print(cart2polar(polar2chart(1,90)[0],polar2cart(1,90)[1]))


