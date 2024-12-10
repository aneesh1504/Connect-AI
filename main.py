from cmu_graphics import *
from board import Board
from game import Game
from screens import *
import numpy as np
import time

def onAppStart(app):
    #initialize all static variables
    app.cols = 7
    app.rows = 6
    app.width = 800
    app.height = 600
    #can be modified for bigger board
    app.cellSize = 50
    app.rotationSpeed = 0.3 

    app.player1PositionX = 30
    app.player1PositionY = 40

    app.player2PositionX = 30
    app.player2PositionY = 90
    app.titleOffset = 0
    app.timeValue = 0
    #buttons
    app.instructionsX = app.instructionsY = app.startX = app.themesX = 400
    app.instructionsWidth, app.instructionsHeight = 300, 60

    app.themesY = 315
    
    app.oceanThemeX =  app.sunsetThemeX = 5*app.width/16
    app.oceanThemeY = app.forestThemeY = 3*app.height/8
    app.forestThemeX = app.lavenderThemeX = 11*app.width/16
    app.sunsetThemeY = app.lavenderThemeY = 5*app.height/8

    app.themeWidth = app.width / 3.5
    app.themeHeight = app.height / 8

    app.startY = 485
    app.startWidth, app.startHeight = 300, 60
    app.themesWidth, app.themesHeight = 300, 60
    app.horizontalWinX = app.verticalWinX = app.diagonalWinX = app.width/4
    app.horizontalWinY = 370
    app.horizontalWinWidth, app.horizontalWinHeight = 125, 40

    app.verticalWinY = 440
    app.verticalWinWidth, app.verticalWinHeight = 125, 40

    app.diagonalWinY = 510
    app.diagonalWinWidth, app.diagonalWinHeight = 125, 40

    app.multiplayerX = 5*app.width/16
    app.computerX = 11*app.width/16
    app.multiplayerY = app.computerY = app.height/2

    app.multiplayerWidth = app.computerWidth = app.width/3
    app.multiplayerHeight = app.computerHeight = app.height/8

    app.easyDifficultyX = 2*app.width/8
    app.mediumDifficultyX = 4*app.width/8
    app.hardDifficultyX = 6*app.width/8

    app.easyDifficultyY = app.mediumDifficultyY = app.hardDifficultyY = 3*app.height/4
    
    app.easyDifficultyWidth = app.mediumDifficultyWidth = app.hardDifficultyWidth = app.width/6
    
    app.easyDifficultyHeight = app.mediumDifficultyHeight = app.hardDifficultyHeight = app.height/12

    app.hintX = 90
    app.hintY = 550

    app.hintWidth = 100
    app.hintHeight = 50

    app.homeX = app.width - 40
    app.homeY = 40
    app.homeWidth = 40
    app.homeHeight = 40

    #theme variables that need to stay constant even if home is pressed
    app.player1PieceColor = gradient(rgb(255, 0, 0), 
                                     rgb(200, 0, 0), start='center')
    app.player2PieceColor = gradient(rgb(255, 255, 0), 
                                     rgb(200, 200, 0), start='center')
    app.boardFrontColor = gradient(rgb(210, 180, 140), 
                                    rgb(160, 130, 90), start='center')
    app.boardBackColor = gradient(rgb(190, 160, 120), 
                                   rgb(140, 110, 70), start='center')
    app.boardSidesColor = gradient(rgb(139, 69, 19), 
                                   rgb(90, 50, 10), start='center')
    app.boardTopBottomColor = gradient(rgb(205, 133, 63), 
                                       rgb(150, 100, 50), start='center')
    
    app.slotBaseRed = 120
    app.slotBaseGreen = 120
    app.slotBaseBlue = 120

    app.highlightColor = rgb(255, 165, 0)

    app.winningPieceColor = gradient(rgb(255, 20, 147), 
                                  rgb(255, 105, 180), start='center')
    
    app.theme = 'Default'

    onGameStart(app)
    loadAllImages(app)

