import pygame
import time

from board import Board


pygame.init()


# --------------------------------
# GAME SETTINGS
# --------------------------------

DIFFICULTIES = {
    "Easy": {
        "rows": 8,
        "columns": 10,
        "mines": 10,
        "tileSize": 45
    },

    "Medium": {
        "rows": 14,
        "columns": 18,
        "mines": 40,
        "tileSize": 32
    },

    "Hard": {
        "rows": 20,
        "columns": 24,
        "mines": 99,
        "tileSize": 28
    }
}


difficulty = "Medium"

HEADER_HEIGHT = 80


# --------------------------------
# GOOGLE-STYLE COLORS
# --------------------------------

DARK_GREEN = (65, 112, 39)

GREEN_LIGHT = (170, 215, 81)
GREEN_DARK = (162, 209, 73)

TAN_LIGHT = (229, 194, 159)
TAN_DARK = (215, 184, 153)

RED = (234, 67, 53)

WHITE = (255, 255, 255)

NUMBER_COLORS = {
    1: (25, 118, 210),
    2: (56, 142, 60),
    3: (211, 47, 47),
    4: (123, 31, 162),
    5: (136, 14, 79),
    6: (0, 121, 107),
    7: (40, 40, 40),
    8: (100, 100, 100)
}


# --------------------------------
# FONTS
# --------------------------------

font = pygame.font.SysFont("Arial", 24, bold=True)
smallFont = pygame.font.SysFont("Arial", 20, bold=True)
bigFont = pygame.font.SysFont("Arial", 36, bold=True)


# --------------------------------
# CREATE GAME
# --------------------------------

def createGame():
    settings = DIFFICULTIES[difficulty]

    board = Board(
        settings["rows"],
        settings["columns"],
        settings["mines"]
    )

    width = settings["columns"] * settings["tileSize"]
    height = settings["rows"] * settings["tileSize"] + HEADER_HEIGHT

    screen = pygame.display.set_mode((width, height))

    return board, screen


board, screen = createGame()

pygame.display.set_caption("Minesweeper")


# --------------------------------
# TIMER
# --------------------------------

startTime = None


def getTime():
    if startTime is None:
        return 0

    if board.gameOver or board.gameWon:
        return int(endTime - startTime)

    return int(time.time() - startTime)


# --------------------------------
# DRAW FLAG
# --------------------------------

def drawFlag(x, y, size):
    poleX = x + size // 2

    pygame.draw.line(
        screen,
        (70, 70, 70),
        (poleX, y + size * 0.25),
        (poleX, y + size * 0.72),
        3
    )

    pygame.draw.polygon(
        screen,
        RED,
        [
            (poleX, y + size * 0.22),
            (poleX, y + size * 0.55),
            (x + size * 0.25, y + size * 0.38)
        ]
    )

    pygame.draw.line(
        screen,
        (70, 70, 70),
        (x + size * 0.30, y + size * 0.75),
        (x + size * 0.70, y + size * 0.75),
        3
    )


# --------------------------------
# DRAW MINE
# --------------------------------

def drawMine(x, y, size):
    centerX = x + size // 2
    centerY = y + size // 2

    radius = size // 5

    pygame.draw.circle(
        screen,
        (50, 50, 50),
        (centerX, centerY),
        radius
    )

    pygame.draw.line(
        screen,
        (50, 50, 50),
        (centerX - radius - 5, centerY),
        (centerX + radius + 5, centerY),
        3
    )

    pygame.draw.line(
        screen,
        (50, 50, 50),
        (centerX, centerY - radius - 5),
        (centerX, centerY + radius + 5),
        3
    )


# --------------------------------
# DRAW HEADER
# --------------------------------

