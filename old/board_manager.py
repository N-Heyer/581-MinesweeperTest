# Cell state values
COVERED = 0
FLAGGED = 1
UNCOVERED = 2
MINE = 3


class Cell:
    def __init__(self):
        self.state = COVERED
        self.hasMine = False
        self.adjacentMines = 0


class BoardManager:
    def __init__(self):
        self.rows = 10
        self.columns = 10

        self.grid = []

        self.makeBoard()

    def makeBoard(self):
        self.grid = []

        for row in range(self.rows):
            newRow = []

            for column in range(self.columns):
                newRow.append(Cell())

            self.grid.append(newRow)

    def resetBoard(self):
        self.makeBoard()

    def isValidCell(self, row, column):
        if row < 0 or row >= self.rows:
            return False

        if column < 0 or column >= self.columns:
            return False

        return True

    def getNeighbors(self, row, column):
        neighbors = []

        for rowChange in range(-1, 2):
            for columnChange in range(-1, 2):

                # Do not include the cell itself
                if rowChange == 0 and columnChange == 0:
                    continue

                newRow = row + rowChange
                newColumn = column + columnChange

                if self.isValidCell(newRow, newColumn):
                    neighbors.append((newRow, newColumn))

        return neighbors

    def revealAllMines(self):
        for row in range(self.rows):
            for column in range(self.columns):

                cell = self.grid[row][column]

                if cell.hasMine:
                    cell.state = MINE