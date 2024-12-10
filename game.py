from board import Board
from minimax import minimaxAlgorithm
import random

class Game:
    def __init__(self,app):
        self.board = app.board
        self.lastMove = (0,0)
        self.moveCount = 0
        self.timeElapsed = 0
        self.lastColor = None
        self.moveList = []
    
    def getBoardPosition(self, app, mouseX, mouseY):
        array = []
        #find which column we're dropping into
        potentialCol = None
        #set a large number that is greater than height of board 
        #so that any row on board in that column will be identified
        minDistance = 100000
        
        for circle in app.board.circles:
            screenX, _, _ = app.board.projectPoint(
                circle.x, circle.y, -app.board.depth/2)
            if (mouseX - (app.board.radius) <= 
                screenX < mouseX + (app.board.radius)):
                row, col = app.board.screenCoordinates(circle.x, circle.y)
                col = int(col)
                #track the closest column to the mouse
                distance = abs(screenX - mouseX)
                if distance < minDistance:
                    minDistance = distance
                    potentialCol = col

        if potentialCol is not None:
            if app.board.getIsBack():
                potentialCol = (app.cols - 1) - potentialCol
            possibleLocation = self.findLowestRow(potentialCol,
                                                  app.boardState, app)
            if possibleLocation != None:
                row,col = possibleLocation
                return row, col           
        return None
    
    def findLowestRow(self, potentialCol, board, app):
        #find the lowest empty position in this column, starting from
        #bottom row
        for row in range(app.rows-1, -1, -1):
            if board[row, potentialCol] == None:
                return row, potentialCol   
            
    def makeMove(self, mouseX, mouseY, app):
        app.projectedRow = None
        app.projectedCol = None
        position = self.getBoardPosition(app, mouseX, mouseY)
        if position != None:
            row, col = position
            if app.player1PieceSelected:
                app.boardState[row, col] = app.player1PieceColor
                self.lastColor = app.player1PieceColor
                app.player1PieceSelected = False
                app.finalAngle = 180
            elif app.player2PieceSelected:
                app.boardState[row, col] = app.player2PieceColor
                self.lastColor = app.player2PieceColor
                app.player2PieceSelected = False
                app.finalAngle = 0
            self.moveCount += 1
            self.lastMove = (row,col, self.lastColor)
            self.moveList.append(self.lastMove)
            self.switchTurns(app)
        else:
            app.player1PieceSelected = False
            app.player2PieceSelected = False

        if app.computer and app.currentPlayer == 2:
            gameOver = self.gameOverState(position, app)
            if (position != None and app.rotating and
                not gameOver):
                app.computerTurn = True
        return position
    
    def getHint(self,app):
        if app.currentPlayer == 1:
            hintMove = minimaxAlgorithm(app.boardState, 
                                                    3, 
                                                    -10000, 10000,
                                                    app.player1PieceColor,
                                                    True, app)
        else:
            hintMove = minimaxAlgorithm(app.boardState, 
                                                    3, 
                                                    -10000, 10000,
                                                    app.player2PieceColor,
                                                    True, app)
    
        if hintMove != None:
                    row, col, _ = hintMove
        return row, col

    def makeComputerMove(self, app):
        if not app.rotating:
            #probability of choosing a random move instead of using minimax
            #depending on difficulty
            if app.computerDifficulty == 1:
                randomness = 0.4
            elif app.computerDifficulty == 2:
                randomness = 0.15
            elif app.computerDifficulty == 3:
                randomness = 0.03
            
            #play piece in random row and column if random number picked
            #between 0 and 1 is within randomness value else use minximax to play
            if random.random() <= randomness:
                validLocations = self.getValidLocations(app.boardState, app)
                col = random.choice(validLocations)
                row, col = self.findLowestRow(col, app.boardState, app)
                self.lastMove = (row, col, app.player2PieceColor)
            else:
                #minimax depth is set to chosen difficulty 
                computerMove = minimaxAlgorithm(app.boardState, 
                                                app.computerDifficulty, 
                                                -10000, 10000,
                                                app.player2PieceColor,
                                                True, app)
                if computerMove != None:
                    row, col, _ = computerMove
                    self.lastMove = (row, col, app.player2PieceColor)
            
            self.moveList.append(self.lastMove)
                    
            computerMove = row, col
            app.boardState[row, col] = app.player2PieceColor
            self.moveCount += 1
            self.switchTurns(app)
            return row, col


    def switchTurns(self,app):
        if app.currentPlayer == 1:
            app.currentPlayer = 2
        else:
            app.currentPlayer = 1
    
    def checkGameDraw(self, board, app):
        for row in range(0, app.rows):
            for col in range(0, app.cols):
                if board[row, col] == None:
                    return False
        return True
        
    def checkGameWin(self, currRow, currCol, board, app):
        color = board[currRow][currCol]
        for dx in range(-1,2):
            for dy in range(-1,2):
                pieces = {(currRow, currCol)}
                pieceCount = 1
                if dx == 0 and dy == 0:
                    continue

                newRow = currRow + dx
                newCol = currCol + dy

                #check forward direction
                while (0 <= newRow < app.rows and 
                       0 <= newCol < app.cols and 
                       board[newRow, newCol] == color):
                    pieces.add((newRow, newCol))
                    pieceCount += 1
                    newRow += dx
                    newCol += dy
                
                newRow = currRow - dx
                newCol = currCol - dy

                #check backward direction
                while (0 <= newRow < app.rows and 
                       0 <= newCol < app.cols and 
                       board[newRow, newCol] == color):
                    pieces.add((newRow, newCol))
                    pieceCount += 1
                    newRow -= dx
                    newCol -= dy
                #if 4 pieces are in a row in given direction return 
                #their coordinates
                if pieceCount >= 4:
                    return pieces
        return None
    
    def gameOverState(self, move, app):
        row, col = move
        pieces = app.game.checkGameWin(row, col, app.boardState, app)
        if pieces != None:
            app.winningPieces = pieces
            app.gameOver = True
            #rotate to winner's side of board, current player is NOT winner
            # as makeMove has switched player
            if app.currentPlayer == 2:
                app.winner = 1
                app.finalAngle = 0 
            elif app.currentPlayer == 1:
                app.winner = 2
                app.finalAngle = 180
            return True
        if app.game.checkGameDraw(app.boardState, app):
            app.gameOver = True
            app.winner = None 
            return True
        app.rotating = True
        return False
    
    #get list of columns that are not full
    def getValidLocations(self, board, app):
        validLocations = []
        for col in range(0, app.cols):
            currCol = board[:, col]
            if currCol[0] == None:
                validLocations.append(col)
        return validLocations