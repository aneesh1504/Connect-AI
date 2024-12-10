from cmu_graphics import *
import numpy as np

class Face:
    def __init__(self, point1, point2, point3, point4, color):
        self.point1 = point1
        self.point2 = point2
        self.point3 = point3
        self.point4 = point4
        self.averageDepth = None
        self.color = color
    
    def calculateAverageDepth(self,Rx,Ry):
        depths = []
        for point in [self.point1, self.point2, self.point3, self.point4]:
            point = Ry @ point
            point = Rx @ point
            depths.append(point[2])
        self.averageDepth = sum(depths)/len(depths)
    
    