import math #for square roots and trignometric functions
import numpy as np #for matrix and vector calculations
import requests #for accessing google api data
import json #for accessing the json data from the api
import urllib #for accessing the image from the google maps static images
import sys
import re #for the use of regex to regulate inputs
from PyQt5.QtWidgets import * #for the GUI
from PyQt5.QtGui import * #for the GUI
from PyQt5.Qt import QWheelEvent #for the zoom function
from PyQt5 import QtCore #for PyQt5
from PyQt5.QtCore import *
from gmaps import Geocoding #for the geocoding function
import time #for debugging time taken

with open('API-KEY.txt') as f:
    Key = f.readline()
    f.close()
#This just keeps my API Key in a seperate folder so it can't be seen when I upload this for the project

api = Geocoding(api_key = Key)
R = 6371
base_url = "https://maps.googleapis.com/maps/api/geocode/json"
#Main constants of the program, the api, the radius of the Earth, and a base endpoint url

class Point:
    cartesian = np.array([]) #[x, y, z]
    polar = [] #[latitude, longitude]
    postcode = str() #address string
    #the three ways location can be desrcibed

    def __init__(self, cartesian, polar, postcode):
        self.cartesian = cartesian
        self.polar = polar
        self.postcode = postcode

    @classmethod
    def fromPolar(cls, polar):
        lat = math.radians(polar[0])
        lng = math.radians(polar[1])

        x = R * math.cos(lat)*math.cos(lng)
        y = R * math.cos(lat)*math.sin(lng)
        z = R * math.sin(lat)
        #finds the x, y and z coordinates from polar coordinates

        endpoint = f"{base_url}?latlng={polar[0]}, {polar[1]}&key={Key}"
        r = requests.get(endpoint)
        json_data = json.loads(r.text)
        if json_data['status'] == "OK":
            postcode = json_data['results'][0]['address_components'][0]['long_name']
            #retrieves the json data and ensures an address exists, if it defines this variable
        else:
            postcode = "None"
            #the status isn't considered OK, meaning there is no address avaliable to retrieve


        return cls(np.array([x, y, z]), polar, postcode)

    @classmethod
    def fromCartesian(cls, cartesian):
        lat = math.degrees(math.asin(cartesian[2] / R))
        lng = math.degrees(math.atan2(cartesian[1], cartesian[0]))
        #finds the lat and lng from cartesian coordinates

        endpoint = f"{base_url}?latlng={lat}, {lng}&key={Key}"
        r = requests.get(endpoint)
        json_data = json.loads(r.text)
        if json_data['status'] == "OK":
            postcode = json_data['results'][0]['address_components'][0]['long_name']
            #retrieves the json data and ensures an address exists, if it defines this variable
        else:
            postcode = "None"
            #the status isn't considered OK, meaning there is no address avaliable to retrieve

        return cls(np.array(cartesian), [lat, lng], postcode)

    @classmethod
    def fromAddress(cls, postcode):

        endpoint = f"{base_url}?address={postcode}&key={Key}"
        r = requests.get(endpoint)
        json_data = json.loads(r.text)
        #gathers json data for an input

        if json_data['status'] == "OK":
            lat = json_data['results'][0]['geometry']['location']['lat']
            lng = json_data['results'][0]['geometry']['location']['lng']
            polar = [lat, lng]

            x = R * math.cos(math.radians(lat)) * math.cos(math.radians(lng))
            y = R * math.cos(math.radians(lat)) * math.sin(math.radians(lng))
            z = R * math.sin(math.radians(lat))
            #finds the cartesian coordinates and the polar coordinates

            return cls(np.array([x, y, z]), polar, postcode)
        else:
            return False
            #returns false to signify there was some error occured from the address input