def onGameStart(app):
    app.computer = False 
    app.computerTurn = False
    app.computerDifficulty = None 
    app.gameOver = False 
    app.winner = None 
    app.winningPieces = None 
    app.isDragging = False 
    app.boardState = np.full((app.rows, app.cols), None) 
    app.currentPlayer = 1
    app.endScreenMove = 0
    app.replayTimer = 0
    #when user changes board view, this controls how quickly board rotates
    
    app.startingScreen = True 
    app.instructionsScreen = False 
    app.modeSelection = False 
    app.themeScreen = False
    app.playingScreen = False 
    app.endScreen = False
    app.lastMouseX = None 
    app.lastMouseY = None 

    #theme variables
    app.oceanThemeHover = False
    app.forestThemeHover = False
    app.sunsetThemeHover = False
    app.lavenderThemeHover = False

    #in playing mode to drag pieces onto board
    app.rotating = False 
    app.finalAngle = 0
    app.player1PieceSelected = False
    app.player2PieceSelected = False

    app.projectedRow = None
    app.projectedCol = None

    app.hintMove = None
    app.hintPressed = False
    app.displayHintsLeft = False
    app.player1HintsLeft = 3
    app.player2HintsLeft = 3
    app.hintColor = app.player1PieceColor

    #buttons
    app.themesHover = False
    app.instructionsHover = False
    app.startHover = False

    app.horizontalWinHover = False
    app.horizontalWin = True

    app.verticalWinHover = False
    app.verticalWin = False

    app.diagonalWinHover = False
    app.diagonalWin = False

    app.multiplayerHover = False
    app.computerHover = False
    app.hardDifficultyHover = False
    app.mediumDifficultyHover = False
    app.easyDifficultyHover = False

    app.hintHover = False
    app.homeHover = False
    #initialize to none and set based on which screen entered
    app.board = None

def redrawAll(app):
    if app.startingScreen:
        startScreen(app)
    elif app.instructionsScreen:
        instructionScreen(app)
    else:
        if app.theme == 'Ocean':
            drawImage(app.ocean, 0, 0, 
                      width = app.width, 
                      height = app.height, 
                      opacity = 60)
        elif app.theme == 'Sunset':
            drawImage(app.sunset, 0, 0, 
                      width = app.width, 
                      height = app.height, 
                      opacity = 60)
        elif app.theme == 'Forest':
            drawImage(app.forest, 0, 0, 
                      width = app.width, 
                      height = app.height, 
                      opacity = 60)
        elif app.theme == 'Lavender':
            drawImage(app.lavender, 0, 0, 
                      width = app.width, 
                      height = app.height, 
                      opacity = 60)
            
        if app.modeSelection:
            modeSelection(app)
        elif app.playingScreen:
            playingScreen(app)
        elif app.themeScreen:
            themeScreen(app)
        elif app.endScreen:
            endScreen(app)
    
    home(app)

def onStep(app):
    app.titleOffset += 0.1
    app.timeValue += 0.15
    if app.instructionsScreen:
        app.board.rotationY = (app.board.rotationY - 1)% 360
    elif app.endScreen:
        app.board.rotationY = (app.board.rotationY - 1)% 360
        if app.endScreenMove < len(app.game.moveList):
            app.replayTimer += 1
            if app.replayTimer == 60:  
                app.replayTimer = 0
                row, col, color = app.game.moveList[app.endScreenMove]
                app.boardState[row, col] = color
                app.board.updateBoardState(app.boardState)
                app.endScreenMove += 1
        elif app.endScreenMove == len(app.game.moveList):
            for i in (app.winningPieces):
                row,col = i
                app.boardState[row, col] = app.winningPieceColor
    elif app.playingScreen and not app.gameOver:
        app.game.timeElapsed += 1/30
    if app.rotating:
        rotationSpeed = 2.5  
        #determine when close enough to target angle
        if abs(app.board.rotationY - app.finalAngle) <= rotationSpeed:  
            app.board.rotationY = app.finalAngle
            app.rotating = False

            #wait till board rotates then play computer's turn and rotate back
            if app.computerTurn:
                time.sleep(2)
                computerMove = app.game.makeComputerMove(app)
                if app.game.gameOverState(computerMove, app):
                    return
                app.finalAngle = 0
                app.rotating = True
                app.computerTurn = False
        else:
            #find direction of rotation so that board needs to rotate minimally
            #to flip to other side
            if (app.finalAngle - app.board.rotationY) % 360 > 180:
                #counter clockwise rotation
                direction = -1 
            else:
                # clockwise rotation
                direction = 1  
            app.board.rotationY = (app.board.rotationY + direction * rotationSpeed) % 360

