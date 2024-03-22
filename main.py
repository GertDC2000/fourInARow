# # # imports
import sys
import time
import random
#import numpy as np
# # # vars
PLAYER_X = ' X ' # the player
PLAYER_O = ' O ' # the ai
EMPTY_SPACE = '{ }' # blank spaces

BOARD_WIDTH = 7
BOARD_HEIGHT = 6
COLUMN_LABELS = ('1', '2', '3', '4', '5', '6', '7')
assert len(COLUMN_LABELS) == BOARD_WIDTH

# # # functions
def getNewBoard():
    board = {}
    for columnIndex in range(BOARD_WIDTH):
        for rowIndex in range(BOARD_HEIGHT):
            board[(columnIndex, rowIndex)] = EMPTY_SPACE
    return board
 
def displayBoard(board):
    tileChars = []
    for rowIndex in range(BOARD_HEIGHT):
         for columnIndex in range(BOARD_WIDTH):
            tileChars.append(board[(columnIndex, rowIndex)])
 
    # show board:    
    print("""
      1  2  3  4  5  6  7 
    +---------------------+
    |{}{}{}{}{}{}{}|
    |{}{}{}{}{}{}{}|
    |{}{}{}{}{}{}{}|
    |{}{}{}{}{}{}{}|
    |{}{}{}{}{}{}{}|
    |{}{}{}{}{}{}{}|
    +---------------------+""".format(*tileChars)) #format allows different char to be used in the {} places 

#pick a random spot
def pickRandom(board):
    while True:
        spot = random.randint(0, BOARD_WIDTH-1)
        if board[(spot, 0)] == EMPTY_SPACE:
            return spot              

#pick best spot for AI
def pickBestMove(board):
	best_score = -10000
	bestSpot = random.choice(COLUMN_LABELS)
	for col in range(7):
            score = 0
            if board[(col, 0)] == EMPTY_SPACE:
                temp_board = board.copy()
                for rowIndex in range(BOARD_HEIGHT - 1, -1, -1):
                    if temp_board[(col, rowIndex)] == EMPTY_SPACE:
                        temp_board[(col, rowIndex)] = playerTurn
                        if isWinner(PLAYER_O ,temp_board):
                            return col
                        else:
                            score = 0
                if score > best_score:
                        best_score = score
                        bestSpot = col
                        
                

def aiCalculatedMove(board):
    print("loading move ...")
    
    chosenGrid = 0

    chosenGrid = pickRandom(board) #chose randomly a spot

    chosenGrid = pickBestMove(board) #let the ai chose

    if chosenGrid == 0:
        chosenGrid = pickRandom(board)
    columnIndex = int(chosenGrid) - 1

    for rowIndex in range(BOARD_HEIGHT - 1, -1, -1):
        if board[(columnIndex, rowIndex)] == EMPTY_SPACE:
            print("made move.")
            return (columnIndex, rowIndex)
    
 
def askForPlayerMove(playerTile, board):
    while True:
        print('Player {}, enter a column or QUIT:'.format(playerTile))
        response = input('> ').upper().strip()
 
        if response == 'QUIT':
            print('Thanks for playing!')
            sys.exit()

        if response not in COLUMN_LABELS:
            print('Enter a number from 1 to {}.'.format(BOARD_WIDTH))
            continue

        columnIndex = int(response) - 1

        # If the column is full, ask for a move again:
        if board[(columnIndex, 0)] != EMPTY_SPACE:
            print('That column is full, select another one.')
            continue

        # Starting from the bottom, find the first empty space.
        for rowIndex in range(BOARD_HEIGHT - 1, -1, -1):
            if board[(columnIndex, rowIndex)] == EMPTY_SPACE:
                return (columnIndex, rowIndex)

def isFull(board):
    for rowIndex in range(BOARD_HEIGHT):
        for columnIndex in range(BOARD_WIDTH):
            if board[(columnIndex, rowIndex)] == EMPTY_SPACE:
                return False  # Found an empty space, so return False.
    return True  # All spaces are full.

