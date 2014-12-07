import numpy as np

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Phimap:
    def __init__(self, width=0, height=0):
        self._width = width
        self._height = height
        self._phi = []

    def set_range(self, width, height):
        self._width = width
        self._height = height

    def set_contour(self, center=(0,0), radius=1):
        if not self._width or not self._height:
            raise ValueError('Assign width and height first')

        print('set')

    @property
    def width(self):
        return self._width
    
    @width.setter
    def width(self, width):
        self._width = width

    @property
    def height(self):
        return self._height

    @width.setter
    def height(self, height):
        self._height = height