def onMousePress(app,mouseX,mouseY):
    #reset all dynamic variables
    if (app.homeX - app.homeWidth/2 <= mouseX <= 
            app.homeX + app.homeWidth/2 and 
            app.homeY - app.homeHeight/2 <= mouseY <= 
            app.homeY + app.homeHeight/2):
        onGameStart(app)
            
    elif app.startingScreen:
        if (app.instructionsX - app.instructionsWidth/2 <= mouseX <= 
            app.instructionsX + app.instructionsWidth/2 and 
            app.instructionsY - app.instructionsHeight/2 <= mouseY <= 
            app.instructionsY + app.instructionsHeight/2):

            #set board state to a sample horizontal win 
            app.instructionsScreen = True
            app.boardState = np.array([[None, None, None, None, None, None, None],
                                       [None, 'darkRed', None, 'blue', None, None, None],
                                       [None, 'darkRed', 'blue', 'blue', None, None, None],
                                       [None, 'blue', 'darkRed', 'darkRed', 'blue', None, None],
                                       [None, 'blue', 'blue', 'red', 'red', 'red', 'red'],
                                       [None, 'darkRed', 'blue', 'blue', 'blue', 'darkRed', 'blue']], 
                                       dtype=object)
            
            app.board = Board(app.width/4,3*app.height/8,30,app)
            app.startingScreen = False

        elif (app.startX - app.startWidth/2 <= mouseX <= 
            app.startX + app.startWidth/2 and 
            app.startY - app.startHeight/2 <= mouseY <= 
            app.startY + app.startHeight/2):

            app.modeSelection = True
            app.startingScreen = False
        
        elif (app.themesX - app.themesWidth/2 <= mouseX <= 
            app.themesX + app.themesWidth/2 and 
            app.themesY - app.themesHeight/2 <= mouseY <= 
            app.themesY + app.themesHeight/2):

            app.themeScreen = True
            app.startingScreen = False

    elif app.modeSelection:
        if (app.multiplayerX - app.multiplayerWidth/2 <= mouseX <= 
            app.multiplayerX + app.multiplayerWidth/2 and 
            app.multiplayerY - app.multiplayerHeight/2 <= mouseY <= 
            app.multiplayerY + app.multiplayerHeight/2):

            app.playingScreen = True
            app.modeSelection = False
            app.computer = False
            app.board = Board(app.width/2,app.height/2,app.cellSize,app)
            app.board.rotationX = 0
            app.board.rotationY = 0
            app.game = Game(app)
            
        
        elif (app.computerX - app.computerWidth/2 <= mouseX <= 
            app.computerX + app.computerWidth/2 and 
            app.computerY - app.computerHeight/2 <= mouseY <= 
            app.computerY + app.computerHeight/2):

            app.computer = True
        
        elif app.computer and app.computerDifficulty == None:
            #set difficulty to 1, 2 or 3 (easy, medium or hard)
            difficultySelected = False
            if (app.easyDifficultyX - app.easyDifficultyWidth/2 <= mouseX <= 
            app.easyDifficultyX + app.easyDifficultyWidth/2 and 
            app.easyDifficultyY - app.easyDifficultyHeight/2 <= mouseY <= 
            app.easyDifficultyY + app.easyDifficultyHeight/2):
                app.computerDifficulty = 1
                difficultySelected = True
        
            elif (app.mediumDifficultyX - app.mediumDifficultyWidth/2 
                  <= mouseX <= 
            app.mediumDifficultyX + app.mediumDifficultyWidth/2 and 
            app.mediumDifficultyY - app.mediumDifficultyHeight/2 <= mouseY <= 
            app.mediumDifficultyY + app.mediumDifficultyHeight/2):
                app.computerDifficulty = 2
                difficultySelected = True
            
            elif (app.hardDifficultyX - app.hardDifficultyWidth/2 <= mouseX <= 
            app.hardDifficultyX + app.hardDifficultyWidth/2 and 
            app.hardDifficultyY - app.hardDifficultyHeight/2 <= mouseY <= 
            app.hardDifficultyY + app.hardDifficultyHeight/2):
                app.computerDifficulty = 3
                difficultySelected = True
            
            if difficultySelected:
                app.playingScreen = True
                app.modeSelection = False
                app.board = Board(app.width/2,app.height/2,app.cellSize,app)
                app.board.rotationX = 0
                app.board.rotationY = 0
                app.game = Game(app)


    elif app.playingScreen:
        if not app.gameOver and not app.rotating:            
            if (isInCircle(mouseX,mouseY,app.player1PositionX,
                            app.player1PositionY,app.cellSize/2) and 
                            app.currentPlayer == 1):
                app.player1PieceSelected = not app.player1PieceSelected
                app.player2PieceSelected = False
                

            elif (isInCircle(mouseX,mouseY,app.player2PositionX,
                            app.player2PositionY,app.cellSize/2) and 
                            app.currentPlayer == 2):
                app.player2PieceSelected = not app.player2PieceSelected 
                app.player1PieceSelected = False
                
            elif (app.hintX - app.hintWidth/2 <= mouseX <= 
            app.hintX + app.hintWidth/2 and 
            app.hintY - app.hintHeight/2 <= mouseY <= 
            app.hintY + app.hintHeight/2):
                if (app.currentPlayer == 1 and 
                    not app.hintPressed and 
                    app.player1HintsLeft > 0):
                    app.hintMove = app.game.getHint(app)
                    app.player1HintsLeft -= 1
                    app.hintPressed = True

                elif (app.currentPlayer == 2 and 
                    not app.hintPressed and 
                    app.player2HintsLeft > 0):
                    app.hintMove = app.game.getHint(app)
                    app.player2HintsLeft -= 1
                    app.hintPressed = True
                    
            app.isDragging = True
            app.lastMouseX = mouseX
            app.lastMouseY = mouseY

        elif app.gameOver:
            app.boardState = np.full((app.rows, app.cols), None) 
            app.board = Board(app.width/2,app.height/2,40,app)
            app.endScreen = True
            app.playingScreen = False

    elif app.instructionsScreen:
        if (app.horizontalWinX - app.horizontalWinWidth/2 <= mouseX <= 
            app.horizontalWinX + app.horizontalWinWidth/2 and 
            app.horizontalWinY - app.horizontalWinHeight/2 <= mouseY <= 
            app.horizontalWinY + app.horizontalWinHeight/2):

            app.horizontalWin = True
            app.verticalWin = False
            app.diagonalWin = False

            #set board state to a sample horizontal win 
            app.boardState = np.array([[None, None, None, None, None, None, None],
                                       [None, 'darkRed', None, 'blue', None, None, None],
                                       [None, 'darkRed', 'blue', 'blue', None, None, None],
                                       [None, 'blue', 'darkRed', 'darkRed', 'blue', None, None],
                                       [None, 'blue', 'blue', 'red', 'red', 'red', 'red'],
                                       [None, 'darkRed', 'blue', 'blue', 'blue', 'darkRed', 'blue']], 
                                       dtype=object)
            

        elif (app.verticalWinX - app.verticalWinWidth/2 <= mouseX <= 
            app.verticalWinX + app.verticalWinWidth/2 and 
            app.verticalWinY - app.verticalWinHeight/2 <= mouseY <= 
            app.verticalWinY + app.verticalWinHeight/2):

                app.horizontalWin = False
                app.verticalWin = True
                app.diagonalWin = False
            
                #set board state to a sample vertical win 
                app.boardState = np.array([[None, None, None, None, None, None, None],
                                       [None, 'darkRed', None, 'blue', None, None, None],
                                       [None, 'darkRed', 'cyan', 'blue', None, None, None],
                                       [None, 'blue', 'cyan', 'darkRed', 'blue', None, None],
                                       [None, 'blue', 'cyan', 'darkRed', 'darkRed', 'darkRed', 'darkRed'],
                                       [None, 'darkRed', 'cyan', 'blue', 'darkRed', 'darkRed', 'blue']], 
                                       dtype=object)
                
        elif (app.diagonalWinX - app.diagonalWinWidth/2 <= mouseX <= 
            app.diagonalWinX + app.diagonalWinWidth/2 and 
            app.diagonalWinY - app.diagonalWinHeight/2 <= mouseY <= 
            app.diagonalWinY + app.diagonalWinHeight/2):
                
                app.horizontalWin = False
                app.verticalWin = False
                app.diagonalWin = True

                #set board state to a sample diagonal win 
                app.boardState = np.array([[None, None, None, None, None, None, None],
                                       [None, 'blue', None, None, None, None, None],
                                       [None, 'darkGreen', 'mediumSpringGreen', 'blue', None, None, None],
                                       [None, 'blue', 'blue', 'mediumSpringGreen', 'blue', None, None],
                                       [None, 'blue', 'blue', 'darkGreen', 'mediumSpringGreen', 'darkGreen', 'darkGreen'],
                                       [None, 'darkGreen', 'blue', 'blue', 'darkGreen', 'mediumSpringGreen', 'blue']], 
                                       dtype=object)
        
        app.board.updateBoardState(app.boardState)

    elif app.themeScreen:
        if (app.oceanThemeX - app.themeWidth/2 <= mouseX <=
        app.oceanThemeX + app.themeWidth/2 and
        app.oceanThemeY - app.themeHeight/2 <= mouseY <=
        app.oceanThemeY + app.themeHeight/2):
            
            app.theme = 'Ocean'
            setOceanTheme(app)

        if (app.forestThemeX - app.themeWidth/2 <= mouseX <=
            app.forestThemeX + app.themeWidth/2 and
            app.forestThemeY - app.themeHeight/2 <= mouseY <=
            app.forestThemeY + app.themeHeight/2):

            app.theme = 'Forest'
            setForestTheme(app)

        if (app.sunsetThemeX - app.themeWidth/2 <= mouseX <=
            app.sunsetThemeX + app.themeWidth/2 and
            app.sunsetThemeY - app.themeHeight/2 <= mouseY <=
            app.sunsetThemeY + app.themeHeight/2):

            app.theme = 'Sunset'
            setSunsetTheme(app)

        if (app.lavenderThemeX - app.themeWidth/2 <= mouseX <=
            app.lavenderThemeX + app.themeWidth/2 and
            app.lavenderThemeY - app.themeHeight/2 <= mouseY <=
            app.lavenderThemeY + app.themeHeight/2):

            app.theme = 'Lavender'
            setLavenderTheme(app)

