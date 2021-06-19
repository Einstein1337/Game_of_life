import os
import pygame
from PIL import Image, ImageDraw
import numpy as np
from random import randint

from pygame.constants import MOUSEBUTTONDOWN

## VARIABLES ##

WIN_WIDTH = 1000
WIN_HEIGHT = WIN_WIDTH

# Framerate
FPS = 10
TIME_DELAY = int(1000 / FPS)
update_per_second = 10

# Colors
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
BG_COLOR = GRAY
# other
squares = 10
side_lengh = WIN_WIDTH/squares

## METHODS #
    
def drawMatrix(matrix, surface):
    for y in range(len(matrix)):
        for x in range(len(matrix[y])):
            if matrix[y][x] == 0:
                color = WHITE
            else:
                color = BLACK
                

            pygame.draw.rect(surface, color, pygame.Rect(
                x*side_lengh + 1, y*side_lengh + 1, side_lengh - 2, side_lengh - 2))

def updateMatrix(matrix): 
    update_matrix = []  
    for i in range(squares):
            update_matrix.append([])
            for j in range(squares):
                update_matrix[i].append(0)

    for y in range(len(matrix)):
        for x in range(len(matrix[y])):
            if matrix[y][x] == 1:
                #rule 1: Live cell dies, if fewer than 2 Neighbours, underpopulation
                pass
            else:
                pass

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
        self.game_play = False

    def play(self):
        matrix = []
        for i in range(squares):
            matrix.append([])
            for j in range(squares):
                matrix[i].append(0)
        while True:
            #key events
            for event in pygame.event.get():
                # Exit app if click quit button
                if event.type == pygame.QUIT:
                    run = False
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1: #Leftclick
                        (x, y) = pygame.mouse.get_pos()
                        if matrix[int(y/side_lengh)][int(x/side_lengh)] == 0:
                            matrix[int(y/side_lengh)][int(x/side_lengh)] = 1
                        else:
                            matrix[int(y/side_lengh)][int(x/side_lengh)] = 0
                    

            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                self.exit()
            if keys[pygame.K_s]:
                self.game_play = not self.game_play
            
            #update Matrix
            if self.game_play:
                matrix = updateMatrix(matrix)
            #draw
            self.screen.fill(BG_COLOR)  # draw empty screen

            drawMatrix(matrix, self.screen)

            # Update
            pygame.time.delay(TIME_DELAY)
            pygame.display.flip()
            pygame.display.update()
        pygame.quit()


if __name__ == "__main__":
    Game().play()
