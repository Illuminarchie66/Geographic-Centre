def createOmega(self, pointlist, C):
    omega = 0
    for i in range(0, len(pointlist)):
        V = pointlist[i].cartesian
        K = np.matrix([[(V[1] ** 2 + V[2] ** 2), -1 * V[0] * V[1], -1 * V[0] * V[2]],
                       [-1 * V[0] * V[1], (V[0] ** 2 + V[2] ** 2), -1 * V[1] * V[2]],
                       [-1 * V[0] * V[2], -1 * V[1] * V[2], (V[0] ** 2 + V[1] ** 2)]])
        scalar1 = 1 / ((np.linalg.norm(C) ** 2) * (np.linalg.norm(V) ** 2))
        scalar2 = np.dot(V, C) / np.linalg.norm(np.cross(V, C))
        omega = omega + scalar1 * scalar2 * K

    return omega


def createDelta(self, pointlist, C):
    delta = 0
    for i in range(0, len(pointlist)):
        V = pointlist[i].cartesian
        scalar1 = np.linalg.norm(np.cross(V, C)) / ((np.linalg.norm(C) ** 2) * (np.linalg.norm(V) ** 2))
        delta = delta + scalar1 * V

    return delta


def centreN(self, pointlist, C):
    omega = self.createOmega(pointlist, C)
    delta = self.createDelta(pointlist, C)

    invomega = np.linalg.inv(omega)
    centre = np.dot(invomega, delta).tolist()[0]
    t_coeffecient = R / np.linalg.norm(centre)
    midpoint = t_coeffecient*centre

    return Point.fromCartesian(centre)




def osum1(self, pointlist, centrepoint):
    C = centrepoint.cartesian
    sum = 0
    for i in range(0, len(pointlist)):
        V = pointlist[i].cartesian
        K = np.matrix([[(V[1] ** 2 + V[2] ** 2), -1 * V[0] * V[1], -1 * V[0] * V[2]],
                        [-1 * V[0] * V[1], (V[0] ** 2 + V[2] ** 2), -1 * V[1] * V[2]],
                        [-1 * V[0] * V[2], -1 * V[1] * V[2], (V[0] ** 2 + V[1] ** 2)]])
        scalar1 = (1/R) * self.arcdistance(pointlist[i], centrepoint)
        scalar2 = 1 / np.dot(V, C)**2
        scalar3 = np.dot(V, C) / np.linalg.norm(np.cross(V, C))
        vector1 = scalar3 * np.dot(K, C)
        vector2 = np.linalg.norm(np.cross(V, C)) * V
        vector3 = (vector1 - vector2)
        total = scalar1 * scalar2 * vector3
        sum = sum + total
    sum = sum * len(pointlist)

    return sum

def osum2(self, pointlist, centrepoint):
    C = centrepoint.cartesian
    sum = 0
    for i in range(0, len(pointlist)):
        V = pointlist[i].cartesian
        total = (1/R)*self.arcdistance(pointlist[i], centrepoint)
        sum = sum + total

    return sum

def osum3(self, pointlist, centrepoint):
    C = centrepoint.cartesian
    sum = 0
    for i in range(0, len(pointlist)):
        V = pointlist[i].cartesian
        scalar1 = np.linalg.norm(np.cross(V, C)) / ((np.linalg.norm(V) ** 2) * (np.linalg.norm(C) ** 2))
        total = scalar1 * V
        sum = sum + total

    return sum

def createOmega(self, pointlist, centrepoint):
    C = centrepoint.cartesian
    omega = 0
    for i in range(0, len(pointlist)):
        V = pointlist[i].cartesian
        K = np.matrix([[(V[1] ** 2 + V[2] ** 2), -1 * V[0] * V[1], -1 * V[0] * V[2]],
                        [-1 * V[0] * V[1], (V[0] ** 2 + V[2] ** 2), -1 * V[1] * V[2]],
                        [-1 * V[0] * V[2], -1 * V[1] * V[2], (V[0] ** 2 + V[1] ** 2)]])
        scalar1 = 1 / ((np.linalg.norm(C) ** 2) * (np.linalg.norm(V) ** 2))
        scalar2 = np.dot(V, C) / np.linalg.norm(np.cross(V, C))
        total = scalar1 * scalar2 * K
        omega = omega + total

    return omega