class Map:
    zoom = int() #refers to the zoom of the image
    maptype = str() #refers to the map type of the image: satellite, roadmap, hybrid, terrain
    pointlist = [] #a list of the point objects on the map
    url = str() #the url to retrieve an image from
    iterationlist = [] #list of markers to iterate

    def __init__(self, zoom, maptype, centre, pointlist):
        self.zoom = zoom
        self.maptype = maptype
        self.centre = centre
        self.pointlist = pointlist

    def centre2(self, P1, P2):
        lat1 = math.radians(P1.polar[0])
        lng1 = math.radians(P1.polar[1])
        lat2 = math.radians(P2.polar[0])
        lng2 = math.radians(P2.polar[1])
        #defines latitude and longitude seperately so it doesn't need to find it in radians very time

        Bx = math.cos(lat2) * math.cos(lng2 - lng1)
        By = math.cos(lat2) * math.sin(lng2 - lng1)

        midlat = math.atan2(math.sin(lat1) + math.sin(lat2), math.sqrt((math.cos(lat1) + Bx) ** 2 + By ** 2))
        midlng = lng1 + math.atan2(By, math.cos(lat1) + Bx)
        #performs the calculations necessary to find the middle latitude and middle longitude

        midpoint = Point.fromPolar([math.degrees(midlat), math.degrees(midlng)])
        #returns the midpoint which is a point object, as to keep the standard of everything being a point whenever possible

        return midpoint

    def centre3(self):
        P1 = self.pointlist[0]
        P2 = self.pointlist[1]
        P3 = self.pointlist[2]
        #defines the points as shorter to write objects

        perpendicular1 = self.createPerpendicular(P1, P2)
        perpendicular2 = self.createPerpendicular(P1, P3)
        #finds the perpendicular planes between P1 and P2, and P1 and P3

        y_coefficient = -((perpendicular1[0]*perpendicular2[2] - perpendicular1[2]*perpendicular2[0]) / (perpendicular1[1]*perpendicular2[2] - perpendicular1[2]*perpendicular2[1]))
        z_coeffecient = -((perpendicular1[0]*perpendicular2[1] - perpendicular1[1]*perpendicular2[0]) / (perpendicular1[2]*perpendicular2[1] - perpendicular1[1]*perpendicular2[2]))
        #parameterizes the line equation and rearranges them to solve them with x^2 + y^2 + z^2 = R

        t_coeffecient = 1 + y_coefficient**2 + z_coeffecient**2
        t = math.sqrt((R**2)*(1/t_coeffecient))
        midpoint = Point.fromCartesian([t, t*y_coefficient, t*z_coeffecient])
        # finds the parameter that brings the coordinates to the sphere to return them as the standard output

        return midpoint

    def createPerpendicular(self, point1, point2):
        plane = np.cross(point1.cartesian, point2.cartesian)
        #plane where point1, point2 and the origin are coplanar
        centre = self.centre2(point1, point2)
        #the midpoint between point 1 and point2

        perpendicular = np.cross(plane, centre.cartesian)
        #finds a vector perpendicular to the plane's normal vector, at the midpoint
        return perpendicular

    def coplanar(self):
        P1 = self.pointlist[0]
        P2 = self.pointlist[1]
        equal = 0
        perpendicular = np.cross(P1.cartesian, P2.cartesian) #the normal vector
        checkval = np.dot(P1.cartesian, perpendicular) #constant value to define the plane
        for V in self.pointlist:
            if np.dot(V.cartesian, perpendicular) != checkval: #r.n = d
                equal = equal + 1

        if equal != 0:
            return False #not coplanar
        else:
            return True #coplanar

    def arcdistance(self, point1, point2):
        cross = np.cross(point1.cartesian, point2.cartesian)
        dot = np.dot(point1.cartesian, point2.cartesian)
        temp = np.linalg.norm(cross) / dot
        sigma = math.atan(temp)
        #formula of sigma = atan(|VxC|/V.C) using the numpy library with linalg which I still don't know what it stands for

        if sigma == 0 and (point1.cartesian[0] != point2.cartesian[0] or point1.cartesian[1] != point2.cartesian[1] or point1.cartesian[2] != point2.cartesian[2]):
            distance = R * np.pi
            #in the case where point1 is parallel to point2 but point1 != point2, as specified by comparing cartesian coords
        else:
            distance = R * sigma
            #in every other case, even including when dot = 0, as atan(inf) = pi/2

        return distance

    def varianceCheck(self, C):
        mean = 0
        variance = 0
        for V in self.pointlist:
            mean = mean + self.arcdistance(C, V)
        mean = mean/len(self.pointlist)
        for V in self.pointlist:
            variance = variance + (self.arcdistance(C, V) - mean)**2
        variance = variance/len(self.pointlist)
        #using the standard definition of variance = sum of data - mean squared divided by number of data points squared

        return variance

    def distanceCheck(self, C):
        for V in self.pointlist:
            print("Distance: " + str(self.arcdistance(C, V)))
        #an easier way of seeing all of the distances to a point from a map object's pointlist

    def summationCheck(self, C):
        total = 0
        for V in self.pointlist:
            total = total + abs(self.arcdistance(C, V))
        #takes the absolute of arcdistance as to avoid negative distances when finding the total
        return total

    def s1(self, V, C): #Scalar
        s1 = 1 / ((np.linalg.norm(V.cartesian) ** 2) * (np.linalg.norm(C.cartesian) ** 2))
        #s1=1/(|V||C|)^2
        #its own function as its reused so much
        return s1

    def s2(self, V, C): #Scalar
        s2 = np.dot(V.cartesian, C.cartesian) / np.linalg.norm(np.cross(V.cartesian, C.cartesian))
        #s2=V.C/|VxC|
        #its own function as its reused so much
        return s2

    def s3(self, V, C): #Scalar
        s3 = np.linalg.norm(np.cross(V.cartesian, C.cartesian))
        #s3=|VxC|
        #its own function as its reused so much
        return s3

    def l(self, V, C): #Scalar
        cross = np.cross(V.cartesian, C.cartesian)
        dot = np.dot(V.cartesian, C.cartesian)
        temp = np.linalg.norm(cross) / dot

        l = math.atan(temp)
        return l

    def K(self, V): #Matrix
        X = V.cartesian
        K = np.array([[(X[1] ** 2 + X[2] ** 2), -1 * X[0] * X[1], -1 * X[0] * X[2]],
                       [-1 * X[0] * X[1], (X[0] ** 2 + X[2] ** 2), -1 * X[1] * X[2]],
                       [-1 * X[0] * X[2], -1 * X[1] * X[2], (X[0] ** 2 + X[1] ** 2)]])
        #uses a numpy 3x3 matrix as derived in formula
        return K

    #all of these functions are representitive of how I made the problem I was solving simpler
    #when performing the proof of the derivative of the variance of arclength I represented a series of scalars and matricies in a more concise form so I could solve for C
    #as there was room for error for scribing the formulae to computational form

    def createOmega1(self, C): #Matrix
        omega = np.array([[0, 0, 0],
                          [0, 0, 0],
                          [0, 0, 0]])
        for V in self.pointlist:
            l = self.l(V, C)
            s1 = self.s1(V, C)
            s2 = self.s2(V, C)
            K = self.K(V)
            omega = omega + l * s1 * s2 * K
            #summation of matricies with the previously established functions

        return omega

    def createOmega2(self, C): #Matrix
        omega = np.array([[0, 0, 0],
                          [0, 0, 0],
                          [0, 0, 0]])
        n = len(self.pointlist)
        lsum = 0
        for V in self.pointlist:
            l = self.l(V, C)
            lsum = lsum + l
            #summation of scalars of the arclength to be multiplied at the end

        for V in self.pointlist:
            s1 = self.s1(V, C)
            s2 = self.s2(V, C)
            K = self.K(V)
            omega = omega + s1 * s2 * K
            #summation of matricies with the previously established functions

        return (lsum / n) * omega

    def createDelta1(self, C): #Vector
        delta = np.array([0, 0, 0])
        for V in self.pointlist:
            l = self.l(V, C)
            s1 = self.s1(V, C)
            s3 = self.s3(V, C)
            delta = delta + l * s1 * s3 * V.cartesian
            #summation of vectors with the previoussly established functions

        return delta

    def createDelta2(self, C): #Vector
        delta = np.array([0, 0, 0])
        n = len(self.pointlist)
        lsum = 0
        for V in self.pointlist:
            l = self.l(V, C)
            lsum = lsum + l
            #summation of scalars of the arclength to be multiplied at the end
        for V in self.pointlist:
            s1 = self.s1(V, C)
            s3 = self.s3(V, C)
            delta = delta + s1 * s3 * V.cartesian
            #summation of vectors with the previoussly established functions

        return (lsum / n) * delta

    def centreN1(self, C):
        omega1 = self.createOmega1(C)
        omega2 = self.createOmega2(C)
        delta1 = self.createDelta1(C)
        delta2 = self.createDelta2(C)
        #once again sets up key variables as to avoid confusion

        invomega = np.linalg.inv(omega1)
        temp = np.matmul(omega2, C.cartesian) - delta2 + delta1
        M = np.matmul(invomega, temp)
        #seperates the C value and uses the fact M*M^-1 = I, to find a vector

        t_coeffecient = R / np.linalg.norm(M)
        C = t_coeffecient * M
        #returns the vector to the surface of the sphere

        return Point.fromCartesian(C)

    def centreN2(self, C):
        omega1 = self.createOmega1(C)
        omega2 = self.createOmega2(C)
        delta1 = self.createDelta1(C)
        delta2 = self.createDelta2(C)
        #once again sets up key variables as to avoid confusion

        invomega = np.linalg.inv(omega2)
        temp = np.matmul(omega1, C.cartesian) - delta1 + delta2
        M = np.matmul(invomega, temp)
        #seperates the C value and uses the fact M*M^-1 = I, to find a vector

        t_coeffecient = R / np.linalg.norm(M)
        C = t_coeffecient * M
        #returns the vector to the surface of the sphere

        return Point.fromCartesian(C)

    def minimumDistanceTravelled(self, C):
        omega = np.array([[0, 0, 0],
                          [0, 0, 0],
                          [0, 0, 0]])
        delta = np.array([0, 0, 0])
        for V in self.pointlist:
            s1 = self.s1(V, C)
            s2 = self.s2(V, C)
            K = self.K(V)
            s3 = self.s3(V, C)

            omega = omega + s1 * s2 * K #Matrix
            delta = delta + s3 * V.cartesian #Vector

        invomega = np.linalg.inv(omega)
        M = np.matmul(invomega, delta)
        #similar seperation process just  simplified to two terms of delta and omega

        t_coeffecient = R / np.linalg.norm(M)
        C = t_coeffecient * M
        #returns the vector to the surface of the sphere

        return Point.fromCartesian(C)

    def polarAverage(self):
        lataverage = 0
        lngaverage = 0
        for V in self.pointlist:
            lataverage = lataverage + V.polar[0]
            lngaverage = lngaverage + V.polar[1]

        #uses linear method of averaging the points to return a polar array

        return [lataverage/len(self.pointlist), lngaverage/len(self.pointlist)]

    def centreMethod(self):
        original = 0
        temp1 = 0
        temp2 = 0

        M1 = []
        M2 = []
        #instantiates the arrays and variables to store iterations and tests

        C = Point.fromPolar(self.polarAverage()) #starting approximation
        original = self.varianceCheck(C)
        for i in range(5):
            C = self.centreN1(C)
        temp1 = self.varianceCheck(C)

        C = Point.fromPolar(self.polarAverage())
        for i in range(5):
            C = self.centreN2(C)
        temp2 = self.varianceCheck(C)
        #for both methods it sees if it decreases or inceases the variance as it does in an iterative formula tending toward the maximum or minimum

        C = Point.fromPolar(self.polarAverage())

        if temp1 <= original and temp2 >= original: #case where method 1 variance is decreasing and method 2 is increasing
            return 1
        elif temp2 <= original and temp1 >= original: #case where method 2 variance is decreasing and method 1 is increasing
            return 2
        elif temp1 <= original and temp2 <= original: #case where variance is decreasing for both methods
            print("Unknown")
            return 1
        else: #variance is increasing for both methods
            print("Non existent point")

    def returnImage(self):
        if len(self.pointlist) == 0: #no markers
            self.url = f"http://maps.googleapis.com/maps/api/staticmap?center={str(self.centre.polar[0])},{str(self.centre.polar[1])}&scale=2&size=800x450&key={Key}&zoom={str(self.zoom)}&maptype={self.maptype}&sensor=false"
        elif len(self.pointlist) > 3 or len(self.iterationlist) > 0: #if there needs to be iterations added to the final image or not
            self.url = f"http://maps.googleapis.com/maps/api/staticmap?center={str(self.centre.polar[0])},{str(self.centre.polar[1])}&scale=2&size=800x450&key={Key}&zoom={str(self.zoom)}&maptype={self.maptype}&markers=size:large%color:red%7Clabel:M%7C{str(self.centre.polar[0])},{str(self.centre.polar[1])}&sensor=false"
            for I in self.iterationlist:
                self.url = self.url + f"&markers=size:tiny%7Ccolor:green%7C{str(I.polar[0])},{str(I.polar[1])}" #why url is an attribute as it can constantly be updated and called
        else:
            self.url = f"http://maps.googleapis.com/maps/api/staticmap?center={str(self.centre.polar[0])},{str(self.centre.polar[1])}&scale=2&size=800x450&key={Key}&zoom={str(self.zoom)}&maptype={self.maptype}&markers=size:mid%color:red%7Clabel:M%7C{str(self.centre.polar[0])},{str(self.centre.polar[1])}&sensor=false"

        for V in self.pointlist:
            self.url = self.url + f"&markers=color:blue%7Clabel:S%7C{str(V.polar[0])},{str(V.polar[1])}"

        urllib.request.urlretrieve(self.url, "map1.jpg") #uses urllib to retrieve the image under the name map.jpg

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Centre of N points'
        self.left = 0
        self.top = 0
        self.width = 1920
        self.height = 1080 #dimensions of most normal computer screens
        self.map = ""
        self.n = 0
        self.accuracy = 100 #default accuracy the program uses
        self.textboxarray = []
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.map = Map(6, "terrain", Point.fromPolar([0,0]), [])
        #the instrance of the map object the program uses

        self.map.returnImage()
        self.label = QLabel(self)
        pixmap = QPixmap('map1.jpg')
        self.label.setPixmap(pixmap)
        self.label.move(400, 20)
        #displays the initial image

        self.centreText = QLabel("The centre of these points are:                                                                            ", self)
        self.centreText.move(800, 920)
        #simple display of text beneath the image

        self.satellite = QCheckBox('Satellite', self)
        self.satellite.move(1828, 10)
        self.satellite.stateChanged.connect(self.state_changed)
        self.satellite.setLayoutDirection(Qt.RightToLeft)
        self.roadmap = QCheckBox('Roadmap', self)
        self.roadmap.move(1820, 30)
        self.roadmap.stateChanged.connect(self.state_changed)
        self.roadmap.setLayoutDirection(Qt.RightToLeft)
        #sets up the two checkboxes of satellite imagery and roadmap imagery

        self.iteration = QCheckBox('Iterations', self)
        self.iteration.move(1820, 70)
        self.iteration.setLayoutDirection(Qt.RightToLeft)
        self.minimization = QCheckBox('Smallest sum', self)
        self.minimization.move(1797, 50)
        self.minimization.setLayoutDirection(Qt.RightToLeft)
        #sets up the two checkboxes of iteration mode and the smallest sum mode

        self.widget = QWidget(self)
        self.addb = QPushButton(self.widget)
        self.addb.setText("+")
        self.addb.setGeometry(160, 20, 24, 24)
        self.addb.clicked.connect(self.addbox)
        self.subb = QPushButton(self.widget)
        self.subb.setText("-")
        self.subb.setGeometry(185, 20, 24, 24)
        self.subb.clicked.connect(self.removebox)
        #sets up the two buttons to add and remove textboxes

        self.accuracytext = QLabel("Accuracy:", self)
        self.accuracytext.move(1770, 870)

        self.accuracybox = QLineEdit("100", self)
        self.accuracybox.move(1770, 890)
        self.accuracybox.returnPressed.connect(self.on_returnPressed)
        self.accuracybox.show()
        #sets up the textbox to input the new accuracy

        self.addbox()
        #adds in the first textbox

        self.show()

    def addbox(self):
        self.textbox = QLineEdit(self)
        self.textbox.move(20, 50 + (self.n -1)*30) #adds in text boxes always 30 pixels apart using an nth term
        self.textbox.returnPressed.connect(self.on_returnPressed)
        self.textbox.show()
        self.textboxarray.append(self.textbox)
        self.n = self.n + 1 #the number of textboxes

    def removebox(self):
        if self.n > 1: #checking there is always at least one textbox
            self.textboxarray[self.n -1].deleteLater() #deletes a widget
            del self.textboxarray[self.n -1]
            self.n = self.n - 1
            self.show()

    def newImgLoad(self):
        self.map.returnImage()
        pixmap = QPixmap('map1.jpg')
        self.label.setPixmap(pixmap)
        self.label.update()
        #updates the current image with the new image retrieved from returnImage()

    def iterations(self, method, detail, C):
        if self.iteration.isChecked():
            self.map.iterationlist.append(C)
            #this adds in the initial starting point marker
        for i in range(self.accuracy):
            #print(C.polar)
            #print(detail(C))
            C = method(C)
            #this does the repeated method specified in the function, repeating accuracy number of times
            if self.iteration.isChecked():
                if i < 10:
                    self.map.iterationlist.append(C)
                else:
                    if (i / 10).is_integer():
                        self.map.iterationlist.append(C)
                #this takes an iteration marker every 10 iterations so that it doesn't take as much time to process the image
                #it will show the first 10 iterations as that is usually when the most change happens
        return C

    def on_returnPressed(self):
        start = time.time()
        self.map.iterationlist.clear()
        self.map.pointlist.clear()
        #empties the pointlist and iterationlist from any previous sessions
        polarCheck = re.compile("^[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?),\s*[-+]?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)$") #the regex for polar coordinates
        if self.accuracybox.text() != "": #only changes accuracy if the textbox is altered
            self.accuracy = int(self.accuracybox.text())

        for box in self.textboxarray:
            text = box.text()
            if text != "": #only considers it a point to add if the textbox isnt empty
                if polarCheck.match(text) != None:
                    polar = text.split(", ") #splits it up into the polar form
                    P = Point.fromPolar([int(polar[0]), int(polar[1])]) #makes the point from polar coords
                    self.map.pointlist.append(P)
                elif Point.fromAddress(text) != False: #if a valid address is inputted it will not return false
                    self.map.pointlist.append(Point.fromAddress(text)) #makes the point from an address
                else:
                    print("Formatting error")

        if  self.minimization.isChecked(): #if it is selected to do the total minimum distance formula
            self.map.centre = self.iterations(self.map.minimumDistanceTravelled, self.map.summationCheck, Point.fromPolar(self.map.polarAverage()))

        elif not self.minimization.isChecked():
            if len(self.map.pointlist) >= 3:
                if self.map.coplanar() == False: #the points don't lie on the same great circle

                    if len(self.map.pointlist) == 3: #makes sure points are not coplanar
                        self.map.centre = self.map.centre3()
                        print(self.map.varianceCheck(self.map.centre))
                        print(self.map.summationCheck(self.map.centre))

                    else:
                        method = self.map.centreMethod()
                        if method == 1: #method 1 has decreasing variance
                            self.map.centre = self.iterations(self.map.centreN1, self.map.varianceCheck, Point.fromPolar(self.map.polarAverage()))
                        elif method == 2: #method 2 has decreasing variance
                            self.map.centre = self.iterations(self.map.centreN2, self.map.varianceCheck, Point.fromPolar(self.map.polarAverage()))
                        else:
                            print("Invalid Point") #Discloses point doesn't exist

                else: #all points lie on a great circle
                    print("normal")
                    normal = np.cross(self.map.pointlist[0].cartesian, self.map.pointlist[1].cartesian)
                    t_coeffecient = R / np.linalg.norm(normal)
                    self.map.centre = Point.fromCartesian(t_coeffecient * normal)

            else:
                if len(self.map.pointlist) == 1:
                    self.map.centre = self.map.pointlist[0]  # the centre of 1 point is itself

                if len(self.map.pointlist) == 2:
                    self.map.centre = self.map.centre2(self.map.pointlist[0],
                                                       self.map.pointlist[1])  # centre of 2 points
                    print(self.map.varianceCheck(self.map.centre))


        self.newImgLoad() #loads in the new image
        roundedLat = "{:.10f}".format(self.map.centre.polar[0])
        roundedLog = "{:.10f}".format(self.map.centre.polar[1])
        self.centreText.setText(f"The centre of these points are: {roundedLat}, {roundedLog}")
        #takes the first 10 values of the string of the polar coords of the point it has found

        end = time.time()

        print(f"Runtime of the program is {end - start}")

        self.update()

    def state_changed(self):
        if self.satellite.isChecked() and not self.roadmap.isChecked():
            self.map.maptype = "satellite" #satellite image
        elif self.roadmap.isChecked() and not self.satellite.isChecked():
            self.map.maptype = "roadmap" #roadmap image
        elif self.roadmap.isChecked() and self.satellite.isChecked():
            self.map.maptype = "hybrid" #hybrid image
        elif not self.roadmap.isChecked() and not self.satellite.isChecked():
            self.map.maptype = "terrain" #terrain image

        self.newImgLoad() #loads in the new image with updated maptype

    def wheelEvent(self, event: QWheelEvent):
        delta = event.angleDelta().y()/120 #can only be 1 or -1
        if self.map.zoom > 0: #lets user increase zoom
            self.map.zoom = int(self.map.zoom + delta)
        elif self.map.zoom == 0 and delta == 1: #lets user increase when theyre at minimum zoom
            self.map.zoom = int(self.map.zoom + delta)
        elif self.map.zoom < 0:
            self.map.zoom = 0 #ensures zoom can never be less than 0
        self.newImgLoad() #loads in the new image with updated zoom

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())




