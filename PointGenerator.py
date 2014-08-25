# PointGenerator.py
import numpy
import math
import random
from Point import *

def _checkInputs(lowerBounds, upperBounds, spacing, number, testDim=None):
    if testDim is None:
        testDim = len(lowerBounds)
    if not (testDim == len(lowerBounds) == len(upperBounds)):
        raise(TypeError("All supplied arguments must be iterables of the same length."))
    if spacing is None and number is None:
        raise(TypeError("Must specify either spacing or number and not both."))
    if spacing is not None and number is not None:
        raise(TypeError("Must specify either spacing or number and not both."))
    if spacing is None:
        if len(number) != testDim:
            raise(TypeError("All supplied arguments must be iterables of the same length."))  
    if number is None:
        if len(spacing)!=2:
            raise(TypeError("All supplied arguments must be iterables of the same length."))

def cart_2D(lowerBounds, upperBounds, spacing=None, number=None):
    points = []
    _checkInputs(lowerBounds, upperBounds, spacing, number, 2)
    
    if number is None:
        number = [math.floor((u-l)/s)+1 for l,u,s in zip(lowerBounds,upperBounds,spacing)]
        
##    print(lowerBounds, upperBounds, number, spacing)
    for x in numpy.linspace(lowerBounds[0], upperBounds[0], num=number[0]):
        for y in numpy.linspace(lowerBounds[1], upperBounds[1], num=number[1]):
            points.append(Point([x,y]))
    return points

def perterbed_cart_2D(lowerBounds, upperBounds, spacing=None, number=None, r=0.1, seed=None):
    points = cart_2D(lowerBounds, upperBounds, spacing, number)
    random.seed(seed)
    for point in points:
        r_x = r * (2*random.random()-1)
        r_y = r * (2*random.random()-1)
        point.move((r_x, r_y))
    return points

def random_2D(lowerBounds, upperBounds, numPoints=50, seed=None):
    random.seed(seed)
    r = random.random
    points = []
    if not (2 == len(lowerBounds) == len(upperBounds)):
        raise(TypeError("lowerBounds and upperBounds must be iterables of length 2."))
    for i in range(numPoints):
        points.append(Point([l+r()*(u-l) for l,u in zip(lowerBounds, upperBounds)]))
    return points

def lloyd_relaxation(points):
    pass
