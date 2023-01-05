#Idea to select squares manually: Use commands such a "left" or "down" and then ask how many spaces. Type "select" to change the square
#Use a white scquare to indicate the location of the "cursor"

import random
import copy
import time

board = []

#Creates a board with each cell having a certain probability to start alive or dead
def buildRandomBoard(length, height, probability):
    global board

    for y in range(height):
        row = []
        for x in range(length):
            randomInt = random.randint(0, 100)
            if randomInt <= probability and probability != 0:
                row.append("#")
            else: 
                row.append(" ")
        board.append(row)

#Prints the current board to console, but I want to change this in the future because you can see movement as each line prints :(
def printBoard():
    print("\n" * 5)
    for row in range(len(board)):
        newLine = ""
        for col in range(len(board[0])):
            newLine += board[row][col]
        print(newLine)

#Determines whether the requested cell is alive or dead
def checkStatus(row, col, currentBoard):
    if currentBoard[row][col][0] == '#':
        return 1
    else:
        return 0

#I don't know how I made this part but I tried to add enough notes to understand it later...
def updateBoard():
    #y is row, x is col
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

    #These are the dimensions that happen to fit the Visual Studio console on my screen, I can add customization later
    gameLength = 148
    gameHeight = 47
    
    buildRandomBoard(gameLength, gameHeight, startingProbability)

    #Change this later, this is just for testing purposes
    for i in range(50):
        printBoard()
        updateBoard()
        time.sleep(0.5)

start()