def onMouseRelease(app,mouseX,mouseY):
    if app.playingScreen and (app.player1PieceSelected or 
                              app.player2PieceSelected):
        move = app.game.makeMove(mouseX,mouseY,app)
        app.player1PositionX = 30
        app.player1PositionY = 40

        app.player2PositionX = 30
        app.player2PositionY = 90
        app.hintMove = None
        app.hintPressed = False
        app.displayHintsLeft = False
        if move != None:
            app.game.gameOverState(move,app)


def onKeyPress(app,key):
    if app.playingScreen:
        if not app.gameOver and not app.rotating:
            if key == 'left':
                app.board.rotationY = (app.board.rotationY + 5)% 360
            elif key == 'right':
                app.board.rotationY = (app.board.rotationY - 5)% 360
            elif key == 'up':
                if 90 < app.board.rotationY < 270:
                    app.board.rotationX = max(-60, 
                                              min(60, 
                                                  app.board.rotationX + 15))
                else:
                    app.board.rotationX = max(-60, 
                                              min(60, 
                                                  app.board.rotationX - 15))
            elif key == 'down':
                if 90 < app.board.rotationY < 270:
                    app.board.rotationX = max(-60, 
                                              min(60, 
                                                  app.board.rotationX - 15))
                else:
                    app.board.rotationX = max(-60, 
                                              min(60, 
                                                  app.board.rotationX + 15))

