class TorusGrid:

    def __init__ (self, numRows, numCols):
        self.rows = numRows
        self.cols = numCols
        self.data = [[0 for j in range(numRows)] for i in range(numCols)]
    
    def __str__(self):
        string = ""
        for i in range(self.rows):
            for j in range(self.cols):
                string += str(self.data[j][i])
                string += " "
            string += "\n"
        return string
    
    def get(self, x, y):
        return self.data[x % self.cols][y % self.rows]
    
    def set(self, x, y, val):
        self.data[x % self.cols][y % self.rows] = val
        return
    
    def pad(self, padwidth, padheight):
        if padheight < 0 or padwidth < 0:
            raise IndexError("Can't pad a negative number")
        self.data = [[0 for j in range(self.rows)] for i in range(padwidth//2)] + self.data
        self.data = self.data + [[0 for j in range(self.rows)] for i in range(padwidth//2)]
        self.cols += (padwidth // 2) * 2
        for i in range(self.cols):
            self.data[i] = [0 for j in range(padheight//2)] + self.data[i]
            self.data[i] = self.data[i] + [0 for j in range(padheight//2)]
        self.rows += (padheight//2) * 2

class GameGrid:

    def __init__(self, initial):
        with open(initial, 'r') as initState:
            self.liveCells = set() # Set of all the live cells
            isFirstLine = True
            i = 0
            j = 0
            for line in initState:
                if isFirstLine:
                    firstLine = line.split()
                    self.grid = TorusGrid(int(firstLine[0]),int(firstLine[1]))
                    isFirstLine = False
                else:
                    for token in line.split():
                        if token == "1":
                            self.grid.set(i,j,int(token))
                            self.liveCells.add((i,j)) # If the cell starts off alive, add it to liveCells
                        i += 1
                    i = 0
                    j += 1
        
    def __str__(self):
        return str(self.grid)
    
    def rows(self):
        return self.grid.rows
    
    def cols(self):
        return self.grid.cols
    
    def strAt(self, x, y, numCols,numRows):
        string = ""
        for j in range(numRows):
            for i in range(numCols):
                string += str(self.grid.get(x+i,y+j)) + " "
            string += "\n"
        return string

    def update(self):
        # Initializes sets
        adjDeadCells = set()
        cellsToKill = set()
        cellsToBirth = set()

        # For each alive cell, counts the surrounding population
        # For each surrounding dead cell, adds to a list of cells to check for birth
        for cell in self.liveCells:
            adjLive = -1 # Starts at -1 to offset it counting itself
            for xos in [-1,0,1]:
                for yos in [-1,0,1]:
                    if self.grid.get(cell[0]+xos, cell[1]+yos) == 1: # If adj cell is alive, add 1 to adjLive
                        adjLive += 1
                    elif self.grid.get(cell[0]+xos, cell[1]+yos) == 0: # If adj cell is dead, add its coords to adjDead
                        adjDeadCells.add((cell[0]+xos, cell[1]+yos))
            
            # Adds the proper cells to a set of cells to kill
            if adjLive < 2: # Underpopulation
                cellsToKill.add(cell)
            elif adjLive > 3: # Overpopulation
                cellsToKill.add(cell)
        
        # For each dead cell adjacent to a live cell, checks how many live cells are adjacent
        for cell in adjDeadCells:
            adjLive = 0
            for xos in [-1,0,1]:
                for yos in [-1,0,1]:
                    if self.grid.get(cell[0]+xos, cell[1]+yos) == 1: # If adj cell is alive, add 1 to adjLive
                        adjLive += 1
            
            # Adds the proper cells to a set of cells to birth
            if adjLive == 3:
                cellsToBirth.add(cell)
        
        # Births cells in cellsToBirth, and kills cells in cellsToKill
        # Also updates the liveCells set
        for cell in cellsToBirth:
            self.grid.set(cell[0], cell[1], 1)
            self.liveCells.add(cell)
        for cell in cellsToKill:
            self.grid.set(cell[0], cell[1], 0)
            self.liveCells.remove(cell)
    
    def reinit_live(self):
        self.liveCells.clear()
        for i in range(self.cols()):
            for j in range(self.rows()):
                if self.grid.get(i,j) == 1:
                    self.liveCells.add((i,j))

if __name__ == "__main__":
    myGrid = TorusGrid(3,3)
    myGrid.set(0,0,1)
    myGrid.set(2,0,1)
    myGrid.set(0,2,1)
    myGrid.set(2,2,1)
    print(myGrid)

    myGrid.pad(6,3)
    print(myGrid)
    