def oldcentreN(self, pointlist, C):
    sum1 = self.sum1(pointlist, C)
    sum2 = self.sum2(pointlist, C)
    sum3 = self.sum3(pointlist, C)
    omega = self.createOmega(pointlist, C)

    inverse = np.linalg.inv(omega)
    vector1 = ((1 / sum2) * sum1).tolist()[0] + sum3
    centre = np.dot(inverse, vector1)

    return centre


def s1(self, V, C):
    s1 = 1 / ((np.linalg.norm(V.cartesian) ** 2) * (np.linalg.norm(C.cartesian) ** 2))
    return s1

def s2(self, V, C):
    s2 = np.dot(V.cartesian, C.cartesian) / np.linalg.norm(np.cross(V.cartesian, C.cartesian))
    return s2

def s3(self, V, C):
    s3 = np.linalg.norm(np.cross(V.cartesian, C.cartesian))
    return s3

def K(self, point):
    X = point.cartesian
    K = np.matrix([[(X[1] ** 2 + X[2] ** 2), -1 * X[0] * X[1], -1 * X[0] * X[2]],
                    [-1 * X[0] * X[1], (X[0] ** 2 + X[2] ** 2), -1 * X[1] * X[2]],
                    [-1 * X[0] * X[2], -1 * X[1] * X[2], (X[0] ** 2 + X[1] ** 2)]])
    return K

def l(self, V, C):
    cross = np.cross(V.cartesian, C.cartesian)
    dot = np.dot(V.cartesian, C.cartesian)
    temp = np.linalg.norm(cross) / dot

    l = math.atan(temp)
    return l

def sum1(self, pointlist, C):
    sum = 0
    for i in range(0, len(pointlist)):
        V = pointlist[i]
        temp = self.l(V, C) * self.s1(V, C) * self.s3(V, C) * V.cartesian
        sum = sum + temp

    sum = sum * len(pointlist)
    return sum

def sum2(self, pointlist, C):
    sum1 = 0
    sum2 = 0
    for i in range(0, len(pointlist)):
        V = pointlist[i]
        temp1 = self.l(V, C)
        sum1 = sum1 + temp1

    for i in range(0, len(pointlist)):
        V = pointlist[i]
        temp2 = self.s1(V, C) * self.s3(V, C) * V.cartesian
        sum2 = sum2 + temp2

    sum = sum1 * sum2
    return sum

def sum3(self, pointlist, C):
    sum = 0
    for i in range(0, len(pointlist)):
        V = pointlist[i]
        K = self.K(V)
        temp = self.l(V, C) * self.s1(V, C) * self.s2(V, C) * K
        sum = sum + temp

    sum = sum * len(pointlist)
    return sum

def sum4(self, pointlist, C):
    sum1 = 0
    sum2 = 0
    for i in range(0, len(pointlist)):
        V = pointlist[i]
        K = self.K(V)
        temp1 = self.l(V, C)
        temp2 = self.s1(V, C) * self.s2(V, C) * K
        sum1 = sum1 + temp1
        sum2 = sum2 + temp2

    sum = sum1 * sum2
    return sum

def centreN(self, pointlist, C):
    #print("s1", self.sum1(pointlist, C))
    #print("s2", self.sum2(pointlist, C))
    print("s3", self.sum3(pointlist, C))
    print("s4", self.sum4(pointlist, C))
    vector = self.sum1(pointlist, C) - self.sum2(pointlist, C)
    omega = self.sum3(pointlist, C) - self.sum4(pointlist, C)
    inverse = np.linalg.inv(omega)

    centre = np.dot(inverse, vector)
    return Point.fromCartesian(centre.tolist())