
#Idea to select squares manually: Use commands such a "left" or "down" and then ask how many spaces. Type "select" to change the square
#Use a white scquare to indicate the location of the "cursor"

#Add auto calibrate board size

#Clean up random hanging inputes after screen clears

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
    cursorUpOne = '\x1b[1A' 
    eraseLine = '\x1b[2K' 
    for i in range(n): 
        sys.stdout.write(cursorUpOne) 
        sys.stdout.write(eraseLine) 

def playerOptions(linesToClear):
    print('Type "1" to auto-play the simulation, or type "2" to go forward one step')
    while True:
        stepProgression = input()
        while stepProgression == "2":
            deleteLastLines(2)
            #explanation of this line further down
            print('\033[%dA\033[2K' % (linesToClear), end='')
            printBoard()
            updateBoard()
            print('Type "1" to auto-play the simulation. Type "2" to advance to the next step. Type "3" to quit (Not yet implemented).')
            stepProgression = input()

        if stepProgression.lower() == "1":
            print("How many steps would you like to advance?")
            #Validate user input
            while True:
                steps = input()
                try:
                    steps = int(steps)
                except:
                    print("Please enter a whole number with numeric digits.")
                    continue
                if steps < 1:
                    print("Please enter a number greater than 0.")
                    continue
                break
            break
        else:
            print('Please type either "1" "2" or "3"')

    print("How much time, in seconds, should pass between steps? (A value around 0.5 is recommended)")
    #Validate user input
    while True:
        time = input()
        try:
            time = float(time)
        except:
            print("Please use numeric digits.")
            continue
        if time <= 0:
            print("Please enter a number greater than 0.")
            continue
        break

    return [steps, time]

def getDimensions():
    print('Type "1" to find optimal dimensions, or type "2" to set your own dimensions.')
    while True:
        dimensionChoice = input()
        if dimensionChoice == "2":
            print("Please enter the simulation width.\nWARNING: If width exceeds screen width, visuals of the simulation break.")
            while True:
                width = input()
                try:
                    width = int(width)
                except:
                    print("Please enter a whole number with numeric digits.")
                    continue
                if width < 3:
                    print("Please enter a number greater than two.")
                    continue
                break
            print("Please enter the simulation height.\nWARNING: If height exceeds screen height, visuals of the simulation break.")
            while True:
                height = input()
                try:
                    height = int(height)
                except:
                    print("Please enter a whole number with numeric digits.")
                    continue
                if height < 3:
                    print("Please enter a number greater than two.")
                    continue
                break
            break
        if dimensionChoice.lower() == "1":
            print("First let's find your maximum width.")
            print()
            print('A "#" will be printed on your screen. Hit enter to advance it one space to the right.')
            print('When it reaches the end of the screen and gets printed back on the left side, type "1"')
            print('If you need to go backwards a space, type "2"')
            print()
            print('You may now begin. Please press enter until the "#" loops back to the left side')
            print()
            widthTest = "#"
            while True:
                redoTest = False
                print(widthTest)
                userInput = input()

                if userInput == "":
                    widthTest = " " + widthTest
                    deleteLastLines(2)
                    continue
                if userInput == "2":
                    if widthTest[0] != "#":
                        widthTest = widthTest.replace(' ', '', 1)
                        deleteLastLines(2)
                        continue
                if userInput == "1":
                    deleteLastLines(1)
                    if len(widthTest) > 1:
                        print("^")
                        print('|  Is this arrow currently pointing at the "#"? (y/n)')
                        print("|")
                        while True:
                            correctLocation = input()
                            if correctLocation[0].lower() == "y":
                                break
                            if correctLocation[0].lower() == "n":
                                redoTest = True
                                print('Please adjust the "#" so it reaches the end of the screen and loops back to the left side.')
                                break
                            else:
                                print('Please type either "y" or "n"')
                        
                        if redoTest:
                            continue
                        break
                    else:
                        print('You have not advanced the "#" yet!')
                        print('Hit enter to advance the "#" until it passes the end of your screen.')
                        continue 
                else:
                    print('Please only hit enter, or type "1" or "2"')
                    continue
            width = len(widthTest) - 1

            print("\nNow let's find your maximum height.")
            print()
            print('Some messages will be printed on your screen. Hit enter to advance them one space up.')
            print('When the message saying "STOP WHEN I DISAPPEAR" goes off-screen, type "1"')
            print('If you go too far, type "2" redo the height test')
            print()
            print('You may now begin. Please press enter until only the final message remains on screen')
            print()
            heightTest = 1
            while True:
                if heightTest == 1:
                    print("WARNING, STOP SOON")
                    print("WARNING, STOP SOON")
                    print("WARNING, STOP SOON")
                    print("STOP WHEN I DISAPPEAR")
                    print('TYPE "1" WHEN YOU CAN ONLY SEE ME')
                redoTest = False
                userInput = input()

                if userInput == "":
                    heightTest += 1
                    print()
                    deleteLastLines(1)
                    continue
                if userInput == "2":
                    heightTest = 1
                    print("Disregard any messages above this statement. Please redo the height test now.")
                    continue
                if userInput == "1":
                    deleteLastLines(1)
                    if heightTest > 1:
                        print('Is the only message remaining at the top of the screen "TYPE "1" WHEN YOU CAN ONLY SEE ME" (y/n)')
                        while True:
                            correctLocation = input()
                            if correctLocation[0].lower() == "y":
                                break
                            if correctLocation[0].lower() == "n":
                                redoTest = True
                                break
                            else:
                                print('Please type either "y" or "n"')
                        
                        if redoTest:
                            heightTest = 1
                            print("Disregard any messages above this statement. Please redo the height test now.")
                            continue
                        break
                    else:
                        print('You have not advanced the messages yet!')
                        print('Hit enter to advance the messages until only the last one remains.')
                        continue 
                else:
                    print('Please type either "1" or "2"')
                    continue
            print(heightTest)
            height = heightTest - 3
            break
    return [width, height]