def onMouseMove(app,mouseX,mouseY):
    if (app.homeX - app.homeWidth/2 <= mouseX <= 
            app.homeX + app.homeWidth/2 and 
            app.homeY - app.homeHeight/2 <= mouseY <= 
            app.homeY + app.homeHeight/2):
            app.homeHover = True
    else:
        app.homeHover = False

    if app.startingScreen:
        if (app.themesX - app.themesWidth/2 <= mouseX <= 
            app.themesX + app.themesWidth/2 and 
            app.themesY - app.themesHeight/2 <= mouseY <= 
            app.themesY + app.themesHeight/2):

            app.themesHover = True
            app.instructionsHover = False
            app.startHover = False

        elif (app.instructionsX - app.instructionsWidth/2 <= mouseX <= 
            app.instructionsX + app.instructionsWidth/2 and 
            app.instructionsY - app.instructionsHeight/2 <= mouseY <= 
            app.instructionsY + app.instructionsHeight/2):

            app.instructionsHover = True
            app.startHover = False
            app.themesHover = False

        elif (app.startX - app.startWidth/2 <= mouseX <= 
            app.startX + app.startWidth/2 and 
            app.startY - app.startHeight/2 <= mouseY <= 
            app.startY + app.startHeight/2):
            app.startHover = True
            app.instructionsHover = False
            app.themesHover = False
        
        else:
            app.instructionsHover = False
            app.startHover = False
            app.themesHover = False

    elif app.instructionsScreen:
        if (app.horizontalWinX - app.horizontalWinWidth/2 <= mouseX <= 
            app.horizontalWinX + app.horizontalWinWidth/2 and 
            app.horizontalWinY - app.horizontalWinHeight/2 <= mouseY <= 
            app.horizontalWinY + app.horizontalWinHeight/2):

            app.horizontalWinHover = True
            app.verticalWinHover = False
            app.diagonalWinHover = False

        elif (app.verticalWinX - app.verticalWinWidth/2 <= mouseX <= 
            app.verticalWinX + app.verticalWinWidth/2 and 
            app.verticalWinY - app.verticalWinHeight/2 <= mouseY <= 
            app.verticalWinY + app.verticalWinHeight/2):

            app.verticalWinHover = True
            app.horizontalWinHover = False
            app.diagonalWinHover = False
        
        elif (app.diagonalWinX - app.diagonalWinWidth/2 <= mouseX <= 
            app.diagonalWinX + app.diagonalWinWidth/2 and 
            app.diagonalWinY - app.diagonalWinHeight/2 <= mouseY <= 
            app.diagonalWinY + app.diagonalWinHeight/2):

            app.diagonalWinHover = True
            app.verticalWinHover = False
            app.horizontalWinHover = False
            
        else: 
            app.horizontalWinHover = False
            app.verticalWinHover = False
            app.diagonalWinHover = False

    elif app.modeSelection:
        if (app.multiplayerX - app.multiplayerWidth/2 <= mouseX <= 
            app.multiplayerX + app.multiplayerWidth/2 and 
            app.multiplayerY - app.multiplayerHeight/2 <= mouseY <= 
            app.multiplayerY + app.multiplayerHeight/2):

            app.multiplayerHover = True
            app.computerHover = False
            
        
        elif (app.computerX - app.computerWidth/2 <= mouseX <= 
            app.computerX + app.computerWidth/2 and 
            app.computerY - app.computerHeight/2 <= mouseY <= 
            app.computerY + app.computerHeight/2):

            app.computerHover = True
            app.multiplayerHover = False

        else:
            app.computerHover = False
            app.multiplayerHover = False
        
        if app.computer and app.computerDifficulty == None:
            if (app.easyDifficultyX - app.easyDifficultyWidth/2 <= mouseX <= 
            app.easyDifficultyX + app.easyDifficultyWidth/2 and 
            app.easyDifficultyY - app.easyDifficultyHeight/2 <= mouseY <= 
            app.easyDifficultyY + app.easyDifficultyHeight/2):
                
                app.easyDifficultyHover = True
                app.mediumDifficultyHover = False
                app.hardDifficultyHover = False
        
            elif (app.mediumDifficultyX - 
                  app.mediumDifficultyWidth/2 <= mouseX <= 
            app.mediumDifficultyX + app.mediumDifficultyWidth/2 and 
            app.mediumDifficultyY - app.mediumDifficultyHeight/2 <= mouseY <= 
            app.mediumDifficultyY + app.mediumDifficultyHeight/2):
                
                app.mediumDifficultyHover = True
                app.hardDifficultyHover = False
                app.easyDifficultyHover = False
            
            elif (app.hardDifficultyX - app.hardDifficultyWidth/2 <= mouseX <= 
            app.hardDifficultyX + app.hardDifficultyWidth/2 and 
            app.hardDifficultyY - app.hardDifficultyHeight/2 <= mouseY <= 
            app.hardDifficultyY + app.hardDifficultyHeight/2):
                
                app.hardDifficultyHover = True
                app.mediumDifficultyHover = False
                app.easyDifficultyHover = False
            
            else:
                app.hardDifficultyHover = False
                app.mediumDifficultyHover = False
                app.easyDifficultyHover = False

    elif app.themeScreen:
        if (app.oceanThemeX - app.themeWidth/2 <= mouseX <=
            app.oceanThemeX + app.themeWidth/2 and
            app.oceanThemeY - app.themeHeight/2 <= mouseY <=
            app.oceanThemeY + app.themeHeight/2):

            app.oceanThemeHover = True

        else:
            app.oceanThemeHover = False

        # Forest Theme hover logic
        if (app.forestThemeX - app.themeWidth/2 <= mouseX <=
            app.forestThemeX + app.themeWidth/2 and
            app.forestThemeY - app.themeHeight/2 <= mouseY <=
            app.forestThemeY + app.themeHeight/2):

            app.forestThemeHover = True

        else:
            app.forestThemeHover = False

        # Sunset Theme hover logic
        if (app.sunsetThemeX - app.themeWidth/2 <= mouseX <=
            app.sunsetThemeX + app.themeWidth/2 and
            app.sunsetThemeY - app.themeHeight/2 <= mouseY <=
            app.sunsetThemeY + app.themeHeight/2):

            app.sunsetThemeHover = True

        else:
            app.sunsetThemeHover = False

        # Lavender Theme hover logic
        if (app.lavenderThemeX - app.themeWidth/2 <= mouseX <=
            app.lavenderThemeX + app.themeWidth/2 and
            app.lavenderThemeY - app.themeHeight/2 <= mouseY <=
            app.lavenderThemeY + app.themeHeight/2):

            app.lavenderThemeHover = True
        else:
            app.lavenderThemeHover = False
    
    elif app.playingScreen:
        if ((app.hintX - app.hintWidth/2 <= mouseX <= 
            app.hintX + app.hintWidth/2 and 
            app.hintY - app.hintHeight/2 <= mouseY <= 
            app.hintY + app.hintHeight/2) and 
            not app.hintPressed and 
            not app.rotating):

            if ((app.currentPlayer == 1 and app.player1HintsLeft > 0) or
                (app.currentPlayer == 2 and app.player2HintsLeft > 0)):
                app.hintHover = True
            app.displayHintsLeft = True

        else:
            app.hintHover = False
            app.displayHintsLeft = False

