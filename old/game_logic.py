import random

from old.board_manager import COVERED
from old.board_manager import FLAGGED
from old.board_manager import UNCOVERED
from old.board_manager import MINE


class GameLogic:
    def __init__(self, board, mineCount):
        if mineCount < 10 or mineCount > 20:
            raise ValueError("Mine count must be between 10 and 20.")

        self.board = board
        self.mineCount = mineCount

        self.flagsRemaining = mineCount

        self.status = "Playing"

        self.firstClick = True
        self.minesPlaced = False

    def resetGame(self, mineCount):
        if mineCount < 10 or mineCount > 20:
            raise ValueError("Mine count must be between 10 and 20.")

        self.board.resetBoard()

        self.mineCount = mineCount
        self.flagsRemaining = mineCount

        self.status = "Playing"

        self.firstClick = True
        self.minesPlaced = False

    def placeMines(self, safeRow, safeColumn):
        possibleLocations = []

        for row in range(self.board.rows):
            for column in range(self.board.columns):

                # Keep the first clicked cell and the cells
                # surrounding it mine-free
                if (
                    abs(row - safeRow) <= 1
                    and abs(column - safeColumn) <= 1
                ):
                    continue

                possibleLocations.append((row, column))

        mineLocations = random.sample(
            possibleLocations,
            self.mineCount
        )

        for row, column in mineLocations:
            self.board.grid[row][column].hasMine = True

        self.calculateNumbers()

        self.minesPlaced = True

    def calculateNumbers(self):
        for row in range(self.board.rows):
            for column in range(self.board.columns):

                cell = self.board.grid[row][column]

                if cell.hasMine:
                    continue

                mineCount = 0

                neighbors = self.board.getNeighbors(row, column)

                for neighborRow, neighborColumn in neighbors:

                    neighbor = self.board.grid[
                        neighborRow
                    ][
                        neighborColumn
                    ]

                    if neighbor.hasMine:
                        mineCount += 1

                cell.adjacentMines = mineCount

    def uncoverCell(self, row, column):
        if self.status != "Playing":
            return

        if not self.board.isValidCell(row, column):
            return

        cell = self.board.grid[row][column]

        # Cannot uncover a flagged cell
        if cell.state == FLAGGED:
            return

        # Already uncovered
        if cell.state == UNCOVERED:
            return

        # Generate mines after the first click
        if self.firstClick:
            self.placeMines(row, column)
            self.firstClick = False

        # Mine was clicked
        if cell.hasMine:
            cell.state = MINE

            self.board.revealAllMines()

            self.status = "Game Over: Loss"

            return

        # Reveal normal cell
        self.revealRecursive(row, column)

        self.checkWin()

    def revealRecursive(self, row, column):
        if not self.board.isValidCell(row, column):
            return

        cell = self.board.grid[row][column]

        # Do not uncover flags
        if cell.state == FLAGGED:
            return

        # Stop if already uncovered
        if cell.state == UNCOVERED:
            return

        # Never recursively uncover mines
        if cell.hasMine:
            return

        cell.state = UNCOVERED

        # If there are adjacent mines, stop recursion
        if cell.adjacentMines > 0:
            return

        # If this cell is zero, uncover neighboring cells
        neighbors = self.board.getNeighbors(row, column)

        for neighborRow, neighborColumn in neighbors:
            self.revealRecursive(
                neighborRow,
                neighborColumn
            )

    def toggleFlag(self, row, column):
        if self.status != "Playing":
            return

        if not self.board.isValidCell(row, column):
            return

        cell = self.board.grid[row][column]

        # Cannot flag an uncovered cell
        if cell.state == UNCOVERED:
            return

        # Remove existing flag
        if cell.state == FLAGGED:
            cell.state = COVERED
            self.flagsRemaining += 1

        # Add a new flag
        elif cell.state == COVERED:

            # Do not allow more flags than mines
            if self.flagsRemaining <= 0:
                return

            cell.state = FLAGGED
            self.flagsRemaining -= 1

    def checkWin(self):
        for row in range(self.board.rows):
            for column in range(self.board.columns):

                cell = self.board.grid[row][column]

                # Every non-mine cell must be uncovered
                if not cell.hasMine and cell.state != UNCOVERED:
                    return

        self.status = "Victory"