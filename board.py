import random

from tile import Tile


class Board:
    def __init__(self, rows, columns, mineCount):
        self.rows = rows
        self.columns = columns
        self.mineCount = mineCount

        self.gameOver = False
        self.gameWon = False
        self.firstClick = True

        self.tiles = []

        self.makeBoard()

    def makeBoard(self):
        self.tiles = []

        for row in range(self.rows):
            newRow = []

            for column in range(self.columns):
                newRow.append(Tile(row, column))

            self.tiles.append(newRow)

    def placeMines(self, safeRow, safeColumn):
        possibleLocations = []

        for row in range(self.rows):
            for column in range(self.columns):

                # Keep first click and surrounding squares safe
                if abs(row - safeRow) <= 1 and abs(column - safeColumn) <= 1:
                    continue

                possibleLocations.append((row, column))

        mineLocations = random.sample(
            possibleLocations,
            self.mineCount
        )

        for row, column in mineLocations:
            self.tiles[row][column].isMine = True

        self.calculateNumbers()

    def calculateNumbers(self):
        for row in range(self.rows):
            for column in range(self.columns):

                tile = self.tiles[row][column]

                if tile.isMine:
                    continue

                tile.adjacent = self.countAdjacentMines(row, column)

    def countAdjacentMines(self, row, column):
        count = 0

        for rowChange in range(-1, 2):
            for columnChange in range(-1, 2):

                if rowChange == 0 and columnChange == 0:
                    continue

                newRow = row + rowChange
                newColumn = column + columnChange

                if self.isValid(newRow, newColumn):
                    if self.tiles[newRow][newColumn].isMine:
                        count += 1

        return count

    def isValid(self, row, column):
        return (
            row >= 0
            and row < self.rows
            and column >= 0
            and column < self.columns
        )

    def reveal(self, row, column):
        if self.gameOver or self.gameWon:
            return

        tile = self.tiles[row][column]

        if tile.flagged or tile.revealed:
            return

        # Generate mines only after first click
        if self.firstClick:
            self.placeMines(row, column)
            self.firstClick = False

        if tile.isMine:
            tile.revealed = True
            self.gameOver = True
            self.revealAllMines()
            return

        self.revealArea(row, column)

        self.checkWin()

    def revealArea(self, row, column):
        if not self.isValid(row, column):
            return

        tile = self.tiles[row][column]

        if tile.revealed or tile.flagged:
            return

        tile.revealed = True

        # Stop spreading once a numbered tile is reached
        if tile.adjacent > 0:
            return

        for rowChange in range(-1, 2):
            for columnChange in range(-1, 2):

                if rowChange == 0 and columnChange == 0:
                    continue

                newRow = row + rowChange
                newColumn = column + columnChange

                if self.isValid(newRow, newColumn):
                    neighboringTile = self.tiles[newRow][newColumn]

                    if not neighboringTile.isMine:
                        self.revealArea(newRow, newColumn)

    def toggleFlag(self, row, column):
        if self.gameOver or self.gameWon:
            return

        tile = self.tiles[row][column]

        if tile.revealed:
            return

        tile.flagged = not tile.flagged

    def revealAllMines(self):
        for row in self.tiles:
            for tile in row:
                if tile.isMine:
                    tile.revealed = True

    def getFlagCount(self):
        count = 0

        for row in self.tiles:
            for tile in row:
                if tile.flagged:
                    count += 1

        return count

    def checkWin(self):
        for row in self.tiles:
            for tile in row:

                if not tile.isMine and not tile.revealed:
                    return

        self.gameWon = True