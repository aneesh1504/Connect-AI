from cmu_graphics import *
import numpy as np
from circle import Circle
from boardFace import Face
import math

class Board:
    def __init__(self, centerX, centerY, cellSize, app):
        self.rows = app.rows
        self.cols = app.cols
        self.depth = self.cellSize = cellSize
        self.boardWidth = self.cols * self.cellSize
        self.boardHeight = self.rows * self.cellSize
        self.rotationX = 0
        self.rotationY = 0
        self.perspective = 800
        self.centerX = centerX
        self.centerY = centerY
        self.board = app.boardState

        #theme variables
        self.boardFrontColor = app.boardFrontColor
        self.boardBackColor = app.boardBackColor
        self.boardSidesColor = app.boardSidesColor
        self.boardTopBottomColor = app.boardTopBottomColor
        
        self.slotBaseRed = app.slotBaseRed
        self.slotBaseGreen = app.slotBaseGreen
        self.slotBaseBlue = app.slotBaseBlue

        self.highlightColor = app.highlightColor
        self.winningPieceColor = app.winningPieceColor

        #draw 'hole' for piece 
        #allows hole to sit behind 
        # front board layer creating 3D effect
        self.offset = -self.depth/2 
        #creates a pixel border between circles so they are not too close
        self.radius = self.cellSize/2 - self.cellSize/10
        self.circles = []

    #citation: https://www.youtube.com/watch?v=sQDFydEtBLE 
    # inspired by video to implement rotation matrix logic 
    def xRotation(self):
        angle = np.radians(self.rotationX)
        return np.array([
            [1, 0, 0],
            [0, np.cos(angle), -np.sin(angle)],
            [0, np.sin(angle), np.cos(angle)]
        ])

    def yRotation(self):
        angle = np.radians(self.rotationY)
        return np.array([
            [np.cos(angle), 0, np.sin(angle)],
            [0, 1, 0],
            [-np.sin(angle), 0, np.cos(angle)]
        ])

    # Rotate a 3D point by the current board rotations
    def rotatePoint(self, x, y, z):
        Rx = self.xRotation()
        Ry = self.yRotation()
        point = np.array([x,y,z])
        point = Ry @ point
        point = Rx @ point
        return point[0], point[1], point[2]

    # projectPoint only applies perspective projection
    def projectPoint(self, x, y, z):
        scale = float(self.perspective / (self.perspective + z))
        screenX = float(self.centerX + x * scale)
        screenY = float(self.centerY + y * scale)
        return screenX, screenY, scale

    def getCellCoordinates(self,row,col):
        # we want to define 0,0 as center of board
        shiftedCol = col - self.cols/2 + 0.5
        shiftedRow = row - self.rows/2 + 0.5
        xCoordinate = shiftedCol * self.cellSize
        yCoordinate = shiftedRow * self.cellSize
        return xCoordinate, yCoordinate
    
    def screenCoordinates(self, xCoordinate, yCoordinate):
        #get row and column from screen coordinates
        shiftedRow = yCoordinate / self.cellSize
        shiftedCol = xCoordinate / self.cellSize
        col = shiftedCol - 0.5 + self.cols/2
        row = shiftedRow - 0.5 + self.rows/2
        return row, col
    
    #Citation: used Claude 3.5 Sonnet to debug and implement 
    # logic so that circles were not overlapping
    def drawBoard(self, app):
        self.drawBoardFrame()
        self.drawCircles(app)
    
    def drawCircles(self, app):
        array = []
        circles = []
        coins = {}
        for row in range(self.rows):
            for col in range(self.cols):
                x, y = self.getCellCoordinates(row, col)
                array.append((x, y))

                currSlotRedValue = self.slotBaseRed+2*row*col
                currSlotGreenValue = self.slotBaseGreen+2*row*col
                currSlotBlueValue = self.slotBaseBlue+2*row*col

                # slightly vary hole colours across board
                color = rgb(currSlotRedValue, 
                            currSlotGreenValue, 
                            currSlotBlueValue)
                
                hole = Circle(x, y, self.offset, self.radius, color)
                circles.append(hole)

                #check if we need to draw a piece or highlight
                if (app.gameOver and not app.endScreen and app.winner != None 
                    and (row, col) in app.winningPieces):
                    coins[(x,y)] = self.winningPieceColor
                elif app.hintMove != None and (row, col) == app.hintMove:
                    hintCellColor = self.calcCurrentColor(currSlotRedValue,
                                                        currSlotGreenValue,
                                                        currSlotBlueValue,
                                                        app)
                    coins[(x, y)] = hintCellColor
                elif self.board[row, col] is not None:
                    coins[(x,y)] = self.board[row, col]
                elif row == app.projectedRow and col == app.projectedCol:
                    coins[(x,y)] = self.highlightColor

        Rx = self.xRotation()
        Ry = self.yRotation()
        
        for circle in circles:
            #sort circles by depth
            circle.calculateDepth(Rx, Ry)

        circles.sort(key=lambda circle:circle.depth, reverse = True)
        
        for circle in circles:
            #draw
            self.draw3DCircle(circle, circle.color)

            if (circle.x, circle.y) in coins:
                #draw coin at the rotated position
                self.draw3DCircle(circle, coins[(circle.x, circle.y)])
    
        self.circles = circles

    def drawBoardFrame(self):
        x1, y1 = -self.boardWidth/2, -self.boardHeight/2
        x2, y2 =  self.boardWidth/2,  self.boardHeight/2
        depth = -self.depth

        frontFace =  Face(np.array([x1, y1, depth]), 
                  np.array([x2, y1, depth]), 
                  np.array([x2, y2, depth]), 
                  np.array([x1, y2, depth]), 
                  self.boardFrontColor)

        backFace =   Face(np.array([x1, y1, 0]), 
                        np.array([x2, y1, 0]), 
                        np.array([x2, y2, 0]), 
                        np.array([x1, y2, 0]), 
                        self.boardBackColor)

        leftFace =   Face(np.array([x1, y1, 0]), 
                        np.array([x1, y2, 0]), 
                        np.array([x1, y2, depth]), 
                        np.array([x1, y1, depth]), 
                        self.boardSidesColor)

        rightFace =  Face(np.array([x2, y1, 0]), 
                        np.array([x2, y2, 0]), 
                        np.array([x2, y2, depth]), 
                        np.array([x2, y1, depth]), 
                        self.boardSidesColor)

        bottomFace =    Face(np.array([x1, y2, 0]), 
                        np.array([x2, y2, 0]), 
                        np.array([x2, y2, depth]), 
                        np.array([x1, y2, depth]), 
                        self.boardTopBottomColor)

        topFace = Face(np.array([x1, y1, 0]), 
                        np.array([x2, y1, 0]), 
                        np.array([x2, y1, depth]), 
                        np.array([x1, y1, depth]), 
                        self.boardTopBottomColor)

        
        faces = [frontFace, backFace, leftFace, rightFace, topFace, bottomFace]

        Rx = self.xRotation()
        Ry = self.yRotation()

        for face in faces:
            face.calculateAverageDepth(Rx,Ry)

        faces.sort(key=lambda face:face.averageDepth, reverse = True)
        
        for face in faces:
            #rotate before projecting for drawing
            self.draw3DFace(face)

    def drawPiece(self, positionX, positionY, 
                  isSelected, currentColor, color):
            if isSelected:
                borderColor = 'yellow'
            elif currentColor == color: 
                borderColor = self.calcCurrentColor(0,0,0,app)
            else:
                borderColor = None

            drawCircle(positionX, positionY, 
                       self.cellSize/2 - self.cellSize/10, fill= color, 
                       border = borderColor,
                       borderWidth=3)
            
            drawLabel('P1' if color == app.player1PieceColor else 'P2',
                      positionX, positionY, 
                      size = 17, bold = True, font='orbitron')

    
    def draw3DCircle(self, circle, color):
        #project to a screen coordinate
        screenX, screenY, _ = self.projectPoint(circle.rotatedX, 
                                                circle.rotatedY, 
                                                circle.depth)
        drawCircle(screenX, screenY, circle.radius, fill=color)
    
    def draw3DFace(self, face):
        #project to a screen coordinate
        coodinatesToDraw = []
        for point in [face.point1, face.point2, 
                      face.point3, face.point4]:
            x, y, z = self.rotatePoint(point[0], 
                                          point[1], 
                                          point[2])
        
            screenX, screenY, _ = self.projectPoint(x,y,z)
            coodinatesToDraw.extend([screenX, screenY])
    
        drawPolygon(*coodinatesToDraw, fill=face.color)

    def getIsBack(self):
        return (90 < self.rotationY < 270)
    
    def updateBoardState(self, newState):
        self.board = newState

    def calcCurrentColor(self,slotRed,slotGreen,slotBlue,app):
        #white is the hint colour we want to show (255)
        maxValue = 255
        red = (slotRed + (maxValue - slotRed) * 
                (1 + math.sin(app.timeValue))/2)
        green = (slotGreen + (maxValue - slotGreen) * 
                (1 + math.sin(app.timeValue))/2)
        blue = (slotBlue + (maxValue - slotBlue) * 
                (1 + math.sin(app.timeValue))/2)
        return rgb(red,blue,green)
    

