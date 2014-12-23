import numpy as  np

class model:
    def __init__(self, file_path):
        with open(file_path, 'r') as f:
            lines = f.readlines()
            mid = [i for i, x in enumerate(lines) if x == '\n']
            contour = lines[:mid[0]]
            contour = list(map(lambda x: x[:-1].split(' '), contour))
            self.contour = np.array([list(map(int, x[:-1])) for x in contour])

            variance = lines[mid[0] + 1:]
            variance = list(map(lambda x: x[:-1].split(' '), variance))
            self.variance = np.array([list(map(int, x[:-1])) for x in variace])
            print(self.contour)

    @property
    def contour(self):
        return self.contour

    @property
    def variance(self):
        return self.variance


