import os
import pygame
from PIL import Image, ImageDraw
import numpy as np
from random import randint
from pygame import mouse
from pygame import fastevent

from pygame.constants import KEYDOWN, MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION

## VARIABLES ##
extra_space = 110
WIN_WIDTH = 1000
WIN_HEIGHT = 500 + extra_space

# Framerate
FPS = 60

# Colors
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
RED = (255, 0, 0)  # 255, 139, 139
GREEN = (46, 255, 0)  # 183, 255, 175
BLACK = (0, 0, 0)
BG_COLOR = GRAY
# other
squares_x = 100
side_lengh = WIN_WIDTH/squares_x
squares_y = int((WIN_HEIGHT-extra_space)/side_lengh)
if WIN_HEIGHT/side_lengh - squares_y > 0:
    WIN_HEIGHT = int(squares_y*side_lengh) + extra_space
text_size1 = 24
text_size2 = 18
# keys
delete_down = False
backspace_down = False
s_down = False
space_down = False
## METHODS #


def drawExtraSpace(surface, color, font1, font2, fps):
    pygame.draw.rect(surface, WHITE, pygame.Rect(
        0, 0, WIN_WIDTH, extra_space-1))
    pygame.draw.circle(surface, color, (WIN_WIDTH/2,
                                        (extra_space-1)/2), (extra_space/2) * 0.6)
    img = [font1.render(f'FPS: {fps}', True, BLACK),
           font2.render(
               'place / delete cells:            left mouse click', True, BLACK),
           font2.render(
               'start / stop generation:     s / space', True, BLACK),
           font2.render(
               'clear grid:                             delete / backspace', True, BLACK),
           font2.render(
               'toggle FPS:                           up / down arrow', True, BLACK),
           font2.render('generate random grid:       r', True, BLACK),
           font2.render('quit game:                             esc', True, BLACK)]
    surface.blit(img[0], (WIN_WIDTH-70, extra_space - text_size1))
    for i in range(len(img)-1):
        surface.blit(img[i+1], (1, 1+i*text_size2))


def drawMatrix(matrix, surface):
    for y in range(squares_y):
        for x in range(squares_x):
            if matrix[y][x] == 0:
                color = WHITE
            else:
                color = BLACK

            pygame.draw.rect(surface, color, pygame.Rect(
                x*side_lengh + 1, y*side_lengh + extra_space + 1, side_lengh - 2, side_lengh - 2))


def updateMatrix(matrix):
    sx = squares_x - 1
    sy = squares_y - 1
    neighbours = 0
    update_matrix = []
    for i in range(squares_y):
        update_matrix.append([])
        for j in range(squares_x):
            update_matrix[i].append(0)

    for y in range(squares_y):
        for x in range(squares_x):
            # detecting neighbours
            if x == 0:  # checking corners/edges
                if y == 0:
                    neighbours += matrix[0][1] + matrix[1][0] + matrix[1][1] + matrix[sy][0] + \
                        matrix[sy][1] + matrix[0][sx] + \
                        matrix[1][sx] + matrix[sy][sx]
                elif y == sy:
                    neighbours += matrix[y][1] + matrix[y-1][0] + matrix[y-1][1] + matrix[0][0] + \
                        matrix[0][1] + matrix[sy][sx] + \
                        matrix[sy-1][sx] + matrix[0][sx]
                else:
                    neighbours += matrix[y-1][0] + matrix[y+1][0] + matrix[y-1][1] + matrix[y][1] + \
                        matrix[y+1][1] + matrix[y-1][sx] + \
                        matrix[y][sx] + matrix[y+1][sx]

            elif x == sx:
                if y == 0:
                    neighbours += matrix[0][x-1] + matrix[1][x] + matrix[1][x-1] + \
                        matrix[sy][sx] + matrix[sy][sx-1] + \
                        matrix[0][0] + matrix[1][0] + matrix[sy][0]
                elif y == sy:
                    neighbours += matrix[y][x-1] + matrix[y-1][x] + matrix[y-1][x-1] + \
                        matrix[sy][0] + matrix[sy-1][0] + \
                        matrix[0][sx] + matrix[0][sx-1] + matrix[0][0]
                else:
                    neighbours += matrix[y-1][sx] + matrix[y+1][sx] + matrix[y-1][sx-1] + \
                        matrix[y][sx-1] + matrix[y+1][sx-1] + \
                        matrix[y-1][0] + matrix[y][0] + matrix[y+1][0]

            elif y == 0:
                neighbours += matrix[0][x-1] + matrix[0][x+1] + matrix[1][x-1] + matrix[1][x] + \
                    matrix[1][x+1] + matrix[sy][x-1] + \
                    matrix[sy][x] + matrix[sy][x+1]
            elif y == sy:
                neighbours += matrix[sy][x-1] + matrix[sy][x+1] + matrix[sy-1][x-1] + matrix[sy -
                                                                                             1][x] + matrix[sy-1][x+1] + matrix[0][x-1] + matrix[0][x] + matrix[0][x+1]

            else:  # checking all others
                neighbours += matrix[y-1][x] + matrix[y+1][x] + matrix[y][x-1] + matrix[y][x+1] + \
                    matrix[y+1][x+1] + matrix[y-1][x-1] + \
                    matrix[y+1][x-1] + matrix[y-1][x+1]

            # Rule 1: Life cell with 2 or 3 neighbours, survives
            # Rule 2: Dead cell with ecatly 3 neighbours, becomes lifing cell
            # Rule 3: All other cells die, stay dead

            if matrix[y][x] == 1:
                if neighbours == 2 or neighbours == 3:
                    update_matrix[y][x] = 1
                else:
                    update_matrix[y][x] = 0

            else:
                if neighbours == 3:
                    update_matrix[y][x] = 1

            neighbours = 0

    return update_matrix


