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
"""


def distance2(x1, y1, x2, y2, rr = 3):
    # default round rr
    dx = x2 - x1
    dy = y2 - y1
    return round(math.sqrt(dx*dx + dy*dy), rr)


def polar2cart(r, alfa, rr = 3):
    x = r * math.cos(math.radians(alfa))
    y = r * math.sin(math.radians(alfa))
    return round(x, rr), round(y, rr)


def cart2polar(x, y):
    r = distance2(0, 0, x, y)
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


def distance3(x1, y1, z1, x2, y2, z2):
    dx = x2 - x1
    dy = y2 - y1
    dz = z2 - z1
    return dx*dx + dy*dy + dz*dz


# test

print(math.radians(180 / math.pi)) # def 1 rad: 360 / 2pi
# math.degrees(math.pi) > 180.0

print(cart2polar(polar2chart(1,90)[0],polar2cart(1,90)[1]))


