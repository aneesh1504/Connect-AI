from cmu_graphics import *
import math
from board import Board
import numpy as np
from PIL import Image
import os

def loadAllImages(app):
    currDir = os.path.dirname(os.path.realpath(__file__))
    #Citation: https://shorturl.at/4KEpp
    app.startPhoto = CMUImage(Image.open(currDir + '/images/start.png'))
    #Citation: https://shorturl.at/07qLU
    app.instructionsPhoto = CMUImage(Image.open(currDir + 
                                                '/images/instructions.png'))
    #Citation: https://www.flaticon.com/free-icon/home-button_61972
    app.homeButton = CMUImage(Image.open(currDir + 
                                                '/images/homeButton.png'))
    #Citation: https://shorturl.at/QyVoA
    app.ocean = CMUImage(Image.open(currDir + 
                                                '/images/ocean.png'))
    #Citation: https://tinyurl.com/4kka28hm
    app.lavender = CMUImage(Image.open(currDir + 
                                                '/images/lavender.png'))
    #Citation: https://shorturl.at/mtqRx
    app.sunset = CMUImage(Image.open(currDir + 
                                                '/images/sunset.png'))
    #Citation: https://shorturl.at/2Nybt
    app.forest = CMUImage(Image.open(currDir + 
                                                '/images/forest.png'))

def startScreen(app):
    drawImage(app.startPhoto, 0, 0) 
    mainTitle = 150 + math.sin(app.titleOffset) * 30
    drawLabel('4', app.width/2, mainTitle, size=100, bold = True,
              fill = 'red', font='orbitron')
    drawLabel('Connect', app.width/2, mainTitle, size=80, bold = True,
              fill = 'black', font='orbitron')
    #themes button
    if app.themesHover:
        themesColor = gradient(rgb(200, 100, 225), 
                               rgb(120, 50, 175), 
                               start='center')
        themesFactor = 1.2

    else:
        themesColor = gradient(rgb(150, 40, 190),
                                        rgb(77, 30, 135), 
                                        start='center')
        themesFactor = 1
    
    drawRect(app.themesX,app.themesY,
             app.themesWidth*themesFactor,
             app.themesHeight*themesFactor, 
             fill = themesColor, align = 'center')
    
    drawLabel('Themes', app.themesX,
              app.themesY, size = 40 * themesFactor, font='orbitron')
    
    #instructions button
    if app.instructionsHover:
        instructionsColor = gradient(rgb(255, 100, 160),  
                                    rgb(220, 80, 100), 
                                    start='center')
        instructionsFactor = 1.2

    else:
        instructionsColor = gradient(rgb(234, 0, 120), 
                                     rgb(180, 0, 60), 
                                     start='center')
        instructionsFactor = 1
    
    drawRect(app.instructionsX,app.instructionsY,
             app.instructionsWidth*instructionsFactor,
             app.instructionsHeight*instructionsFactor, 
             fill = instructionsColor, align = 'center')
    
    drawLabel('Instructions', app.instructionsX,
              app.instructionsY, size = 40 * instructionsFactor, 
              font='orbitron')
    
    #game start button
    if app.startHover:
        startColor = gradient(rgb(175, 80, 145),  
                              rgb(230, 100, 185), 
                              start='center')
        startFactor = 1.2

    else:
        startColor = gradient(rgb(159, 39, 125), 
                              rgb(203, 37, 185), 
                              start='center')
        startFactor = 1
    
    drawRect(app.startX,app.startY,
             app.startWidth*startFactor,
             app.startHeight*startFactor, 
             fill = startColor, align = 'center')
    
    drawLabel('Start Game', app.startX,
              app.startY, size = 40 * startFactor, font='orbitron')

