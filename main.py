import pygame

from board_manager import BoardManager
from game_logic import GameLogic
from input_handler import InputHandler
from ui import UI


pygame.init()


# Window size
WIDTH = 600
HEIGHT = 650


screen = pygame.display.set_mode(
    (WIDTH, HEIGHT)
)

pygame.display.set_caption(
    "Minesweeper"
)


ui = UI(screen)


inputHandler = InputHandler(
    ui.boardX,
    ui.boardY,
    ui.tileSize
)


mineCount = 10

game = None

screenState = "setup"


clock = pygame.time.Clock()

running = True


while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False


        # -------------------------
        # SETUP SCREEN
        # -------------------------

        if screenState == "setup":

            if event.type == pygame.MOUSEBUTTONDOWN:

                if ui.minusButton.collidepoint(event.pos):

                    if mineCount > 10:
                        mineCount -= 1


                elif ui.plusButton.collidepoint(event.pos):

                    if mineCount < 20:
                        mineCount += 1


                elif ui.startButton.collidepoint(event.pos):

                    board = BoardManager()

                    game = GameLogic(
                        board,
                        mineCount
                    )

                    screenState = "game"


        # -------------------------
        # GAME SCREEN
        # -------------------------

        elif screenState == "game":

            if event.type == pygame.MOUSEBUTTONDOWN:

                # Restart using same mine count
                if ui.restartButton.collidepoint(event.pos):

                    game.resetGame(
                        mineCount
                    )


                # Return to mine selection
                elif ui.newGameButton.collidepoint(event.pos):

                    screenState = "setup"


                else:

                    inputHandler.handleEvent(
                        event,
                        game
                    )


    # -------------------------
    # DRAW SCREEN
    # -------------------------

    if screenState == "setup":

        ui.drawSetup(
            mineCount
        )

    else:

        ui.drawGame(
            game
        )


    pygame.display.flip()

    clock.tick(60)


pygame.quit()