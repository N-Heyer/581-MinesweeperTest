import pygame


class InputHandler:
    def __init__(self, boardX, boardY, tileSize):
        self.boardX = boardX
        self.boardY = boardY
        self.tileSize = tileSize

    def getClickedCell(self, mousePosition):
        mouseX = mousePosition[0]
        mouseY = mousePosition[1]

        relativeX = mouseX - self.boardX
        relativeY = mouseY - self.boardY

        if relativeX < 0 or relativeY < 0:
            return None

        column = relativeX // self.tileSize
        row = relativeY // self.tileSize

        if row < 0 or row >= 10:
            return None

        if column < 0 or column >= 10:
            return None

        return row, column

    def handleEvent(self, event, game):
        if event.type != pygame.MOUSEBUTTONDOWN:
            return

        clickedCell = self.getClickedCell(event.pos)

        if clickedCell is None:
            return

        row, column = clickedCell

        # Left mouse click = uncover
        if event.button == 1:
            game.uncoverCell(row, column)

        # Right mouse click = flag
        elif event.button == 3:
            game.toggleFlag(row, column)