def onMouseDrag(app,mouseX,mouseY):
    if (app.isDragging and app.playingScreen 
        and not app.gameOver and not app.rotating):
        if app.player1PieceSelected or app.player2PieceSelected:
            position = app.game.getBoardPosition(app,mouseX,mouseY)
            if position != None:
                app.projectedRow, app.projectedCol = position
            else:
                app.projectedRow = app.projectedCol = None
            if app.player1PieceSelected:
                app.player1PositionX = mouseX
                app.player1PositionY = mouseY
            elif app.player2PieceSelected:
                app.player2PositionX = mouseX
                app.player2PositionY = mouseY
        else:
            #calculate change in x and y
            dx = mouseX - app.lastMouseX
            dy = mouseY - app.lastMouseY
            #dragging mouse up or down will tilt 
            # the board about x axis (width of board)
            #limit range of rotation to range of -60 to 60 degrees
            app.board.rotationX = max(-60, min(60, app.board.rotationX + 
                                                dy * app.rotationSpeed))
            #dragging mouse left or right will 
            # tilt the board about y axis (height of board)
            app.board.rotationY = (app.board.rotationY+ dx * 
                                   app.rotationSpeed)% 360

            app.lastMouseX = mouseX
            app.lastMouseY = mouseY

def isInCircle(x1,y1,x2,y2,radius):
    distance = ((x1 - x2)**2 + (y1 - y2)**2)**0.5
    return distance <= radius

def main():
    runApp()

main()
