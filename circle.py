from cmu_graphics import *
import numpy as np

class Circle:
    def __init__(self, x, y, z, radius, color):
        self.x = x
        self.y = y
        self.z = z
        self.rotatedX = None
        self.rotatedY = None
        self.depth = None
        self.radius = radius 
        self.color = color
        self.depth = 0
        self.height = 4
    
    def calculateDepth(self,Rx,Ry):
        point = np.array([self.x,self.y,self.z])
        point = Ry @ point
        point = Rx @ point
        self.rotatedX, self.rotatedY, self.depth = point
    
    