import pygame

from old.board_manager import COVERED
from old.board_manager import FLAGGED
from old.board_manager import UNCOVERED
from old.board_manager import MINE


class UI:
    def __init__(self, screen):
        self.screen = screen

        self.tileSize = 44

        self.boardX = 80
        self.boardY = 165

        # Google Minesweeper inspired colors
        self.darkGreen = (70, 120, 45)

        self.greenLight = (170, 215, 81)
        self.greenDark = (162, 209, 73)

        self.tanLight = (229, 194, 159)
        self.tanDark = (215, 184, 153)

        self.white = (255, 255, 255)
        self.black = (45, 45, 45)
        self.red = (220, 50, 50)

        self.numberColors = {
            1: (25, 118, 210),
            2: (56, 142, 60),
            3: (211, 47, 47),
            4: (123, 31, 162),
            5: (136, 14, 79),
            6: (0, 121, 107),
            7: (40, 40, 40),
            8: (100, 100, 100)
        }

        self.font = pygame.font.SysFont(
            "Arial",
            25,
            bold=True
        )

        self.smallFont = pygame.font.SysFont(
            "Arial",
            20,
            bold=True
        )

        self.largeFont = pygame.font.SysFont(
            "Arial",
            34,
            bold=True
        )

        # Setup screen buttons
        self.minusButton = pygame.Rect(
            175,
            320,
            60,
            50
        )

        self.plusButton = pygame.Rect(
            365,
            320,
            60,
            50
        )

        self.startButton = pygame.Rect(
            200,
            410,
            200,
            60
        )

        # Game buttons
        self.restartButton = pygame.Rect(
            410,
            25,
            80,
            40
        )

        self.newGameButton = pygame.Rect(
            500,
            25,
            80,
            40
        )

    def drawSetup(self, mineCount):
        self.screen.fill((245, 245, 245))

        title = self.largeFont.render(
            "MINESWEEPER",
            True,
            self.darkGreen
        )

        titleRect = title.get_rect(
            center=(300, 120)
        )

        self.screen.blit(
            title,
            titleRect
        )

        label = self.smallFont.render(
            "Choose Number of Mines",
            True,
            self.black
        )

        labelRect = label.get_rect(
            center=(300, 250)
        )

        self.screen.blit(
            label,
            labelRect
        )

        # Minus button
        pygame.draw.rect(
            self.screen,
            self.darkGreen,
            self.minusButton,
            border_radius=8
        )

        minusText = self.largeFont.render(
            "-",
            True,
            self.white
        )

        minusRect = minusText.get_rect(
            center=self.minusButton.center
        )

        self.screen.blit(
            minusText,
            minusRect
        )

        # Mine count
        mineText = self.largeFont.render(
            str(mineCount),
            True,
            self.black
        )

        mineRect = mineText.get_rect(
            center=(300, 345)
        )

        self.screen.blit(
            mineText,
            mineRect
        )

        # Plus button
        pygame.draw.rect(
            self.screen,
            self.darkGreen,
            self.plusButton,
            border_radius=8
        )

        plusText = self.largeFont.render(
            "+",
            True,
            self.white
        )

        plusRect = plusText.get_rect(
            center=self.plusButton.center
        )

        self.screen.blit(
            plusText,
            plusRect
        )

        # Start button
        pygame.draw.rect(
            self.screen,
            self.darkGreen,
            self.startButton,
            border_radius=10
        )

        startText = self.smallFont.render(
            "START GAME",
            True,
            self.white
        )

        startRect = startText.get_rect(
            center=self.startButton.center
        )

        self.screen.blit(
            startText,
            startRect
        )

    def drawGame(self, game):
        self.screen.fill((245, 245, 245))

        self.drawHeader(game)

        self.drawColumnLabels()
        self.drawRowLabels()

        self.drawBoard(game)

    def drawHeader(self, game):
        pygame.draw.rect(
            self.screen,
            self.darkGreen,
            (0, 0, 600, 100)
        )

        mineText = self.smallFont.render(
            "Flags: " + str(game.flagsRemaining),
            True,
            self.white
        )

        self.screen.blit(
            mineText,
            (20, 25)
        )

        statusText = self.smallFont.render(
            game.status,
            True,
            self.white
        )

        statusRect = statusText.get_rect(
            center=(300, 45)
        )

        self.screen.blit(
            statusText,
            statusRect
        )

        # Restart button
        pygame.draw.rect(
            self.screen,
            (90, 145, 60),
            self.restartButton,
            border_radius=6
        )

        restartText = pygame.font.SysFont(
            "Arial",
            14,
            bold=True
        ).render(
            "Restart",
            True,
            self.white
        )

        restartRect = restartText.get_rect(
            center=self.restartButton.center
        )

        self.screen.blit(
            restartText,
            restartRect
        )

        # New game button
        pygame.draw.rect(
            self.screen,
            (90, 145, 60),
            self.newGameButton,
            border_radius=6
        )

        newText = pygame.font.SysFont(
            "Arial",
            12,
            bold=True
        ).render(
            "New Game",
            True,
            self.white
        )

        newRect = newText.get_rect(
            center=self.newGameButton.center
        )

        self.screen.blit(
            newText,
            newRect
        )

    def drawColumnLabels(self):
        for column in range(10):

            letter = chr(ord("A") + column)

            text = self.smallFont.render(
                letter,
                True,
                self.black
            )

            x = (
                self.boardX
                + column * self.tileSize
                + self.tileSize // 2
            )

            rectangle = text.get_rect(
                center=(x, self.boardY - 20)
            )

            self.screen.blit(
                text,
                rectangle
            )

    def drawRowLabels(self):
        for row in range(10):

            text = self.smallFont.render(
                str(row + 1),
                True,
                self.black
            )

            y = (
                self.boardY
                + row * self.tileSize
                + self.tileSize // 2
            )

            rectangle = text.get_rect(
                center=(self.boardX - 25, y)
            )

            self.screen.blit(
                text,
                rectangle
            )

    def drawBoard(self, game):
        for row in range(10):
            for column in range(10):

                cell = game.board.grid[row][column]

                x = (
                    self.boardX
                    + column * self.tileSize
                )

                y = (
                    self.boardY
                    + row * self.tileSize
                )

                # Covered or flagged cells
                if (
                    cell.state == COVERED
                    or cell.state == FLAGGED
                ):

                    if (row + column) % 2 == 0:
                        color = self.greenLight
                    else:
                        color = self.greenDark

                # Uncovered cells
                else:

                    if (row + column) % 2 == 0:
                        color = self.tanLight
                    else:
                        color = self.tanDark

                pygame.draw.rect(
                    self.screen,
                    color,
                    (
                        x,
                        y,
                        self.tileSize,
                        self.tileSize
                    )
                )

                if cell.state == FLAGGED:
                    self.drawFlag(
                        x,
                        y
                    )

                elif cell.state == MINE:
                    self.drawMine(
                        x,
                        y
                    )

                elif (
                    cell.state == UNCOVERED
                    and cell.adjacentMines > 0
                ):
                    self.drawNumber(
                        x,
                        y,
                        cell.adjacentMines
                    )

    def drawNumber(self, x, y, number):
        color = self.numberColors[number]

        text = self.font.render(
            str(number),
            True,
            color
        )

        rectangle = text.get_rect(
            center=(
                x + self.tileSize // 2,
                y + self.tileSize // 2
            )
        )

        self.screen.blit(
            text,
            rectangle
        )

    def drawFlag(self, x, y):
        centerX = x + self.tileSize // 2

        pygame.draw.line(
            self.screen,
            self.black,
            (
                centerX,
                y + 10
            ),
            (
                centerX,
                y + 33
            ),
            3
        )

        pygame.draw.polygon(
            self.screen,
            self.red,
            [
                (
                    centerX,
                    y + 10
                ),
                (
                    centerX,
                    y + 25
                ),
                (
                    x + 10,
                    y + 17
                )
            ]
        )

        pygame.draw.line(
            self.screen,
            self.black,
            (
                x + 12,
                y + 34
            ),
            (
                x + 32,
                y + 34
            ),
            3
        )

    def drawMine(self, x, y):
        centerX = x + self.tileSize // 2
        centerY = y + self.tileSize // 2

        pygame.draw.circle(
            self.screen,
            self.black,
            (
                centerX,
                centerY
            ),
            8
        )

        pygame.draw.line(
            self.screen,
            self.black,
            (
                centerX - 13,
                centerY
            ),
            (
                centerX + 13,
                centerY
            ),
            3
        )

        pygame.draw.line(
            self.screen,
            self.black,
            (
                centerX,
                centerY - 13
            ),
            (
                centerX,
                centerY + 13
            ),
            3
        )