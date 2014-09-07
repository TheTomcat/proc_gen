# voronoi.py
from CustomQueue import CustomQueue
from BinaryTree import Node
from graph import *
from PointGenerator import random_2D
import Point
# http://cgm.cs.mcgill.ca/~mcleish/644/Projects/DerekJohns/Sweep.htm
     
class Event(object):
    def __init__(self, other):
        pass
    
##@total_ordering
##__eq__=lambda s,o: s.point.get_loc()[1] == o.point.get_loc()[1]
##__lt__=lambda s,o: s.point.get_loc()[1] < o.point.get_loc()[1]
## This probably isn't needed... will use ordering from Point structure and
## key in CustomQueue
class SiteEvent(Event):
    def __init__(self, Point):
        self.point = Point


class CircleEvent(Event):
    def __init__(self):
        pass

# input a field of points
FieldOfPoints = random_2D([0,0],[10,10],num=20,seed=1)
# Put points in queue
Q = CustomQueue(Point.yx_key)
_ = [Q.put(i) for i in FieldOfPoints]
# default direction is Y from upper to lower (vert)

