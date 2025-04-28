import sys
from Game import Game
from blessed import Terminal

if __name__=="__main__":
    term = Terminal()
    print(term.clear + term.home, end = '')
    myGame = Game(sys.argv[1], term)
    myGame.gameLoop()