def instructionScreen(app):
    drawImage(app.instructionsPhoto, 0, 0) 
    app.board.drawBoard(app)
    
    #horizontal win
    if app.horizontalWinHover:
        horizontalWinColor = gradient(rgb(255, 100, 160),  
                                      rgb(220, 80, 100),  
                                      start='center')
        horizontalWinFactor = 1.2

    else:
        horizontalWinColor = gradient(rgb(234, 0, 120), 
                                      rgb(180, 0, 60), 
                                      start='center')
        horizontalWinFactor = 1
    
    drawRect(app.horizontalWinX,app.horizontalWinY,
             app.horizontalWinWidth*horizontalWinFactor,
             app.horizontalWinHeight*horizontalWinFactor, 
             fill = horizontalWinColor, align = 'center')
    
    drawLabel('Horizontal Win', app.horizontalWinX,
              app.horizontalWinY, size = 15 * horizontalWinFactor,
              font='orbitron', fill = 'white')
    
    #vertical win
    if app.verticalWinHover:
        verticalWinColor = gradient(rgb(255, 100, 160),  
                                      rgb(220, 80, 100),  
                                      start='center')
        verticalWinFactor = 1.2

    else:
        verticalWinColor = gradient(rgb(234, 0, 120), 
                                      rgb(180, 0, 60), 
                                      start='center')
        verticalWinFactor = 1
    
    drawRect(app.verticalWinX,app.verticalWinY,
             app.verticalWinWidth*verticalWinFactor,
             app.verticalWinHeight*verticalWinFactor, 
             fill = verticalWinColor, align = 'center')
    
    drawLabel('Vertical Win', app.verticalWinX,
              app.verticalWinY, size = 15 * verticalWinFactor, 
              font='orbitron', fill = 'white')
    
    #diagonal win
    if app.diagonalWinHover:
        diagonalWinColor = gradient(rgb(255, 100, 160),  
                                      rgb(220, 80, 100),  
                                      start='center')
        diagonalWinFactor = 1.2

    else:
        diagonalWinColor = gradient(rgb(234, 0, 120), 
                                      rgb(180, 0, 60), 
                                      start='center')
        diagonalWinFactor = 1
    
    drawRect(app.diagonalWinX,app.diagonalWinY,
             app.diagonalWinWidth*diagonalWinFactor,
             app.diagonalWinHeight*diagonalWinFactor, 
             fill = diagonalWinColor, align = 'center')
    
    drawLabel('Diagonal Win', app.diagonalWinX,
              app.diagonalWinY, size = 15 * diagonalWinFactor, 
              font='orbitron', fill = 'white')
    
    #text
    labels = [
    ('How to Connect 4', 3 * app.width / 4 - 55, 80, 30, 'center', False),
    ('- Aim to be the first player to connect 4 pieces', 
     app.width / 2 - 55, 130, 15, 'left', False),
    ('in a row to win!', 3 * app.width / 4 - 55, 150, 15, 'center', True),
    ('- Connect pieces horizontally, vertically, or diagonally', 
     app.width / 2 - 55, 180, 15, 'left', False),
    ('- Click buttons on the left to explore patterns', 
     app.width / 2 - 55, 200, 15, 'left', False),
    ('- Drag your piece from the left during your turn', 
     app.width / 2 - 55, 230, 15, 'left', False),
    ('Drop it on the board Pieces stack automatically', 
     app.width / 2 - 55, 250, 15, 'left', False),
    ('Plan carefully to make the best moves each turn', 
     app.width / 2 - 55, 270, 15, 'left', False),
    ('- Press play mode in the top left to start playing', 
     app.width / 2 - 55, 290, 15, 'left', False),
    ('- Use arrows to tilt the board up, down, or sideways', 
     app.width / 2 - 55, 320, 15, 'left', False),
    ('Or drag the screen to rotate the board easily', 
     app.width / 2 - 55, 340, 15, 'left', False),
    ('- Select 2-player mode to challenge friends', 
     app.width / 2 - 55, 360, 15, 'left', False),
    ('Or play AI with easy, medium, or hard modes', 
     app.width / 2 - 55, 380, 15, 'left', False),
    ('- Press the hint button for help on your turn', 
     app.width / 2 - 55, 410, 15, 'left', False),
    ('Hints show the best moves Use them wisely', 
     app.width / 2 - 55, 430, 15, 'left', False),
    ('You only get three hints per game', 
     app.width / 2 - 55, 450, 15, 'left', False),
    ('- Customize themes in the menu for new styles', 
     app.width / 2 - 55, 480, 15, 'left', False),
    ('Enjoy fresh colors for pieces and the board', 
     app.width / 2 - 55, 500, 15, 'left', False),
    ('- Keep practicing to sharpen skills and win', 
     app.width / 2 - 55, 530, 15, 'left', False),
    ('Track your progress and aim for mastery', 
     app.width / 2 - 55, 550, 15, 'left', False),
    ('Have fun and enjoy Connect 4 your way', 
     app.width / 2 - 55, 570, 15, 'left', False)
    ]




    for text, x, y, size, align, bold in labels:
        drawLabel(text, x, y, size=size, align=align, bold=bold, 
                  font='orbitron')
    