def isWinner(playerTile, board):

    # Go through the entire board, checking for four-in-a-row:
    for columnIndex in range(BOARD_WIDTH - 3):
        for rowIndex in range(BOARD_HEIGHT):
            # Check for horizontal 
            tile1 = board[(columnIndex, rowIndex)]
            tile2 = board[(columnIndex + 1, rowIndex)]
            tile3 = board[(columnIndex + 2, rowIndex)]
            tile4 = board[(columnIndex + 3, rowIndex)]
            if tile1 == tile2 == tile3 == tile4 == playerTile:
                return True
 
    for columnIndex in range(BOARD_WIDTH):
        for rowIndex in range(BOARD_HEIGHT - 3):
            # Check for vertical
            tile1 = board[(columnIndex, rowIndex)]
            tile2 = board[(columnIndex, rowIndex + 1)]
            tile3 = board[(columnIndex, rowIndex + 2)]
            tile4 = board[(columnIndex, rowIndex + 3)]
            if tile1 == tile2 == tile3 == tile4 == playerTile:
                return True

    for columnIndex in range(BOARD_WIDTH - 3):
        for rowIndex in range(BOARD_HEIGHT - 3):
            # Check for four-in-a-row going right-down diagonal:
            tile1 = board[(columnIndex, rowIndex)]
            tile2 = board[(columnIndex + 1, rowIndex + 1)]
            tile3 = board[(columnIndex + 2, rowIndex + 2)]
            tile4 = board[(columnIndex + 3, rowIndex + 3)]
            if tile1 == tile2 == tile3 == tile4 == playerTile:
                return True

            # Check for four-in-a-row going left-down diagonal:
            tile1 = board[(columnIndex + 3, rowIndex)]
            tile2 = board[(columnIndex + 2, rowIndex + 1)]
            tile3 = board[(columnIndex + 1, rowIndex + 2)]
            tile4 = board[(columnIndex, rowIndex + 3)]
            if tile1 == tile2 == tile3 == tile4 == playerTile:
                return True
    return False

# # # main program
#new game:
gameBoard = getNewBoard()
# player x for player, player 0 for ai
playerTurn = PLAYER_X

while True:  # Run a player's turn.
    # Display the board and get player's move:
    if playerTurn == PLAYER_O: #the AI
        displayBoard(gameBoard)

        aiMove = aiCalculatedMove(gameBoard)
        gameBoard[aiMove] = playerTurn

        time.sleep(1)# pause

    elif playerTurn == PLAYER_X: # the PLAYER
        displayBoard(gameBoard)
        playerMove = askForPlayerMove(playerTurn, gameBoard)
        gameBoard[playerMove] = playerTurn

    else: # if something breaks
        print("error, check player count or code for errors.")
        break

    # Check for a win or tie:
    if isWinner(playerTurn, gameBoard):
        displayBoard(gameBoard)
        print('Player ' + playerTurn + ' has won!')
        sys.exit()
    elif isFull(gameBoard):
        displayBoard(gameBoard)
        print('There is a tie!')
        sys.exit()

    # Switch turns to other player:
    if playerTurn == PLAYER_X:
        playerTurn = PLAYER_O
    elif playerTurn == PLAYER_O:
        playerTurn = PLAYER_X

""" 
#code example for super hard ai found on the web. 
#(inspiration for the ai part of the code: https://github.com/KeithGalli/Connect4-Python/blob/master/connect4_with_ai.py#L123)

def minimax(board, depth, alpha, beta, maximizingPlayer):
	valid_locations = get_valid_locations(board)
	is_terminal = is_terminal_node(board)
	if depth == 0 or is_terminal:
		if is_terminal:
			if winning_move(board, AI_PIECE):
				return (None, 100000000000000)
			elif winning_move(board, PLAYER_PIECE):
				return (None, -10000000000000)
			else: # Game is over, no more valid moves
				return (None, 0)
		else: # Depth is zero
			return (None, score_position(board, AI_PIECE))
	if maximizingPlayer:
		value = -math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			b_copy = board.copy()
			drop_piece(b_copy, row, col, AI_PIECE)
			new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
			if new_score > value:
				value = new_score
				column = col
			alpha = max(alpha, value)
			if alpha >= beta:
				break
		return column, value

	else: # Minimizing player
		value = math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			b_copy = board.copy()
			drop_piece(b_copy, row, col, PLAYER_PIECE)
			new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
			if new_score < value:
				value = new_score
				column = col
			beta = min(beta, value)
			if alpha >= beta:
				break
		return column, value

"""