import numpy as np

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Phimap:
    def __init__(self, width=0, height=0):
        if not width or not height:
            return

        self._width = width
        self._height = height
        self._phi = []

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


