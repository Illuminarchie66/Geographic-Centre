import numpy as np

def perpendicularBisector(p1, p2):
    midpoint = [(p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2]
    if p2[1] - p1[1] == 0:
        gradient = "infinity"
        c_value = midpoint[0]
    else:
        gradient = -(p2[0] - p1[0]) / (p2[1] - p1[1])
        c_value = midpoint[1] - gradient*midpoint[0]

    return [gradient, c_value]

def intersect(l1, l2):
    if l1[0] == l2[0]:
        return "No intersects"
    else:
        if l1[0] == "infinity":
            x = l1[1]
            y = l2[0]*x + l2[1]
        elif l2[0] == "infinity":
            x = l2[1]
            y = l1[0] * x + l1[1]
        else:
            x = (l2[1] - l1[1]) / (l1[0] - l2[0])
            y = l1[0]*x +l1[1]

        return [x,y]

def centre4(pointlist):
    linelist = []
    newpointlist = []
    for i in range(3):
        linelist.append(perpendicularBisector(pointlist[i], pointlist[i+1]))
    linelist.append(perpendicularBisector(pointlist[3], pointlist[0]))

    for i in range(3):
        newpointlist.append(intersect(linelist[i], linelist[i+1]))
    newpointlist.append(intersect(linelist[3], linelist[0]))


    roundedlist = np.around(newpointlist, -4)
    if all(np.all(elem == roundedlist[0]) for elem in roundedlist) == True:
        return newpointlist
    else:
        print("yes")
        return centre4(newpointlist)

def distance(p1, p2):
    x = p2[0] - p1[0]
    y = p2[1] - p1[1]
    dist = (x**2 + y**2)**0.5
    return dist

pointlist = [[-6,0], [10,5], [1,9], [5, 4]]
cntr = centre4(pointlist)
print(cntr)

for i in range(4):
    print(distance(cntr[i], pointlist[i]))







