from Point import Point
from flask import jsonify
import numpy as np

R = 6371

class Centre_Calculator:

    def __init__(self, socketio):
        self.socketio = socketio

    def centre(self, V, sid, experimental=False, alpha=1, precision=10, track=10, balanced=False, verbose=True):
        print("balanced: " + str(balanced))
        if len(V) < 1:
            return None

        if experimental:
            print("Centre N")
            return self.centreN(V, sid, alpha, 10**-precision, track, balanced)

        if len(V) == 1:
            print("Centre 1")
            return V[0]
        elif len(V) == 2:
            print("Centre 2")
            return self.centre2(V[0], V[1])
        elif len(V) == 3:
            print("Centre 3")
            return self.centre3(V[0], V[1], V[2])
        else:
            print("Centre N")
            return self.centreN(V, sid, alpha, 10**-precision, track, balanced)

    def centre2(self, P1, P2):
        lat1 = np.radians(P1.polar[0])
        lng1 = np.radians(P1.polar[1])
        lat2 = np.radians(P2.polar[0])
        lng2 = np.radians(P2.polar[1])

        Bx = np.cos(lat2) * np.cos(lng2 - lng1)
        By = np.cos(lat2) * np.sin(lng2 - lng1)

        midlat = np.atan2(np.sin(lat1) + np.sin(lat2), np.sqrt((np.cos(lat1) + Bx) ** 2 + By ** 2))
        midlng = lng1 + np.atan2(By, np.cos(lat1) + Bx)

        midpoint = Point.fromPolar([np.degrees(midlat), np.degrees(midlng)])

        return midpoint
    
    def centre3(self, P1, P2, P3):
    
        def createPerpendicular(point1, point2):
            plane = np.cross(point1.cartesian, point2.cartesian)
            #plane where point1, point2 and the origin are coplanar
            centre = self.centre2(point1, point2)
            #the midpoint between point 1 and point2

            perpendicular = np.cross(plane, centre.cartesian)
            #finds a vector perpendicular to the plane's normal vector, at the midpoint
            return perpendicular

        perpendicular1 = createPerpendicular(P1, P2)
        perpendicular2 = createPerpendicular(P1, P3)

        y_coefficient = -((perpendicular1[0]*perpendicular2[2] - perpendicular1[2]*perpendicular2[0]) / (perpendicular1[1]*perpendicular2[2] - perpendicular1[2]*perpendicular2[1]))
        z_coeffecient = -((perpendicular1[0]*perpendicular2[1] - perpendicular1[1]*perpendicular2[0]) / (perpendicular1[2]*perpendicular2[1] - perpendicular1[1]*perpendicular2[2]))
        
        t_coeffecient = 1 + y_coefficient**2 + z_coeffecient**2
        t = np.sqrt((R**2)*(1/t_coeffecient))
        midpoint = Point.fromCartesian([t, t*y_coefficient, t*z_coeffecient])

        return midpoint
    
    def coplanar(self, vertexlist):
        P1 = vertexlist[0]
        P2 = vertexlist[1]
        perpendicular = np.cross(P1.cartesian, P2.cartesian) #the normal vector
        checkval = np.dot(P1.cartesian, perpendicular) #constant value to define the plane
        for V in vertexlist:
            if np.dot(V.cartesian, perpendicular) != checkval: #r.n = d
                return False
        return True
    
    def variance_gradient(self, C, V, K):
        n = len(V)
        cross_product = [0]*n
        dot_product = [0]*n
        inverse_div = [0]*n
        inverse_sum = [0]*n
        arctan = [0]*n

        s1 = 0
        s2 = 0
        s3 = 0

        for i in range(0, n):
            cross_product[i] = np.linalg.norm(np.cross(V[i].normal, C))
            dot_product[i] = np.dot(V[i].normal, C)
            arctan[i] = np.arctan(cross_product[i]/dot_product[i] )
            inverse_div[i] = dot_product[i]/cross_product[i]
            inverse_sum[i] = 1/(np.square(cross_product[i]) + np.square(dot_product[i]))

            temp = inverse_sum[i]*(inverse_div[i]*(K[i]@C) - (cross_product[i]*V[i].normal))
            s1 += arctan[i]*temp
            s2 += arctan[i]
            s3 += temp

        return 2*((1/n)*s1 - (1/np.square(n))*s2*s3)

    def balanced_gradient(self, C, V, K, alpha):
        n = len(V)
        cross_product = [0]*n
        dot_product = [0]*n
        inverse_div = [0]*n
        inverse_sum = [0]*n
        arctan = [0]*n

        s1 = 0
        s2 = 0
        s3 = 0

        for i in range(0, n):
            cross_product[i] = np.linalg.norm(np.cross(V[i].normal, C))
            dot_product[i] = np.dot(V[i].normal, C)
            arctan[i] = np.arctan(cross_product[i]/dot_product[i] )
            inverse_div[i] = dot_product[i]/cross_product[i]
            inverse_sum[i] = 1/(np.square(cross_product[i]) + np.square(dot_product[i]))

            temp = inverse_sum[i]*(inverse_div[i]*(K[i]@C) - (cross_product[i]*V[i].normal))
            s1 += arctan[i]*temp
            s2 += arctan[i]
            s3 += temp

        return 2*alpha[0]*((1/n)*s1 - (1/np.square(n))*s2*s3) + alpha[1]*(10**-3)*s3

    def centreN(self, V, sid, alpha=1, precision=1e-10, track=10, balanced=False):
        K = []
        n = len(V)

        avg = [0,0]
        for i in range(0, n):
            avg[0] += V[i].polar[0]
            avg[1] += V[i].polar[1]
        avg[0] = avg[0]/n
        avg[1] = avg[1]/n

        self.updateIterations(sid, avg)

        C_next = Point.fromPolar(avg).normal
        C = C_next + np.random.normal(scale=1e-2, size=C_next.shape)

        def K_matrix(V): #Matrix
            X = V.normal
            return np.array([[(X[1] ** 2 + X[2] ** 2), -1 * X[0] * X[1], -1 * X[0] * X[2]],
                        [-1 * X[0] * X[1], (X[0] ** 2 + X[2] ** 2), -1 * X[1] * X[2]],
                        [-1 * X[0] * X[2], -1 * X[1] * X[2], (X[0] ** 2 + X[1] ** 2)]])
        
        for i in range(0, n):
            K.append(K_matrix(V[i]))

        counter = 0
        while not np.allclose(C, C_next, atol=precision):
            if counter > 10000:
                break

            C = C_next
            counter += 1

            if counter % track == 0:
                lat = np.degrees(np.asin(C[2]))
                lng = np.degrees(np.atan2(C[1], C[0]))
                self.updateIterations(sid, [float(lat), float(lng)])

            if balanced:
                delta = self.balanced_gradient(C, V, K, [0.25, 0.75])
            else:    
                delta = self.variance_gradient(C, V, K)

            C_next = C - alpha*delta

        return Point.fromCartesian(R*C)

    def arcdistance(self, P1, P2):
        cross = np.linalg.norm(np.cross(P1.cartesian, P2.cartesian))
        dot = np.dot(P1.cartesian, P2.cartesian)
        sigma = np.arctan(cross/dot)

        if sigma == 0 and (P1.cartesian[0] != P2.cartesian[0] or P1.cartesian[1] != P2.cartesian[1] or P1.cartesian[2] != P2.cartesian[2]):
            return R * np.pi
            #in the case where point1 is parallel to point2 but point1 != point2, as specified by comparing cartesian coords
        else:
            return R * sigma
        
    def arcvariance(self, C, V):
        n = len(V)
        arctan = [0]*n
        mean = 0
        for i in range(0, n):
            arctan[i] = self.arcdistance(C, V[i])
            mean += arctan[i]
        mean = mean/n

        var = 0
        for i in range(0, n):
            var += np.square(arctan[i]-mean)
        return var/n
        
    def format(self, C, V):
        string = "Distances:\n["
        for i in range(0,len(V)):
            string += "\n  " + str(self.arcdistance(C,V[i]))
        string += "\n]\n"
        string += "Variance: " + str(self.arcvariance(C,V))
        return string
        
    def updateIterations(self, sid, iteration):
        # Emit the updated item to the client
        self.socketio.emit('updated_iterations', 
                           {'iteration': {'latitude': iteration[0], 'longitude': iteration[1]}},
                           room=sid)