def modeSelection(app):
    multiplayerFactor = 1
    computerFactor = 1
    hardDifficultyFactor = 1
    mediumDifficultyFactor = 1
    easyDifficultyFactor = 1

    computerColor = gradient(rgb(159, 39, 125), 
                              rgb(203, 37, 185), 
                              start='center')
    
    easyColor = mediumColor = hardColor = gradient(rgb(150, 40, 190),
                                                   rgb(77, 30, 135), 
                                                   start='center')

    
    multiplayerColor = gradient(rgb(234, 0, 120), 
                                     rgb(180, 0, 60), 
                                     start='center')

    if app.multiplayerHover:
        multiplayerFactor = 1.2
        multiplayerColor = gradient(rgb(255, 100, 160),  
                                    rgb(220, 80, 100), 
                                    start='center')
        
    elif app.computerHover:
        computerFactor = 1.2
        computerColor = gradient(rgb(175, 80, 145),  
                                 rgb(230, 100, 185), 
                                 start='center')
        
    elif app.hardDifficultyHover:
        hardDifficultyFactor = 1.2
        hardColor = gradient(rgb(120, 50, 175), 
                             rgb(200, 100, 225), 
                             start='center')
        
    elif app.mediumDifficultyHover:
        mediumDifficultyFactor = 1.2
        mediumColor = gradient(rgb(120, 50, 175), 
                               rgb(200, 100, 225), 
                               start='center')
        
    elif app.easyDifficultyHover:
        easyDifficultyFactor = 1.2
        easyColor = gradient(rgb(120, 50, 175), 
                             rgb(200, 100, 225), 
                             start='center')

    #multiplayer button
    drawRect(app.multiplayerX,app.multiplayerY,
             app.multiplayerWidth * multiplayerFactor, 
             app.multiplayerHeight * multiplayerFactor,
             fill = multiplayerColor, align = 'center')
    drawLabel('Multiplayer', app.multiplayerX,
              app.multiplayerY, size = 40 * multiplayerFactor, 
              font='orbitron')
    #computer button
    drawRect(app.computerX, app.computerY,
             app.computerWidth * computerFactor, 
             app.computerHeight * computerFactor,
             fill = computerColor,align = 'center')
    drawLabel('Computer', app.computerX,
              app.computerY, size = 40 * computerFactor, font='orbitron')

    #if computer selected difficulty selection
    if app.computer and app.computerDifficulty == None:
        drawRect(app.easyDifficultyX, app.easyDifficultyY,
             app.easyDifficultyWidth * easyDifficultyFactor, 
             app.easyDifficultyHeight * easyDifficultyFactor,
             fill = easyColor, align = 'center')
        drawLabel('Easy', app.easyDifficultyX,
                app.easyDifficultyY, size = 30 * easyDifficultyFactor, 
                font='orbitron')
        
        drawRect(app.mediumDifficultyX, app.mediumDifficultyY,
             app.mediumDifficultyWidth * mediumDifficultyFactor, 
             app.mediumDifficultyHeight * mediumDifficultyFactor,
             fill = mediumColor, align = 'center')
        drawLabel('Medium', app.mediumDifficultyX,
                app.mediumDifficultyY, size = 30 * mediumDifficultyFactor, 
                font='orbitron')
        
        drawRect(app.hardDifficultyX, app.hardDifficultyY,
             app.hardDifficultyWidth * hardDifficultyFactor, 
             app.hardDifficultyHeight * hardDifficultyFactor,
             fill = hardColor, align = 'center')
        drawLabel('Hard', app.hardDifficultyX,
                app.hardDifficultyY, size = 30 * hardDifficultyFactor, 
                font='orbitron')