def drawHeader():
    width = screen.get_width()

    pygame.draw.rect(
        screen,
        DARK_GREEN,
        (0, 0, width, HEADER_HEIGHT)
    )

    # Difficulty
    difficultyText = smallFont.render(
        difficulty,
        True,
        WHITE
    )

    screen.blit(
        difficultyText,
        (20, 28)
    )

    # Flag counter
    flagsRemaining = board.mineCount - board.getFlagCount()

    flagX = width // 2 - 90

    drawFlag(
        flagX,
        18,
        45
    )

    flagText = font.render(
        str(flagsRemaining),
        True,
        WHITE
    )

    screen.blit(
        flagText,
        (flagX + 40, 27)
    )

    # Timer
    timerText = font.render(
        f"{getTime():03}",
        True,
        WHITE
    )

    screen.blit(
        timerText,
        (width // 2 + 40, 27)
    )


# --------------------------------
# DRAW BOARD
# --------------------------------

def drawBoard():
    tileSize = DIFFICULTIES[difficulty]["tileSize"]

    for row in range(board.rows):
        for column in range(board.columns):

            tile = board.tiles[row][column]

            x = column * tileSize
            y = row * tileSize + HEADER_HEIGHT

            # Revealed square
            if tile.revealed:

                if (row + column) % 2 == 0:
                    color = TAN_LIGHT
                else:
                    color = TAN_DARK

            # Hidden square
            else:

                if (row + column) % 2 == 0:
                    color = GREEN_LIGHT
                else:
                    color = GREEN_DARK

            pygame.draw.rect(
                screen,
                color,
                (x, y, tileSize, tileSize)
            )

            # Flag
            if tile.flagged and not tile.revealed:
                drawFlag(x, y, tileSize)

            # Mine
            elif tile.revealed and tile.isMine:
                drawMine(x, y, tileSize)

            # Number
            elif tile.revealed and tile.adjacent > 0:

                numberColor = NUMBER_COLORS[tile.adjacent]

                numberText = font.render(
                    str(tile.adjacent),
                    True,
                    numberColor
                )

                textRectangle = numberText.get_rect(
                    center=(
                        x + tileSize // 2,
                        y + tileSize // 2
                    )
                )

                screen.blit(
                    numberText,
                    textRectangle
                )


# --------------------------------
# GAME OVER MESSAGE
# --------------------------------

def drawMessage():
    if not board.gameOver and not board.gameWon:
        return

    overlay = pygame.Surface(
        (
            screen.get_width(),
            screen.get_height()
        ),
        pygame.SRCALPHA
    )

    overlay.fill((0, 0, 0, 100))

    screen.blit(overlay, (0, 0))

    if board.gameWon:
        message = "You Win!"
    else:
        message = "Game Over"

    text = bigFont.render(
        message,
        True,
        WHITE
    )

    rectangle = text.get_rect(
        center=(
            screen.get_width() // 2,
            screen.get_height() // 2
        )
    )

    screen.blit(text, rectangle)


# --------------------------------
# MAIN LOOP
# --------------------------------

clock = pygame.time.Clock()

running = True
endTime = 0


while running:

    # ----------------------------
    # EVENTS
    # ----------------------------

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:

            mouseX, mouseY = pygame.mouse.get_pos()

            # Ignore header clicks for now
            if mouseY < HEADER_HEIGHT:
                continue

            tileSize = DIFFICULTIES[difficulty]["tileSize"]

            column = mouseX // tileSize
            row = (mouseY - HEADER_HEIGHT) // tileSize

            if row >= board.rows or column >= board.columns:
                continue

            # Left click
            if event.button == 1:

                if startTime is None:
                    startTime = time.time()

                board.reveal(row, column)

            # Right click
            elif event.button == 3:

                board.toggleFlag(row, column)

            if board.gameOver or board.gameWon:

                if startTime is not None:
                    endTime = time.time()


    # ----------------------------
    # DRAW
    # ----------------------------

    drawHeader()

    drawBoard()

    drawMessage()

    pygame.display.flip()

    clock.tick(60)


pygame.quit()