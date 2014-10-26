import numpy as np
import matplotlib.mlab as mlab

class Gaussian_model:
    def __init__(self, mean, std, start=0, end=500):
        self.mean = mean
        self.std = std
        self.start = start
        self.end = end

        scale =  np.arange(start, end, 1)

        self.probility = mlab.normpdf(scale, mean, std)

    def getProb(self, val):
        if val <= self.end and val >= self.start: 
            return self.probility[val]