def playingScreen(app):
    app.board.drawBoard(app)
    if not app.gameOver:
        if app.computer and app.currentPlayer == 2:
            drawLabel(f"Computer's turn", 
                  400, 560, size = 40, font='orbitron')
        else:
            drawLabel(f"Player {app.currentPlayer}'s turn", 
                  400, 560, size = 40, font='orbitron')
            
        if app.currentPlayer == 1:
            currentColor = app.player1PieceColor
        else:
            currentColor = app.player2PieceColor
        
        Player1Piece = app.board.drawPiece(app.player1PositionX,
                                        app.player1PositionY,
                                        app.player1PieceSelected,
                                        currentColor,
                                        app.player1PieceColor)
    
        Player2Piece = app.board.drawPiece(app.player2PositionX,
                                            app.player2PositionY,
                                            app.player2PieceSelected,
                                            currentColor,
                                            app.player2PieceColor)
        if app.hintHover:
            hintFactor = 1.2
        else:
            hintFactor = 1
        if app.currentPlayer == 1 and app.player1HintsLeft > 0:
            hintColor = app.player1PieceColor
        elif app.currentPlayer == 2 and app.player2HintsLeft > 0:
            hintColor = app.player2PieceColor
        else:
            hintColor = None

        drawRect(app.hintX, app.hintY, 
                 app.hintWidth * hintFactor, app.hintHeight * hintFactor, 
                 align = 'center',
                 fill = hintColor,
                 border = 'black')
        drawLabel("Hint", app.hintX, app.hintY, size = 30 * hintFactor, 
                  font='orbitron')
        if app.displayHintsLeft:
            if app.currentPlayer == 1:
                drawLabel(f"{app.player1HintsLeft}",
                           app.hintX - 18, app.hintY - 45, 
                           size = 20, font='orbitron')
                drawLabel("left",
                           app.hintX + 13, app.hintY - 45, 
                           size = 20, font='orbitron')
            else:
                drawLabel(f"{app.player2HintsLeft}",
                           app.hintX - 18, app.hintY - 45, 
                           size = 20, font='orbitron')
                drawLabel("left",
                           app.hintX + 13, app.hintY - 45, 
                           size = 20, font='orbitron')


    elif app.winner == None:
        drawLabel("Game over, nobody wins! Press to continue", 
                  400, 570, size = 30, font='orbitron')
    else:
        drawLabel(f"Game over! Player {app.winner} wins! Press to continue", 
                  400, 570, size = 30, font='orbitron')
        
