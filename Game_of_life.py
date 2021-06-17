import os
import pygame
from PIL import Image, ImageDraw
import numpy as np
from random import randint

## VARIABLES ##

WIN_WIDTH = 500
WIN_HEIGHT = WIN_WIDTH

# Framerate
FPS = 30
TIME_DELAY = int(1000 / FPS)
update_per_second = 10

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BG_COLOR = WHITE

# other
squares = 50
side_lengh = WIN_WIDTH/squares

## METHODS #


def drawMatrix(matrix, surface):
    for y in range(len(matrix)):
        for x in range(len(matrix[y])):
            if matrix[y][x] == 0:
                color = WHITE
            elif matrix[y][x] == 1:
                color = BLACK

            pygame.draw.rect(surface, color, pygame.Rect(
                x*side_lengh, y*side_lengh, side_lengh, side_lengh))
            pygame.display.flip()


class Game:
    """
    Main GAME class
    """

    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.time_delay = TIME_DELAY
        self.screen = pygame.display.set_mode(
            (WIN_WIDTH, WIN_HEIGHT)
        )  # create screen which will display everything
        self.win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        pygame.display.set_caption("Simulation")  # Game title

    def play(self):
        test_matrix = []
        for i in range(squares):
            test_matrix.append([])
            for j in range(squares):
                test_matrix[i].append(randint(0, 1))

        while True:
            pygame.time.delay(TIME_DELAY)
            for event in pygame.event.get():
                # Exit app if click quit button
                if event.type == pygame.QUIT:
                    run = False
            keys = pygame.key.get_pressed()

            if keys[pygame.K_ESCAPE]:
                self.exit()

            self.screen.fill(BG_COLOR)  # draw empty screen
            drawMatrix(test_matrix, self.screen)
            test_matrix = []
            for i in range(squares):
                test_matrix.append([])
                for j in range(squares):
                    test_matrix[i].append(randint(0, 1))

            # Update
            pygame.display.update()
        pygame.quit()


if __name__ == "__main__":
    Game().play()
