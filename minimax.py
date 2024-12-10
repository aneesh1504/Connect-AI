import numpy as np

def minimaxAlgorithm(board, depth, alpha, beta, playerToWin, maxPlayer, app):
    #define which player we are trying to beat using minimax
    if playerToWin == app.player2PieceColor:
        playerToLose = app.player1PieceColor
    else:
        playerToLose = app.player2PieceColor

    validLocations = app.game.getValidLocations(board, app)
    
    #return colour of winning piece if game has been won
    colorIfGameWon = checkWinOnBoard(board, app)
    gameDrawn = app.game.checkGameDraw(board, app)
    
    #if 0 depth has been reached or game has been won or drawn return out
    if depth == 0 or colorIfGameWon or gameDrawn:
        if colorIfGameWon == playerToLose:
            return (None, None, -100000000)
        elif colorIfGameWon == playerToWin:
            return (None, None, 100000000)
        elif gameDrawn:
            return (None, None, 0)
        else:
            return (None, None, generateScore(board, playerToWin, app))
    
    #if it is the player whose turn we are trying to maximise then 
    #calculate best move possible
    if maxPlayer:
        maxScore = float('-inf')
        bestMove = None
        for col in validLocations:
            row = app.game.findLowestRow(col, board, app)[0]
            boardCopy = board.copy()
            boardCopy[row][col] = playerToWin
            #enter recursive case to calculate score of chosen sequence 
            #of moves
            _, _, newScore = minimaxAlgorithm(boardCopy, depth-1, 
                                              alpha, beta, 
                                              playerToWin, 
                                              False, app)
            if newScore > maxScore:
                maxScore = newScore
                bestMove = (row, col)
            #prune the branch if beta cutoff is reached
            alpha = max(alpha, maxScore)
            if alpha > beta:
                break
        return bestMove[0], bestMove[1], maxScore
    
    #if it is the player whose turn we are trying to minimize then 
    #calculate the best move possible so that we can still formulate 
    #a winning sequence if they play the best move
    else:
        minScore = float('inf')
        bestMove = None
        for col in validLocations:
            row = app.game.findLowestRow(col, board, app)[0]
            boardCopy = board.copy()
            boardCopy[row][col] = playerToLose
            _, _, newScore = minimaxAlgorithm(boardCopy, depth-1, alpha, beta, 
                                              playerToWin, True, app)
            if newScore < minScore:
                minScore = newScore
                bestMove = (row, col)
            beta = min(beta, minScore)
            if alpha > beta:
                break
        return bestMove[0], bestMove[1], minScore

def checkWinOnBoard(board, app):
    #if we start from a certain location and there are 4 pieces consecutively
    #then there is a win on the board
    for row in range(0, app.rows):
        for col in range(0, app.cols):
            if board[row][col] is not None:
                if app.game.checkGameWin(row, col, board, app) is not None:
                    return board[row][col]
    return None

def generateScore(board, piece, app):
    score = 0

    if piece == app.player1PieceColor:
        oppPiece = app.player2PieceColor  
    else:
        oppPiece = app.player1PieceColor

    #determine game stage based on total pieces
    totalPieces = np.count_nonzero(board != None)
    if totalPieces < 14:
        positionalWeightMultiplier = 1.2
        windowMultiplier = 0.8
    elif totalPieces < 28:
        positionalWeightMultiplier = 1.0
        windowMultiplier = 1.0
    else:
        positionalWeightMultiplier = 0.5
        windowMultiplier = 1.5

    positionalWeights = np.array([
        [3, 4, 5, 7, 5, 4, 3],
        [4, 6, 8,10, 8, 6, 4],
        [5, 8,11,13,11, 8, 5],
        [5, 8,11,13,11, 8, 5],
        [4, 6, 8,10, 8, 6, 4],
        [3, 4, 5, 7, 5, 4, 3]
    ])

    #calculate positional score for player and opponent
    playerPositions = np.where(board == piece, 1, 0)
    playerPositionalScore = (np.sum(playerPositions * positionalWeights) * 
                             positionalWeightMultiplier)

    opponentPositions = np.where(board == oppPiece, 1, 0)
    opponentPositionalScore = (np.sum(opponentPositions * positionalWeights) * 
                               positionalWeightMultiplier)

    #net positional score
    score += (playerPositionalScore - opponentPositionalScore)

    #evaluate windows based on stages
    score += evaluateAllWindows(board, piece, oppPiece, app, windowMultiplier)

    return score

def evaluateAllWindows(board, piece, oppPiece, app, windowMultiplier):
    score = 0

    #horizontal 4-in-a-row check
    for row in range(app.rows):
        for col in range(app.cols - 3):
            window = board[row, col:col + 4]
            score += evaluateWindow(window, piece, oppPiece, 
                                    app, windowMultiplier)

    #vertical 4-in-a-row check
    for row in range(app.rows - 3):
        for col in range(app.cols):
            window = board[row:row + 4, col]
            score += evaluateWindow(window, piece, oppPiece, 
                                    app, windowMultiplier)

    #negative slope diagonal check
    for row in range(app.rows - 3):
        for col in range(app.cols - 3):
            window = [board[row + i][col + i] for i in range(4)]
            score += evaluateWindow(window, piece, oppPiece, 
                                    app, windowMultiplier)

    #positive slope diagonal check
    for row in range(3, app.rows):
        for col in range(app.cols - 3):
            window = [board[row - i][col + i] for i in range(4)]
            score += evaluateWindow(window, piece, oppPiece, 
                                    app, windowMultiplier)

    return score

def evaluateWindow(window, piece, oppPiece, app, windowMultiplier):
    score = 0
    windowList = list(window)

    #score opponent
    if windowList.count(oppPiece) == 4 and windowList.count(None) == 0:
        score -= 120
    if windowList.count(oppPiece) == 3 and windowList.count(None) == 1:
        score -= 90

    #score player
    if windowList.count(piece) == 4:
        score += 100
    elif windowList.count(piece) == 3 and windowList.count(None) == 1:
        score += 70
    elif windowList.count(piece) == 2 and windowList.count(None) == 2:
        score += 30

    score *= windowMultiplier

    return score


#citation: drew inspiration from connect 4 minimax implemented here:
#https://github.com/KeithGalli/Connect4-Python/blob/master/connect4_with_ai.py#L168
#modified minimax and added a positional scoring system