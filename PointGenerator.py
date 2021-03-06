# PointGenerator.py
import numpy
import math
import random
from Point import *

def _checkInputs(lowerBounds, upperBounds, spacing, num, testDim=None):
    if testDim is None:
        testDim = len(lowerBounds)
    if not (testDim == len(lowerBounds) == len(upperBounds)):
        raise(TypeError("All supplied arguments must be iterables of the same length."))
    if spacing is None and num is None:
        raise(TypeError("Must specify either spacing or number and not both."))
    if spacing is not None and num is not None:
        raise(TypeError("Must specify either spacing or number and not both."))
    if spacing is None:
        if len(num) != testDim:
            raise(TypeError("All supplied arguments must be iterables of the same length."))  
    if num is None:
        if len(spacing)!=2:
            raise(TypeError("All supplied arguments must be iterables of the same length."))

def cart_2D(lowerBounds, upperBounds, spacing=None, num=None):
    _checkInputs(lowerBounds, upperBounds, spacing, num, 2)
    if num is None:
        num = [math.floor((u-l)/s)+1 for l,u,s in zip(lowerBounds,upperBounds,spacing)]
    for x in numpy.linspace(lowerBounds[0], upperBounds[0], num=num[0]):
        for y in numpy.linspace(lowerBounds[1], upperBounds[1], num=num[1]):
            yield Point([x,y])

def perterbed_cart_2D(lowerBounds, upperBounds, spacing=None, num=None, r=0.1, seed=None):
    grid_points = cart_2D(lowerBounds, upperBounds, spacing, num, return_iterator=True)
    random.seed(seed)
    for point in grid_points:
        r_x = r * (2*random.random()-1)
        r_y = r * (2*random.random()-1)
        point.move((r_x, r_y))
        yield point

def random_2D(lowerBounds, upperBounds, num=20, seed=None):
    random.seed(seed)
    r = random.random
    points = []
    if not (2 == len(lowerBounds) == len(upperBounds)):
        raise(TypeError("lowerBounds and upperBounds must be iterables of length 2."))
    for i in range(num):
        yield Point([l+r()*(u-l) for l,u in zip(lowerBounds, upperBounds)])

def lloyd_relaxation(points):
    pass