def themeScreen(app):
    drawLabel(f'Current Theme: {app.theme}',
              app.width/2,7*app.height/8, size = 40, 
              font='orbitron', fill = 'White')
    oceanThemeFactor = 1
    forestThemeFactor = 1
    sunsetThemeFactor = 1
    lavenderThemeFactor = 1

    oceanThemeColor = gradient(rgb(0, 0, 255), 
                                     rgb(0, 128, 255), start='center')
    forestThemeColor = gradient(rgb(0, 128, 0), 
                                      rgb(34, 139, 34), start='center')
    sunsetThemeColor = gradient(rgb(255, 165, 0), 
                                      rgb(255, 69, 0), start='center')
    lavenderThemeColor = gradient(rgb(128, 0, 128), 
                                        rgb(255, 0, 255), start='center')

    if app.oceanThemeHover:
        oceanThemeFactor = 1.2
        oceanThemeColor = gradient(rgb(30, 144, 255), 
                                         rgb(100, 149, 237), start='center')

    elif app.forestThemeHover:
        forestThemeFactor = 1.2
        forestThemeColor = gradient(rgb(34, 139, 34), 
                                          rgb(60, 179, 113), start='center')

    elif app.sunsetThemeHover:
        sunsetThemeFactor = 1.2
        sunsetThemeColor = gradient(rgb(255, 140, 0), 
                                          rgb(255, 99, 71), start='center')

    elif app.lavenderThemeHover:
        lavenderThemeFactor = 1.2
        lavenderThemeColor = gradient(rgb(186, 85, 211), 
                                            rgb(218, 112, 214), start='center')

    #ocean theme button
    drawRect(app.oceanThemeX, app.oceanThemeY,
             app.themeWidth * oceanThemeFactor, 
             app.themeHeight * oceanThemeFactor,
             fill=oceanThemeColor, align='center')
    drawLabel('Ocean', app.oceanThemeX, 
              app.oceanThemeY, size=40 * oceanThemeFactor, font='orbitron')

    #forest theme button
    drawRect(app.forestThemeX, app.forestThemeY,
             app.themeWidth * forestThemeFactor, 
             app.themeHeight * forestThemeFactor,
             fill=forestThemeColor, align='center')
    drawLabel('Forest', app.forestThemeX, 
              app.forestThemeY, size=40 * forestThemeFactor, font='orbitron')

    #sunset theme button
    drawRect(app.sunsetThemeX, app.sunsetThemeY,
             app.themeWidth * sunsetThemeFactor, 
             app.themeHeight * sunsetThemeFactor,
             fill=sunsetThemeColor, align='center')
    drawLabel('Sunset', app.sunsetThemeX, 
              app.sunsetThemeY, size=40 * sunsetThemeFactor, font='orbitron')

    #lavender theme button
    drawRect(app.lavenderThemeX, app.lavenderThemeY,
             app.themeWidth * lavenderThemeFactor, 
             app.themeHeight * lavenderThemeFactor,
             fill=lavenderThemeColor, align='center')
    drawLabel('Lavender', app.lavenderThemeX, 
              app.lavenderThemeY, size=40 * lavenderThemeFactor, 
              font='orbitron')
    
def setOceanTheme(app):
    app.player1PieceColor = gradient(rgb(0, 191, 255), 
                                     rgb(0, 128, 255), start='center')
    app.player2PieceColor = gradient(rgb(0, 255, 191), 
                                     rgb(64, 224, 208), start='center')
    app.boardFrontColor = gradient(rgb(0, 105, 148), 
                                    rgb(25, 25, 112), start='center')
    app.boardBackColor = gradient(rgb(173, 216, 230), 
                                   rgb(135, 206, 250), start='center')
    app.boardSidesColor = gradient(rgb(0, 34, 102), 
                                    rgb(0, 76, 153), start='center')
    app.boardTopBottomColor = gradient(rgb(70, 130, 180), 
                                       rgb(100, 149, 237), start='center')
    app.slotBaseRed = 120
    app.slotBaseGreen = 120
    app.slotBaseBlue = 120

    app.highlightColor = rgb(255, 215, 0)
    app.winningPieceColor = gradient(rgb(0, 255, 127), 
                                     rgb(50, 205, 50), start='center')


