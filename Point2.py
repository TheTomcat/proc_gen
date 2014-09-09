# Point.py
import numpy, math
import functools
import itertools


class _Space(object):
    def __init__(self):
        pass
    def add(self, p1, p2):
        raise NotImplementedError
    def sub(self, p1, p2):
        raise NotImplementedError
    def mul(self, p1, p2):
        raise NotImplementedError

class _Euclidean(_Space):
    def __init__(self):
        pass
    def add(Point1, Point2):
        return Point(Point1.get_loc() + Point2.get_loc())
    def sub(Point1, Point2):
        return Point(Point1.get_loc() - Point2.get_loc())
    def mul(Point1, r):
        if isinstance(r, (int, float)):
            return Point(r*Point1.get_loc())
        else:
            raise(TypeError("Cannot multiply Point by non-scalar."))
    def dot(Point1, Point2):
        return sum([i*j for i,j in zip(Point1.get_loc(), Point2.get_loc())])
    def bisect(Point1, Point2):
        return Point1 + 0.5*(Point2-Point1)
    mag_key = lambda P: [P.mag2()]
    xyz_key = lambda P: list(P.get_loc())
    yx_key = lambda P: [-P.get_loc()[1], P.get_loc()[0]]


Euclidean = _Euclidean
##Sphere = _Spherical

@functools.total_ordering
class Point(object):
##    newid = itertools.count()
    def __init__(self, loc, space=Euclidean):
        self._coordinate = numpy.array(loc)
        self._dim=len(loc)
##        self.index = next(Point.newid)
        for attr in dir(space):
            if attr[0:2]=="__":
                continue
            self.__setattr__(attr, space.__getattribute__(attr))
    @classmethod
    def fromscalars(cls, *args):
        return cls(args)
    
    def set_loc(self, loc, dimChange=False):
        if len(loc) != self._dim and not dimChange:
            raise(IndexError("Wrong number of dimensions."))
        self._coordinate = numpy.array(loc)
        self._dim = len(loc)        
    def get_loc(self):
        return self._coordinate
    def move(self, peterbment):
        self._coordinate = self._coordinate + numpy.array(peterbment)
    def scale(self, r):
        self._coordinate = mul(self._coordinate, r)
    def __repr__(self):
        return "Point([" + ", ".join([str(i) for i in self._coordinate]) + "])"
##    __add__ = space.add
##    __sub__ = space.sub
##    __mul__ = space.mul
    __rmul__=lambda self, other: self.__mul__(other)
    __eq__=lambda self, other: all(self._coordinate == other._coordinate)
    __ne__=lambda self, other: not self.__eq__(other)
    __lt__=lambda self, other: self.mag2() < other.mag2()

    def close(self, other, tol=0.01):
        return math.fabs(self.mag2() - other.mag2()) <= tol*tol
    def mag(self):
        return math.sqrt(self.mag2())
    def mag2(self):
        return sum(i*i for i in self._coordinate)
    def dim(self):
        return self._dim
    def same_dim(self, other):
        return self._dim == other._dim
    
##class Field(object):
##    def __init__(self, localDimensions, globalDimensions):
##        self._localDim = localDimensions
##        self._globalDim = globalDimensions
##    #def checkLocal(self, Point):
##        blah
##    def setLocalLimits(self, namedTuple):
##        blah
