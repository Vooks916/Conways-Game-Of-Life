
#Idea to select squares manually: Use commands such a "left" or "down" and then ask how many spaces. Type "select" to change the square
#Use a white scquare to indicate the location of the "cursor"

#Add customization to size of board

#Add a detector if the simulation will take a significant amount of time

import random
import copy
import time
import sys

board = []

#Creates a board with each cell having a certain probability to start alive or dead
def buildRandomBoard(length, height, probability):
    global board
    board = []

    for y in range(height):
        row = []
        for x in range(length):
            randomInt = random.randint(0, 100)
            if randomInt <= probability and probability != 0:
                row.append("#")
            else: 
                row.append(" ")
        board.append(row)

#Prints the board with minimal flicker effect by combining it all into one string
def printBoard():
    boardToPrint = ""
    for row in range(len(board)):
        newLine = ""
        for col in range(len(board[0])):
            boardToPrint += board[row][col]
        boardToPrint += "\n"
    print('')
    print(boardToPrint)

#Determines whether the requested cell is alive or dead
def checkStatus(row, col, currentBoard):
    if currentBoard[row][col] == '#':
        return 1
    else:
        return 0

#I don't know how I made this part but I tried to add enough notes to understand it later...
def updateBoard():
    global board
    boardCopy = copy.deepcopy(board)

    for y in range(len(boardCopy)):
        y -= 1

        for x in range(len(boardCopy[0])):
            #Find number of alive neighbors for each cell.
            aliveNeighbors = 0
            x -= 1

            #Search the 3x3 area around the current cell
            for i in range(3):
                #If the cell below doesn't exist, loop back around to the top
                if y + i >= len(boardCopy):
                    #When adding y to i below, i will be 2, so set y to -2 to ensure final y coordinate is 0
                    y = -2

                for j in range(3):
                    #Do not check the cell itself, only it's neighbors
                    if i == 1 and j == 1:
                        continue
                    #If the cell to the right doesn't exist, loop back around to the left
                    if x + j >= len(boardCopy[0]):
                        #When adding x to j below, j will be 2, so set x to -2 to ensure final x coordinate is 0
                        x = -2
    
                    #checkStatus returns 1 if the cell is alive, and 0 if not
                    aliveNeighbors += checkStatus(y + i, x + j, boardCopy)

            #If there are 2 alive neighbors, no change to the cell is needed
            #Also quick question for later, why doesn't this work without the continues?
            if aliveNeighbors == 2:
                continue
            if aliveNeighbors == 3:
                board[y + 1][x + 1] = '#'
                continue
            else:
                board[y + 1][x + 1] = ' '
                continue

def deleteLastLines(n):
    CURSOR_UP_ONE = '\x1b[1A' 
    ERASE_LINE = '\x1b[2K' 
    for i in range(n): 
        sys.stdout.write(CURSOR_UP_ONE) 
        sys.stdout.write(ERASE_LINE) 

def start():
    print("Welcome to my rendition of Conway's Game of Life!")
    print("Right now you cannot make your own board, but that might be added in the future.")
    print("To start, please type the probability (0-100) that any square begins the game alive!")
    
    #Validate user input
    while True:
        startingProbability = input()
        try:
            startingProbability = int(startingProbability)
        except:
            print("Please use numeric digits.")
            continue
        if startingProbability not in range(101):
            print("Please enter a number between 0 and 100.")
            continue
        break

    print('')

    #These are the dimensions that happen to fit the Visual Studio console on my screen, I can add customization later
    #DO NOT change gameHeight at the moment or it will break
    gameLength = 148
    gameHeight = 43

    buildRandomBoard(gameLength, gameHeight, startingProbability)

    printBoard()
    updateBoard()

    print('Type "auto" to play the simulation, or type "next" to go forward one step')
    while True:
        stepProgression = input()
        while stepProgression.lower() == "next":
            deleteLastLines(2)
            #explanation of this line further down
            print('\033[47A\033[2K', end='')
            printBoard()
            updateBoard()
            print('Type "next" to advance to the next step. Type "auto" to play the simulation. Type "quit" to stop (Not yet implemented).')
            stepProgression = input()

        if stepProgression.lower() == "auto":
            print("How many steps would you like to advance?")
            #Validate user input
            while True:
                stepsToAdvance = input()
                try:
                    stepsToAdvance = int(stepsToAdvance)
                except:
                    print("Please use numeric digits.")
                    continue
                if stepsToAdvance < 1:
                    print("Please enter a number greater than 0.")
                    continue
                break
            break
        else:
            print('Please type either "next" or "auto"')

    print("How much time, in seconds, should pass between steps? (A value around 0.5 is recommended)")
    #Validate user input
    while True:
        sleepTime = input()
        try:
            sleepTime = float(sleepTime)
        except:
            print("Please use numeric digits.")
            continue
        if sleepTime <= 0:
            print("Please enter a number greater than 0.")
            continue
        break
    
    #This ensures the first line clear of the for loop below doesn't mess anything up
    print('\n' * (gameHeight + 1))

    for i in range(stepsToAdvance):
        #This witchcraft makes the flicker go away
        #It basically clears all the previous lines and then moves the cursor back up to the top
        print('\033[47A\033[2K', end='')        
        printBoard()
        updateBoard()
        time.sleep(sleepTime)
            

start()