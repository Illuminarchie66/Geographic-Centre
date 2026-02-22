class point:
    x = 0
    y = 0
    i = 0
    area = 0
    Cx = 0
    Cy = 0
    
    points = []
    
    def __init__(self, x, y, i):
        self.x = x
        self.y = y
        self.i = i

    def display_coords(self):
        print(self.x, self.y)

    def list_append(self):
        self.points.append([self.x, self.y, self.i])

    def signed_area(self):
        for i in range(0, n-1):
            self.area = self.area + 0.5*((self.points[i][0] * self.points[i+1][1]) - (self.points[i+1][0] * self.points[i][1]))
            print(self.area)
        return abs(self.area)

    def center_x(self):
        for i in range(0, n-1):
            #print("x: " + str(self.Cx))
            self.Cx = self.Cx + ((self.points[i][0] + self.points[i+1][0])*((self.points[i][0] * self.points[i+1][1]) - (self.points[i+1][0] * self.points[i][1])))
        self.Cx = self.Cx*(1/(6*full_area))
        return abs(self.Cx)

    def center_y(self):
        for i in range(0, n-1):
            #print("y: " + str(self.Cy))
            self.Cy = self.Cy + ((self.points[i][1] + self.points[i+1][1])*((self.points[i][0] * self.points[i+1][1]) - (self.points[i+1][0] * self.points[i][1])))
        self.Cy = self.Cy*(1/(6*full_area))
        return abs(self.Cy)

    def distance_check(self):
        for z in range(0, n):
            print("From vertex " + str(z) + ": " + str(((self.points[z][0]-abs(self.Cx))**2 + (self.points[z][1]-abs(self.Cy))**2)**0.5))
   
n = int(input("Enter how many vertices the shape has: "))      
for i in range(0, n):
    input_x = int(input("Enter the x coordinate of the vertex: "))
    input_y = int(input("Enter the y coordinate of the vertex: "))
    
    append_point = point(input_x, input_y, i)
    point.list_append(append_point)

final_point = point(point.points[0][0], point.points[0][1], point.points[0][2]+n)
point.list_append(final_point)

full_area = point.signed_area(append_point)
center_coords = [point.center_x(append_point), point.center_y(append_point)]
print(center_coords)
point.distance_check(append_point)