def start():
    print("Welcome to my rendition of Conway's Game of Life!")
    dimensions = getDimensions()
    gameLength = dimensions[0]
    gameHeight = dimensions[1]
    print("To start, please type the probability (0-100) that any square begins the game alive!")
    #Validate user input
    while True:
        startingProbability = input()
        try:
            startingProbability = int(startingProbability)
        except:
            print("Please enter a whole number with numeric digits.")
            continue
        if startingProbability not in range(101):
            print("Please enter a number between 0 and 100.")
            continue
        break

    print('')

    linesToClear = gameHeight + 2 
    buildRandomBoard(gameLength, gameHeight, startingProbability)
    printBoard()
    updateBoard()

    while True:
        getNewChoices = False
        playerOptionChoices = playerOptions(linesToClear)
        stepsToAdvance = playerOptionChoices[0]
        sleepTime = playerOptionChoices[1]

        estimatedSimulationTime = (stepsToAdvance * sleepTime) + (0.02365 * stepsToAdvance) 

        if estimatedSimulationTime < 60:
            print("The estimated simulation time is about %d second(s). Would you like to continue? (y/n)" % (estimatedSimulationTime))
            while True:
                continueSimulation = input()
                if continueSimulation[0].lower() == "y":
                    break
                if continueSimulation[0].lower() == "n":
                    getNewChoices = True
                    break
                else:
                    print('Please type either "(y)es" or "(n)o"')
            if getNewChoices:
                continue
            break
        else:
            print("The estimated simulation time is about %d minute(s). Are you sure you want to continue? (y/n)" % (estimatedSimulationTime / 60))
            while True:
                continueSimulation = input()
                if continueSimulation[0].lower() == "y":
                    break
                if continueSimulation[0].lower() == "n":
                    getNewChoices = True
                    break
                else:
                    print('Please type either "y" or "n"')
            if getNewChoices:
                continue
            break

    
    #This ensures the first line clear of the for loop below doesn't mess anything up
    print('\n' * (gameHeight + 1))

    for i in range(stepsToAdvance):
        #This statement makes the flicker go away
        #It basically clears all the previous lines and then moves the cursor back up to the top
        print('\033[%dA\033[2K' % (linesToClear), end='')        
        printBoard()
        updateBoard()
        time.sleep(sleepTime)
            

start()
