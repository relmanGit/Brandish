import pygame
from constants import *
import tile_map as tm



## Preset some settings.
screen_size = (SCREEN_WIDTH*2, SCREEN_HEIGHT*2.1)
set_path = f'../assets/img/platform_new/'
set_size = (32, 32)

herotileset = 'hero_vert.png'
mytileset = 'tile_set.png'

which_set = herotileset



## Position conversion hellper functions.
def cell_pos(pixel_pos, cell_size=set_size):

    cell_width, cell_height = cell_size
    pix_x, pix_y = pixel_pos
    cell_x = (pix_x // cell_width)
    cell_y = (pix_y // cell_height)
    return (cell_x, cell_y)

def pixel_pos(cell_pos, cell_size=set_size):
    
    cell_width, cell_height = cell_size
    cell_x, cell_y = cell_pos
    pix_x = cell_x * cell_width
    pix_y = cell_y * cell_height
    return (pix_x, pix_y)



## Hellper classes.
class Grid:


    def __init__(self, cell_width=set_size[0], cell_height=set_size[1]):

        self.width = cell_width
        self.height = cell_height


    def draw(self, surface, cell_size=set_size):

        screen_width, screen_height = surface.get_size()
        cell_width, cell_height = cell_size

        cols = screen_width // cell_width
        for col in range(cols):
            start_pos = (col * set_size[0], 0)
            end_pos = (col * set_size[0], screen_height)
            pygame.draw.line(surface, BLACK, start_pos, end_pos)

        rows = screen_height // cell_height
        for row in range(rows):
            start_pos = (0, row * set_size[1])
            end_pos = (screen_width, row * set_size[1])
            pygame.draw.line(surface, BLACK, start_pos, end_pos)



class Tile(pygame.sprite.Sprite):


    def __init__(self, size=set_size, pos=(0, 0)):
        super().__init__()

        self.size = size
        self.pos = pos
        self.cell = cell_pos(self.pos)
        self.image = pygame.Surface(self.size)
        self.rect = pygame.Rect(*pos, *size)

        self.image.fill(TRANSPARENT)
        self.image.set_colorkey(TRANSPARENT)



class Button(pygame.sprite.Sprite):


    def __init__(self, size=set_size, pos=(0, 0)):
        super().__init__()

        self.size = size
        self.pos = pos
        self.cell = cell_pos(self.pos)
        self.image = pygame.Surface(self.size)
        self.rect = pygame.Rect(*pos, *size)
        self.toggled = False

        self.text_str = 'Default'
        self.name = 'Button'
        self.color = MY_RED
        self.image.fill(self.color)



class Mouse:


    def __init__(self):
        
        self.pos = (0, 0)
        self.cell = (0, 0)
        '''
        self.left_down = None
        self.right_down = None
        self.left_up = None
        self.right_up = None
        self.cell_clicked = None
        self.tile = None
        '''
        self.reset()


    def reset(self):

        self.left_down = None
        self.right_down = None
        self.left_up = None
        self.right_up = None
        self.cell_clicked = None
        self.tile = None

