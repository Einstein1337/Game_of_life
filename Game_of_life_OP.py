import os
from numpy.core.fromnumeric import _resize_dispatcher
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

# Cell Class


class Cell:
    def __init__(self, xy):
        self.xy = xy

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
           font2.render('quit game:                             esc', True, BLACK)]
    surface.blit(img[0], (WIN_WIDTH-70, extra_space - text_size1))
    for i in range(len(img)-1):
        surface.blit(img[i+1], (1, 1+i*text_size2))


def drawGrid(lc, surface):
    for y in range(squares_y):
        for x in range(squares_x):
            pygame.draw.rect(surface, WHITE, pygame.Rect(
                x*side_lengh + 1, y*side_lengh + extra_space + 1, side_lengh - 2, side_lengh - 2))

    for i in range(len(lc)):
        if lc[i].xy[0]*side_lengh >= 0 and lc[i].xy[0]*side_lengh <= WIN_WIDTH and lc[i].xy[1]*side_lengh >= 0 and lc[i].xy[1]*side_lengh <= WIN_HEIGHT:
            pygame.draw.rect(surface, BLACK, pygame.Rect(
                lc[i].xy[0]*side_lengh + 1, lc[i].xy[1]*side_lengh + extra_space + 1, side_lengh - 2, side_lengh - 2))


def checkIfCellAlife(lc, xy):
    living = False
    position_in_list = 0
    if len(lc) > 0:
        for i in range(len(lc)):
            if lc[i].xy == xy:
                position_in_list = i
                living = True
    return [living, position_in_list]


def updateCells(lc):
    # sx = squares_x - 1
    # sy = squares_y - 1
    neighbours = 0
    updated_living_cells = []
    neighbour_coordinates = []
    dead_cells_arround_living_cells = []
    for i in range(len(lc)):
        x = lc[i].xy[0]
        y = lc[i].xy[1]
        for j in range(len(lc)):  # checking living neighbours
            if lc[j].xy != [x, y]:
                if np.abs(lc[j].xy[0] - x) <= 1 and np.abs(lc[j].xy[1] - y) <= 1:
                    neighbours += 1
                    neighbour_coordinates.append(lc[j].xy)

        dead_cells_arround_living_cells.append([Cell([x, y+1]), Cell([x, y-1]), Cell([x+1, y]), Cell( #creates List with all neighbours
            [x-1, y]), Cell([x+1, y+1]), Cell([x+1, y-1]), Cell([x-1, y+1]), Cell([x-1, y-1])])

        deleted_cells = 0 
        for k in range(neighbours): #deletes all living neighbours from list
            for f in range(len(dead_cells_arround_living_cells[i])):
                if neighbour_coordinates[k] == dead_cells_arround_living_cells[i][f - deleted_cells].xy:
                    del dead_cells_arround_living_cells[i][f - deleted_cells]
                    deleted_cells += 1
                    f += deleted_cells
            deleted_cells = 0
        # Rule 1: Life cell with 2 or 3 neighbours, survives
        # Rule 2: Dead cell with ecatly 3 neighbours, becomes lifing cell
        # Rule 3: All other cells die, stay dead

        if neighbours == 2 or neighbours == 3: #if ¨to little or to many neighbours die, else life
            updated_living_cells.append(Cell(lc[i].xy))

        neighbour_coordinates = []
        neighbours = 0


    deleted_cells = 0 #deletes all duplicated dead neighbours to get list with all dead neighbours arround living cells
    for r in range(len(dead_cells_arround_living_cells)):
        for c in range(len(dead_cells_arround_living_cells[r])):
            for r2 in range(len(dead_cells_arround_living_cells)):
                x1 = dead_cells_arround_living_cells[r][c].xy[0]
                y1 = dead_cells_arround_living_cells[r][c].xy[1]
                x2 = dead_cells_arround_living_cells[r][0].xy[0]
                y2 = dead_cells_arround_living_cells[r][0].xy[1] - 1
                if r != r2 and x1 - x2 > -3 and x1 - x2 < 3 and y1 - y2 > -3 and y1 - y2 < 3:
                    for c2 in range(len(dead_cells_arround_living_cells[r2])):
                        if dead_cells_arround_living_cells[r][c].xy == dead_cells_arround_living_cells[r2][c2 - deleted_cells].xy:
                            del dead_cells_arround_living_cells[r2][c2 - deleted_cells]
                            deleted_cells += 1
                            c2 += deleted_cells
                    deleted_cells = 0

    d_cell_l_neighbours = 0 #checking living neighbours from dead cell
    for row in range(len(dead_cells_arround_living_cells)):
        for column in range(len(dead_cells_arround_living_cells[row])):
            x = dead_cells_arround_living_cells[row][column].xy[0]
            y = dead_cells_arround_living_cells[row][column].xy[1]
            for cell in range(len(lc)):  
                if np.abs(lc[cell].xy[0] - x) <= 1 and np.abs(lc[cell].xy[1] - y) <= 1:
                    d_cell_l_neighbours += 1

            if d_cell_l_neighbours == 3: #if exactly 3 living neighbours => come alive
                updated_living_cells.append(Cell(dead_cells_arround_living_cells[row][column].xy))

            d_cell_l_neighbours = 0

    return updated_living_cells


