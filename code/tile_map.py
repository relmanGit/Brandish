import os
import random
import pygame
from constants import *



class Tile:


    def __init__(self, size=(8, 8)):

        self.area = pygame.Rect(0, 0, *size)
        self.pos = (0, 0)



class Tile_map:


    def __init__(self, path, tile_size=(8, 8)):

        self.tile_set = pygame.image.load(path)
        if tile_size != (8, 8):
            width = tile_size[0] * (self.tile_set.get_width() // 8)
            height = tile_size[1] * (self.tile_set.get_height() // 8)
            new_size = (width, height)
            self.tile_set = pygame.transform.scale(self.tile_set, new_size)
        self.tile_size = tile_size
        self.tiles = []
        self.__make_map()


    def __make_map(self):

        sheet_width = self.tile_set.get_width()
        sheet_height = self.tile_set.get_height()

        tile_width = self.tile_size[0]
        tile_height = self.tile_size[1]

        cols = sheet_width // tile_width
        rows = sheet_height // tile_height

        for row in range(rows):
            y = tile_height * row

            for col in range(cols):

                x = tile_width * col
                pos = (x, y)

                tile = Tile(self.tile_size)
                tile.area.topleft = pos
                tile.pos = (col * tile_width, row * tile_height)

                self.tiles.append(tile)


'''
## Testing
pygame.init()
screen_size = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(screen_size)

which_set = 'hero.png'
set_path = f'../assets/img/platform_new/' + which_set
set_size = (32, 32)
tm = Tile_map(set_path, set_size)

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
    
    screen.fill(MY_BLUE)
    for tile in tm.tiles:
        screen.blit(tm.tile_set, tile.pos, tile.area)
    pygame.display.flip()

pygame.quit()
'''