def setForestTheme(app):
    app.player1PieceColor = gradient(rgb(34, 139, 34), 
                                     rgb(0, 100, 0), start='center')
    app.player2PieceColor = gradient(rgb(107, 142, 35), 
                                     rgb(154, 205, 50), start='center')
    app.boardFrontColor = gradient(rgb(139, 69, 19), 
                                    rgb(101, 67, 33), start='center')
    app.boardBackColor = gradient(rgb(222, 184, 135), 
                                   rgb(210, 180, 140), start='center')
    app.boardSidesColor = gradient(rgb(160, 82, 45), 
                                    rgb(139, 69, 19), start='center')
    app.boardTopBottomColor = gradient(rgb(184, 134, 11), 
                                       rgb(160, 82, 45), start='center')
    app.slotBaseRed = 120
    app.slotBaseGreen = 120
    app.slotBaseBlue = 120

    app.highlightColor = rgb(255, 140, 0)
    app.winningPieceColor = gradient(rgb(0, 255, 0), 
                                     rgb(124, 252, 0), start='center')

def setSunsetTheme(app):
    app.player1PieceColor = gradient(rgb(255, 69, 0), 
                                     rgb(220, 20, 60), start='center')
    app.player2PieceColor = gradient(rgb(255, 160, 122), 
                                     rgb(255, 105, 97), start='center')
    app.boardFrontColor = gradient(rgb(255, 153, 153), 
                                    rgb(255, 102, 102), start='center')
    app.boardBackColor = gradient(rgb(255, 225, 190), 
                                   rgb(255, 200, 170), start='center')
    app.boardSidesColor = gradient(rgb(255, 178, 178), 
                                    rgb(255, 153, 153), start='center')
    app.boardTopBottomColor = gradient(rgb(255, 229, 204), 
                                       rgb(255, 204, 153), start='center')
    app.slotBaseRed = 120
    app.slotBaseGreen = 120
    app.slotBaseBlue = 120

    app.highlightColor = rgb(75, 0, 130)
    app.winningPieceColor = gradient(rgb(255, 102, 102), 
                                     rgb(255, 51, 51), start='center')

def setLavenderTheme(app):
    app.player1PieceColor = gradient(rgb(230, 230, 250), 
                                     rgb(216, 191, 216), start='center')
    app.player2PieceColor = gradient(rgb(138, 43, 226), 
                                     rgb(148, 0, 211), start='center')
    app.boardFrontColor = gradient(rgb(186, 85, 211), 
                                    rgb(138, 43, 226), start='center')
    app.boardBackColor = gradient(rgb(200, 162, 200), 
                                   rgb(180, 130, 180), start='center')
    app.boardSidesColor = gradient(rgb(147, 112, 219), 
                                    rgb(138, 43, 226), start='center')
    app.boardTopBottomColor = gradient(rgb(170, 120, 190), 
                                       rgb(180, 140, 200), start='center')
    app.slotBaseRed = 120
    app.slotBaseGreen = 120
    app.slotBaseBlue = 120

    app.highlightColor = rgb(255, 0, 255)
    app.winningPieceColor = gradient(rgb(255, 105, 180), 
                                     rgb(255, 20, 147), start='center')
    

def endScreen(app):
    app.board.drawBoard(app)
    #adjust width for number of digits in time elapsed
    RectWidth = 270 + 10*math.floor(math.log10(int(app.game.timeElapsed)))
    drawRect(app.width/4, 550, RectWidth, 40, 
             fill = app.boardFrontColor, align='center')
    drawRect(3*app.width/4, 550, RectWidth, 40, 
             fill = app.boardFrontColor, align='center')
    drawLabel(f'Total Moves: {app.game.moveCount}', 
              app.width/4, 550, size=20, font='orbitron', fill = 'white')
    drawLabel(f'Game Time: {int(app.game.timeElapsed)} seconds', 
              3*app.width/4, 550, size=20, font='orbitron', fill = 'white')

def home(app):
    if app.homeHover:
        factor = 1.2
    else:
        factor = 1
    drawImage(app.homeButton, app.width-40, 40, 
              width = 50*factor, height = 50*factor, align = 'center') 