class Game:
    """
    Main GAME class
    """

    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode(
            (WIN_WIDTH, WIN_HEIGHT)
        )  # create screen which will display everything
        self.win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        pygame.display.set_caption("Game of life")  # Game title
        self.game_play = False
        self.living_cells = []

    def play(self):
        mouse_pressed = False
        draw = False
        erase = False
        self.fps = FPS
        font1 = pygame.font.SysFont('Arial.ttf', text_size1)
        font2 = pygame.font.SysFont('Arial.ttf', text_size2)
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
                            check = checkIfCellAlife(
                                self.living_cells, [int(x/side_lengh), int(y/side_lengh)])
                            if check[0] == False:
                                draw = True
                                self.living_cells.append(
                                    Cell([int(x/side_lengh), int(y/side_lengh)]))

                            elif check[0]:
                                erase = True
                                del self.living_cells[check[1]]

                if event.type == MOUSEBUTTONUP:
                    mouse_pressed = False
                    draw = False
                    erase = False

                if event.type == MOUSEMOTION:
                    if mouse_pressed:
                        (x, y) = pygame.mouse.get_pos()
                        if y > extra_space:
                            y -= extra_space
                            check = checkIfCellAlife(
                                self.living_cells, [int(x/side_lengh), int(y/side_lengh)])
                            if draw:
                                if check[0] == False:
                                    self.living_cells.append(
                                        Cell([int(x/side_lengh), int(y/side_lengh)]))
                            elif erase:
                                if check[0]:
                                    del self.living_cells[check[1]]

                if event.type == KEYDOWN:
                    if event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                        self.living_cells = []

                    if event.key == pygame.K_s or event.key == pygame.K_SPACE:
                        self.game_play = not self.game_play
                        if self.game_play:
                            if self.fps == 60:
                                self.fps = 10
                        else:
                            if self.fps < 60:
                                self.fps = 60


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
                    self.living_cells = updateCells(self.living_cells)
                else:
                    frame += 3
                    if frame >= int(1000/self.fps):
                        self.living_cells = updateCells(self.living_cells)
                        frame = 0

            else:
                running_button_color = RED

            # draw
            self.screen.fill(BG_COLOR)  # draw empty screen
            drawExtraSpace(self.screen, running_button_color,
                           font1, font2, self.fps)
            drawGrid(self.living_cells, self.screen)

            # Update
            if fps_update:
                pygame.time.delay(int(1000/self.fps))
                fps_update = False
            pygame.display.flip()
            pygame.display.update()
        pygame.quit()


if __name__ == "__main__":
    Game().play()
