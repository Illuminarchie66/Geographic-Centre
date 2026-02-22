import math
R = 6371

def geodetic_to_cartesian(lat, long):
    rlat = math.radians(lat)
    rlong = math.radians(long)
    x = R*math.cos(rlat)*math.cos(rlong)
    y = R*math.cos(rlat)*math.sin(rlong)
    z = R*math.sin(rlat)
    return x, y, z

def cartesian_to_geodetic(x, y, z):
    rlat = math.asin(z/R)
    rlong = math.atan2(y,x)
    lat = math.degrees(rlat)
    long = math.degrees(rlong)
    return lat, long

def greatcircle_definition(x1, y1, z1, x2, y2, z2):
    a = y1*z1 - z1*y2
    b = z1*x2 - x1*z2
    c = x1*y2 - y1*x2
    return a, b, c

def greatcircle_intersect(a1, b1, c1, a2, b2, c2):     
    h = (a2*c1 - c2*a1)/(b2*a1 - a2*b1)
    g = (-b1*h - c1)/(a1)
    k =  math.sqrt((R**2)/(g**2 + h**2 + 1))

    x = g*k
    y = h*k
    z = k
    
    return cartesian_to_geodetic(x, y, z)
