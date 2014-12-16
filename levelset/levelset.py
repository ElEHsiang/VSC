# -*- coding: utf-8 -*-

from itertools import cycle

import numpy as np
import scipy as sp
import scipy.ndimage

_P2 = [np.eye(3), np.array([[0,1,0]] * 3), np.flipud(np.eye(3)), np.rot90([[0,1,0]] * 3)]

class Fcycle(object):
    def __init__(self, iterable):
        self.func = cycle(iterable)

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

def IS(u):
    global _aux
    if np.ndim(u) == 2:
        P = _P2


class LevelSetSolver():
    """Level set solver

    Attributes:
    _I: image data, 2d numpy array
    _gI: gradient of _I
    _smooth: smooth factor
    _threshold: mask threhold, determine level set affect region
    _balloon: balloon force
    """

    def __init__(self, image, smooth=1, threshold=0, balloon=0):
        """Create a level set solver

        Args:
        image: image data, 2d numpy array
        smoothing: smoothing factor
        threshold: mask threhold, determine level set affect region
        balloon: balloon force
        """
        if type(image) is not np.ndarray:
            raise(TypeError, "image must be numpy ndarray")

        self._u = None
        self._I = image
        self._dI = np.gradient(self._I)
        self._smooth = smooth
        self._threshold = threshold
        self._balloon = balloon

        self._gI = self._gborder(self._I/255.0, alpha=1000, sigma=5.48)
        self._dgI = np.gradient(self._gI)

        dim = np.ndim(image)
        self.structure = scipy.ndimage.generate_binary_structure(dim, 2)

        self._update_mask()

    def set_levelset(self, u):
        self._u = np.double(u)

    @staticmethod
    def circle_levelset(shape, center, sqradius):
        R, C = np.mgrid[:shape[0], :shape[1]]
        phi = sqradius - (np.sqrt((R - center[0])**2) + (C - center[0])**2)
        u = np.float_(phi > 0)
        return u

    def _update_mask(self):
        """Compute mask to speed up."""
        self._mask = self._gI > self._threshold
        self._mask_v = self._gI > self._threshold/np.abs(self._balloon)

    def _gborder(self, img, alpha=1.0, sigma=1.0):
        """Compute g(I) energy"""
        grad_norm = scipy.ndimage.gaussian_gradient_magnitude(img, sigma, mode="constant")
        return 1.0/np.sqrt(1.0 + alpha * grad_norm)

    def step(self):
        """A single step of level set"""

        u = self._u
        gI = self._gI
        dI = self._dI
        dgI = self._dgI
        threhold = self._threshold
        balloon = self._balloon

        if u is None:
            raise ValueError("The levelset is not set")

        res = np.copy(u)

        #count next u(t+1) position
        if balloon > 0:
            aux = scipy.ndimage.binary_dilation(u, self.structure)
        elif balloon < 0:
            aux = scipy.ndimage.binary_erosion(u, self.structure)
        #only consider u in mask
        if balloon != 0:
            res[self._mask_v] = aux[self._mask_v]

        aux = np.zeros_like(res)
        #count gradient of u
        dres = np.gradient(res)
        for e11, e12 in zip(dgI, dres):
            aux += e11 * e12
        res[aux > 0] = 1
        res[aux < 0] = 0

        self._u = res

        return self._u
