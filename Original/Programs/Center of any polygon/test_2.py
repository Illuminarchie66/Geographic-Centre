import math

v = []
n = int(input("Enter how many vertices the shape has: ")) 

def point_distance(p1, p2):
    return ((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)**0.5

def input_points(v, n):   
    for i in range(0, n):
        input_x = int(input("Enter the x coordinate of the vertex: "))
        input_y = int(input("Enter the y coordinate of the vertex: "))
        v.append([input_x, input_y])

def signed_area(v, n):
    area = 0
    for i in range(0, n-1):
        area += ((v[i][0]*v[i+1][1]) - (v[i+1][0]*v[i][1]))
        print(area)
    area += ((v[n-1][0]*v[0][1])-(v[0][0]*v[n-1][1]))
    area = abs(area*0.5)
    return area

def cyclic_area(v, n):
    a = []
    d = []
    w = [point_distance(v[1], v[3]), point_distance(v[0], v[2])]
    area = 0
    
    for i in range(0, n-1):
        d.append(point_distance(v[i], v[i+1]))
    d.append(point_distance(v[n-1], v[0]))
    print(d)

    for i in range(0, n-1):
        x = int((((-1)**i) + 1)/2)
        a.append(math.acos((d[i+1]**2 - d[i]**2 - w[x]**2)/(-2*d[i]*w[x])))
    a.append(math.acos((d[0]**2 - d[3]**2 - w[1]**2)/(-2*d[3]*w[1])))

    for i in range(0, n):
        area += ((d[i]**2)*math.tan(a[i]))
    print(area)

input_points(v, n)
cyclic_area(v, n)
#print(point_distance(v[0], v[1]))