class Game:
    """
    Main GAME class
    """

    def __init__(self):
        pygame.init()
        pygame.font.init()
        print(WIN_HEIGHT)
        print(WIN_WIDTH)
        self.screen = pygame.display.set_mode(
            (WIN_WIDTH, WIN_HEIGHT)
        )  # create screen which will display everything
        self.win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        pygame.display.set_caption("Game of life")  # Game title
        self.game_play = False

    def play(self):
        mouse_pressed = False
        draw = False
        erase = False
        self.fps = FPS
        font1 = pygame.font.SysFont('Arial.ttf', text_size1)
        font2 = pygame.font.SysFont('Arial.ttf', text_size2)
        matrix = []
        for i in range(squares_y):
            matrix.append([])
            for j in range(squares_x):
                matrix[i].append(0)
        frame = 0
        fps_update = False
        while True:
            # key events
            for event in pygame.event.get():
                # Exit app if click quit button
                if event.type == pygame.QUIT:
                    run = False
                if event.type == MOUSEBUTTONDOWN:
                    mouse_pressed = True
                    if event.button == 1:  # Leftclick
                        (x, y) = pygame.mouse.get_pos()
                        if y > extra_space:
                            y -= extra_space
                            if matrix[int((y/side_lengh))][int(x/side_lengh)] == 0:
                                draw = True
                                matrix[int((y/side_lengh))
                                       ][int(x/side_lengh)] = 1
                            else:
                                erase = True
                                matrix[int((y/side_lengh))
                                       ][int(x/side_lengh)] = 0

                if event.type == MOUSEBUTTONUP:
                    mouse_pressed = False
                    draw = False
                    erase = False

                if event.type == MOUSEMOTION:
                    if mouse_pressed:
                        (x, y) = pygame.mouse.get_pos()
                        if y > extra_space:
                            y -= extra_space
                            if draw:
                                if matrix[int((y/side_lengh))][int(x/side_lengh)] == 0:
                                    matrix[int((y/side_lengh))
                                           ][int(x/side_lengh)] = 1
                            if erase:
                                if matrix[int((y/side_lengh))][int(x/side_lengh)] == 1:
                                    matrix[int((y/side_lengh))
                                           ][int(x/side_lengh)] = 0

                if event.type == KEYDOWN:
                    if event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                        matrix = []
                        for i in range(squares_y):
                            matrix.append([])
                            for j in range(squares_x):
                                matrix[i].append(0)

                    if event.key == pygame.K_s or event.key == pygame.K_SPACE:
                        self.game_play = not self.game_play
                        if self.game_play:
                            if self.fps == 60:
                                self.fps = 10
                        else:
                            if self.fps < 60:
                                self.fps = 60

                    if event.key == pygame.K_r:
                        matrix = []
                        for i in range(squares_y):
                            matrix.append([])
                            for j in range(squares_x):
                                matrix[i].append(randint(0, 1))

            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                self.exit()

            if keys[pygame.K_DOWN]:
                fps_update = True
                if self.fps > 1:
                    frame = 0
                    self.fps -= 1

            if keys[pygame.K_UP]:
                fps_update = True
                if self.fps < 120:
                    frame = 0
                    self.fps += 1

            # update Matrix
            if self.game_play:
                running_button_color = GREEN
                if fps_update:
                    matrix = updateMatrix(matrix)
                else:
                    frame += 3
                    if frame >= int(1000/self.fps):
                        matrix = updateMatrix(matrix)
                        frame = 0

            else:
                running_button_color = RED

            # draw
            self.screen.fill(BG_COLOR)  # draw empty screen
            drawExtraSpace(self.screen, running_button_color,
                           font1, font2, self.fps)
            drawMatrix(matrix, self.screen)

            # Update
            if fps_update:
                pygame.time.delay(int(1000/self.fps))
                fps_update = False
            pygame.display.flip()
            pygame.display.update()
        pygame.quit()


if __name__ == "__main__":
    Game().play()
