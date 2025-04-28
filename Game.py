from Grids import GameGrid
from blessed import Terminal

class Game:

    def __init__(self, initial, terminal, infinite = True, delay = 0.2, liveSymbol = "■", deadSymbol = "."):
        self.grid = GameGrid(initial)
        self.homeCol = 0
        self.homeRow = 0
        self.infinite = infinite
        self.term = terminal
        # Screen check: Height 26 Width 78
        print(self.term.clear)
        with self.term.hidden_cursor():
            while (self.term.height < 26 or self.term.width < 78):
                print(self.term.home + self.term.green + "Please resize your window to at least 26 height and 78 width.")
                print(f"Current Height: {self.term.height}  Current Width: {self.term.width}")
        if self.infinite == True:
            self.grid.grid.pad((self.term.width // 2) + 50, self.term.height + 50) # Add more to add an off screen buffer
            self.grid.reinit_live()
            self.homeCol = (self.grid.cols() - min(self.grid.cols(), (self.term.width // 2) - 1)) // 2
            self.homeRow = (self.grid.rows() - min(self.grid.rows(), self.term.height - 1)) // 2
        self.delay = delay
        self.liveSymbol = liveSymbol
        self.deadSymbol = deadSymbol
        self.generation = 0
    
    def display(self):
        print(self.term.move_xy(0, 0),end = '')
        colsToDisplay = min(self.grid.cols(), (self.term.width // 2))
        rowsToDisplay = min(self.grid.rows(), self.term.height - 1)
        rawString = self.grid.strAt(self.homeCol, self.homeRow, colsToDisplay, rowsToDisplay)
        bakedString = rawString.replace("0", self.deadSymbol)
        bakedString = bakedString.replace("1", self.liveSymbol)
        # bakedString = bakedString.replace(" ", "")
        for line in bakedString.split("\n"):
            if line != '':
                print(self.term.green + line)
            #print(self.term.move_x((self.term.width-self.grid.cols())//2), end='')
        print(f'Generation: {self.generation}  Speed: {self.delay:2f}  Position: x={self.homeCol%self.grid.cols()} y={self.homeRow%self.grid.rows()}  Press q to stop.', end = '')
            # Maybe some information down at the bottom?
    
    def gameLoop(self):
        with self.term.hidden_cursor(), self.term.cbreak():
            print(self.term.clear + self.term.home + self.term.green + "_________                                     /\                           \n\_   ___ \  ____   ______  _  _______  ___.__.)/_____                      \n/    \  \/ /  _ \ /    \ \/ \/ /\__  \<   |  |/  ___/                      \n\     \___(  <_> )   |  \     /  / __ \\\\___  |\___ \                       \n \______  /\____/|___|  /\/\_/  (____  / ____/____  >                      \n        \/            \/             \/\/         \/                       ")
            print("  ________                                _____  .____    .__  _____       \n /  _____/_____    _____   ____     _____/ ____\ |    |   |__|/ ____\____  \n/   \  ___\__  \  /     \_/ __ \   /  _ \   __\  |    |   |  \   __\/ __ \ \n\    \_\  \/ __ \|  Y Y  \  ___/  (  <_> )  |    |    |___|  ||  | \  ___/ \n \______  (____  /__|_|  /\___  >  \____/|__|    |_______ \__||__|  \___  >\n        \/     \/      \/     \/                         \/             \/ \n")
            print("By: Daniel Sampson\n")
            print("Press any key to start.\n\nWhile game is active:\nz: Slow down\nx: Speed up\nArrow keys: Move focus\nq: Quit\n\n\nMade using Blessed Python library. ASCII art by patorjk at patorjk.com/software/taag", end = '')
            self.term.inkey()
            lastKey = self.term.inkey(timeout=0.001)
            while(lastKey != 'q'):
                if lastKey == 'z': # Slow down
                    self.delay *= 1.33
                elif lastKey == 'x': # Speed up
                    self.delay *= 0.75
                elif lastKey.name == "KEY_UP": # Move up
                    self.homeRow -= 1
                elif lastKey.name == "KEY_DOWN": # Move down
                    self.homeRow += 1
                elif lastKey.name == "KEY_LEFT": # Move left
                    self.homeCol -= 1
                elif lastKey.name == "KEY_RIGHT": # Move right
                    self.homeCol += 1
                self.display()
                self.grid.update()
                self.generation += 1
                lastKey = self.term.inkey(timeout=self.delay)
            print(self.term.move_xy(0, self.term.height - 1), end = '')
            print(f'Generation: {self.generation}  Speed: {self.delay:2f}  Position: x={self.homeCol%self.grid.cols()} y={self.homeRow%self.grid.rows()}  Press any key to end.', end = '', flush = True)
            self.term.inkey()
            print(self.term.clear + self.term.normal)
        return

if __name__=="__main__":
    term = Terminal()
    print(term.clear + term.home, end = '')
    myGame = Game("testinit2.txt", term)
    myGame.gameLoop()