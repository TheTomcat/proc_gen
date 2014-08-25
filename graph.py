# graph.py
import numpy, math
from Point import *

class Environment(object):
    def __init__(self, loc):
        self._environment = {}
    def set_environment(self, env, setas):
        self._environment[environment]=setas
    def get_environment(self, environment):
        if environment in self._environment:
            return self._environment[environment]
        else:
            raise(KeyError)

class Center(Point, Environment):
    # x index
    # v coordinate
    # v BiomeData (bool lists)
    # x Moisture and Elevation (perlin driven)
    # v Neighbours (list of Centers)
    # v Borders (list of Edges)
    # v Corners (list of Corners)
    def __init__(self, loc):
        super().__init__(loc)
        self._Borders = []
        self._Neighbours = []
        self._Corners = []
    def addNeighbour(self, neighbour):
        if not isinstance(neighbour, Center):
            raise(TypeError)
        self._Neighbours.append(neighbour)
        neighbour._Neighbours.append(self)
    def addBorder(self, border):
        self._Borders.append(border)
    def addCorner(self, corner):
        self._Corners.append(corner)
    def Neighbours(self):
        return self._Neighbours
    def Corners(self):
        return self._Corners
    def Borders(self):
        return self._Borders

class Corner(Point, Environment):
    # x index
    # v coordinate
    # v BiomeData (bool list) --> From Environment
    # x Moisture and Elevation (perlin driven)
    # v Touches (list of Centers)
    # v Protrudes (list of Edges)
    # v Adjacent (list of Corners)
    # o River 0 if no river, or volume of water in river
    # o downslope (Corner) adjacent down-hill corner
    # o watershed (Corner) coastal corner or None
    # o watershed size (int)
    def __init__(self, loc):
        super().__init__(loc)
        self._Touches = []
        self._Protrudes = []
        self._Adjacent = []

    def addTouching(self, center):
        self._Touches.append(center)
    def addProtruding(self, edge):
        self._Protrudes.append(edge)
    def addAdjacent(self, corner):
        self._Adjacent.append(corner)
    def Touching(self):
        return self._Touches
    def Protruding(self):
        return self._Protrudes
    def Adjacent(self):
        return self._Adjacent
    ## Not complete

class Edge(object):
    def __init__(self, loc):
        pass
    def setDelaunayEdge(self, d0, d1):
        if not isinstance(d0, Center) or not isinstance(d1, Center):
            raise(TypeError)
        self._delaunay = [d0,d1]
    def setVoronoiEdge(self, v0, v1):
        if not isinstance(v0, Corner) or not isinstance(v1, Corner):
            raise(TypeError)
        self._voronoi = [v0, v1]
        self._midpoint = bisect(v0,v1)
    

