import numpy as np
import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Phimap:
    def __init__(self, width, height):
        self.contour = []
        self.contour_gradient = []
        self.width = width
        self.height = height

        self.phi = np.ones((width, height))
        self.mask = np.zeros((width, height))

    def add_contour( contour ):
        """Add contour into phi map and count distance function"""
        if type(contour) is not list:
            print('input is not a list')

        try:
            for p in contour:
                self.phi[p.x][p.y] = 0
                self.contour.append(p)
        except AttributeError:
            print('list must store point')
            self.phi = np.ones((width, height))
            self.contour = []
        except :
            print('Unknown Error')
            self.phi = np.ones((width, height))
            self.contour = []

        self._count_distance()

    def _count_distance(self):
        """Count distance from conour with 5x5 window, set compute mask"""
        self.mask = np.zeros((self.width, self.height))

        for p in self.contour:
            for x in range(-2, 3): #[-2, -1, 0, 1, 2]
                for y in range(-2, 3): #[-2, -1, 0, 1, 2]
                    temp = Point(p.x + x, p.y + y)
                    if not self._valid_point(temp):
                        continue

                    self.phi[temp.x][temp.y] = math.sqrt((temp.x - p.x)*(temp.x - p.x) + (temp.y - p.y)*(temp.y - p.y))
                    self.mask[p.y][p.y] = 1

    def _count_contour_gradient(self):
        """Count gradient for contour"""
        self.contour_gradient = []
        for p in self.contour:
            x = self.phi[p.x + 1][p.y] - self.phi[p.x - 1][y]
            y = self.phi[p.x][p.y + 1] - self.phi[p][y - 1]
            gradient = np.array((x, y))
            self.contour_gradient.append(gradient)


    def _valid_point(self, p):
        """Check Point is valid in map."""
        if p.x >= 0 and p.x < self.width and p.y >= 0 and p.y < self.height:
            return True
        else:
            return False

    def _norm(self, vector):
        """Return L2 norm of vector"""
        value = 0
        for x in vector:
            value += x*x
        return math.sqrt(value)

