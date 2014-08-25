# graph.py
import numpy, math
from Point import *

class EnvironmentalPoint(Point):
    def __init__(self, loc):
        super().__init__(loc)
        self._environment = {}
    def set_environment(self, env, setas):
        self._environment[environment]=setas
    def get_environment(self, environment):
        if environment in self._environment:
            return self._environment[environment]
        else:
            raise(KeyError)

class Center(EnvironmentalPoint):
    # index
    # coordinate
    # BiomeData (bool lists)
    # Moisture and Elevation (perlin driven)
    # Neighbours (list of Centers)
    # Borders (list of Edges)
    # Corners (list of Corners)
    def __init__(self, loc):
        super().__init__(loc)
        self._Borders = []
        self._Neighbours = []
        self._Corners = []
    def addNeighbour(self, neighbour):
        self._Neighbours.append(neighbour)
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

class Corner(EnvironmentalPoint):
    # index
    # coordinate
    # BiomeData (bool list)
    # Moisture and Elevation (perlin driven)
    # Touches (list of Centers)
    # Protrudes (list of Edges)
    # Adjacent (list of Corners)
    # River 0 if no river, or volume of water in river
    # downslope (Corner) adjacent down-hill corner
    # watershed (Corner) coastal corner or None
    # watershed size (int)
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
        self._delaunay = [d0,d1]
    def setVoronoiEdge(self, v0, v1):
        self._voronoi = [v0, v1]
        self._midpoint = bisect(v0,v1)
    
    
