import random
from tkinter import *
from tkinter.messagebox import *
import tkinter.font as tkFont

class TicTacToe:
    
    def __init__(self, window):
        'constructor for TicTacToe'
        self.menu = window
        Frame(self.menu, height=800, width=800).grid()
        self.menu.title("Menu")
        Label(self.menu, text="Welcome to the unbeatable Tic Tac Toe Game").grid(row=0)
        Button(self.menu, text='Start New Game', command=self.startGame).grid(row=1, column=0, columnspan=1, sticky=W)
        Button(self.menu, text='Quit', command=self.menu.quit).grid(row=1, column=1, columnspan=1)

        self.whoWon = Player(' ')
        self.resumeGame = False
        self.currentPlayer = None
        self.player = None
        self.ai = None


    def newGame(self):
        'resets the board for a new game'
        self.board = [None] * 9
        self.buttonList = [None]*9
        self.placeTaken = [False]*9
        self.checkMove = self.board        

    def startGame(self):
        'starts the game'
        if self.resumeGame == False:
           self.menu.withdraw()
        self.newGame()
        self.setGameSymbol()

    def generateBoard(self):
        'generates a new board'
        self.gameBoardWindow = Tk()
        self.gameBoardWindow.title("Game Board")
        Frame(self.gameBoardWindow, height=800, width=800).grid(columnspan=3, rowspan=3)
        for i, each in enumerate(self.board):
            x, y = self.oneDtoTwoD(i)
            self.buttonList[i] = Button(self.gameBoardWindow, text= "", command=self.lambda_generator(i))
            self.buttonList[i].grid(column=x, row=y, sticky=(N, S, E, W))

    def oneDtoTwoD(self, i):
        'turns a one dimensional array into a two dimensional'
        # creates x and y coords for board layout
        x = int(i % 3)
        y = int(i / 3)
        return x, y

    def lambda_generator(self, i):
        'lambda function for board buttons'
        return lambda: self.turn(i)

    def pickX(self):
        'Picks who goes first'
        # Creates new window to pick who goes first
        first = Tk()
        first.title("Who will go first?")
        Label(first, text="I'm thinking of a number between 1 and 10.\nYou and my AI will pick a number and whoever is closest gets to start as X.").pack()
        randNum = random.randint(1, 10)

        # Asks for usr guess
        label = Label(first, text="Make your choice")
        label.pack()

        entry = Entry(first)
        entry.pack()
        Button(first, text="Good Luck", command=lambda: self.whoGoesFirst(entry)).pack()

    def setGameSymbol(self):
        'sets the Player symbol'
        # if the human wants to replay
        if self.resumeGame == True:
            if self.whoWon == self.player:
                showinfo(title="Winner", message="Because you won you will start first as 'X's")
                self.playerPickWin()
            elif self.whoWon == self.ai:
                showinfo(title="Loser", message= "Because you lost you will start second as 'O's")
                self.playerPickLose()
            else:
                showinfo("Who Goes First", message= "We need to find out who will start as 'X' and go first")
                self.pickX()
                
        # if this is first game
        else:
            showinfo("Who Goes First", message= "We need to find out who will start as 'X' and go first")
            self.pickX()

    def playerPickWin(self):
        'human won and sets symbol to x'
        self.player = Player('X')
        self.ai = Player('O')
        self.currentPlayer = self.player
        self.generateBoard()

    def playerPickLose(self):
        'human lost and sets symbol to o'
        self.player = Player('O')
        self.ai = Player('X')
        self.currentPlayer = self.ai
        self.generateBoard()
        self.aiTurn()

    def whoGoesFirst(self, ent):
        'Checks who goes first'
        # Checks ent for a valid entry
        try:
            playerGuess = int(ent.get())
            if not 0 < playerGuess < 11:
                raise ValueError
        except ValueError:
            showinfo(title="Not Valid", message="Enter a valid number.")
            ent.delete(0, END)
            return

        # Generates random number to compare against
        compareGuess = random.randint(1, 10)
        aiGuess = random.randint(1, 10)
        playerDelta = abs(playerGuess - compareGuess)
        aiDelta = abs(aiGuess - compareGuess)
        startingPosition = ''

        # Picks who goes first
        if playerDelta <= aiDelta:
            self.playerPickWin()
            startingPosition = 'first'
        else:
            self.playerPickLose()
            startingPosition = 'second'

        # Displays who goes first
        showinfo(title="Your Piece", message=f"My number was {compareGuess}, and the ai picked {aiGuess}.\nYou will be going {startingPosition} as {self.player.playerSymbol}")
        ent.master.destroy()        

    def turn(self, i):
        'checks if position is available, places piece, and ends turn'
        # if self.board[i]:
        #     showinfo(title="No Move", message="This position is already filled.")
        # Places down playerSymbol on board
        self.board[i] = self.currentPlayer.playerSymbol

        # Updates buttonList to show new button text
        self.buttonList[i].config(text= self.currentPlayer.playerSymbol, state=DISABLED)
        self.buttonList[i].update_idletasks()
        self.placeTaken[i] = True
        self.endTurn()

    def endTurn(self):
        if self.checkWin(self.board) or self.checkStalemate(self.board):
            if self.replay():
                self.gameBoardWindow.destroy()
                self.startGame()
            else:
                quit()
        elif self.currentPlayer == self.player:
            self.currentPlayer = self.ai
            print("ai flip")
            self.aiTurn()
        else:
            print("player flip")
            self.currentPlayer = self.player
        print(f"{self.board}")

    def aiTurn(self):
        # validMove = False
        # while not validMove:
        #     move = random.randint(0, 8)
        #     if self.placeTaken[move] == False:
        #         self.turn(move)
        #         validMove = True

        moveCounter = 0
        initialMove = 0
        score = 0
        validMove = False
        if self.checkWin(checkMove):
            score = 1
        elif self.checkStalemate(checkMove):
            score = 0
        else:
            score = -1
            
        if score == 1:
            validMove = False
            while not validMove:
                if self.placeTaken[initialMove] == False:
                    self.turn(initialMove)
                    validMove = True
                initialMove += 1
        elif score == 0:
            validMove = False
            while not validMove:
                if self.placeTaken[initialMove] == False:
                    self.turn(initialMove)
                    validMove = True
                initialMove += 1
        else:
            while not checkMove:
                if self.checkMove[moveCounter] == '':
                    initialMove = moveCounter
                    self.checkMove[moveCounter] = self.ai.playerSymbol
                    moveCounter += 1 + self.aiTurn()
                else:
                    self.aiTurn()

    def checkWin(self, boardCheck):
        'checks all win conditions'
        # check horizontal
        for rowIndex in range(0, 3):
            isWinTrue = [False] * 3
            for colIndex in range(0, 3):
                if boardCheck[rowIndex * 3 + colIndex] == self.currentPlayer.playerSymbol:
                    isWinTrue[colIndex] = True
            if all(isWinTrue):
                self.whoWon = self.currentPlayer
                return True

        # check vertical
        for colIndex in range(0, 3):
            isWinTrue = [False] * 3
            for rowIndex in range(0, 3):
                if boardCheck[rowIndex * 3 + colIndex] == self.currentPlayer.playerSymbol:
                    isWinTrue[rowIndex] = True
            if all(isWinTrue):
                self.whoWon = self.currentPlayer
                return True

        # check diagonal
        if boardCheck[4] == self.currentPlayer.playerSymbol:
            if boardCheck[0] == boardCheck[4] and boardCheck[8] == boardCheck[4]:
                self.whoWon = self.currentPlayer
                return True
            elif boardCheck[2] == boardCheck[4] and boardCheck[6] == boardCheck[4]:
                self.whoWon = self.currentPlayer
                return True

    def checkStalemate(self, boardCheck):
        'checks tie'
        if all(boardCheck):
            self.whoWon = None
            return True
        else:
            return False

    def replay(self):
        'checks if human wants to replay and displays a winner'
        if self.whoWon != None:
            showinfo(title= "Winner", message= f"{self.currentPlayer.playerSymbol} is the winner!")
        else:
            showinfo(title= "Stalemate", message= "It was a draw")
        self.resumeGame = askyesno(title="Wanna play again?", message=f"Would you like to play again?")
        return self.resumeGame

class Player:

    def __init__(self, playerSymbol):
        'constructor for Player'
        self.playerSymbol = playerSymbol

root = Tk()
game = TicTacToe(root)
root.mainloop()

