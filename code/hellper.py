import pygame
from constants import *
import tile_map as tm



## Preset some settings.
screen_size = (SCREEN_WIDTH*2, SCREEN_HEIGHT*2.1)
set_path = f'../assets/img/map_sheet/'
set_size = (32, 32)

herotileset = 'hero.png'

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


def get_button_clicked(buttons, mouse):

    if mouse.cell_clicked:

        for button in buttons:

            button_cell = cell_pos(button.pos)

            if mouse.cell_clicked == button_cell:

                return button

    return None


def export_map(tiles):

    temp = sorted(tiles, key=lambda tile : cell_pos(tile.rect.topleft)[0])
    temp.sort(key=lambda tile : cell_pos(tile.rect.topleft)[1])

    f = open('../maps/map.txt', 'w')
    f.write('Cell : Sheet_pos\n')

    for tile in temp:

        cell = str(tile.cell)
        area = str(tile.area.topleft)
        
        line = f'{cell} : {area}\n'
        f.write(line)

    f.close()


## Panel version ##
def craft_buttons(tiles, size):

    buttons = []

    width, height = size
    cell_width, cell_height = (width // set_size[0], height // set_size[1])

    col = 0
    row = 0

    for tile in tiles:

        button = Button()
        button.tile = tile
        button.image = tile.image
        button.rect = button.image.get_rect()

        button.cell = (col, row)
        button.pos = (col * set_size[0], row * set_size[1])
        button.rect.topleft = button.pos

        button.type = 'select'

        col = col + 1
        if col >= cell_width:
            col = 0
            row = row + 1

        buttons.append(button)

    return buttons


def craft_tile_buttons(tiles):

    buttons = []

    ## Should be replaced with panel ##
    sh_padding = 2  # selectable height padding
    # cell_height of panel holding selectable buttons.
    selectable_height = (screen_size[1] // set_size[1]) - sh_padding

    # cell_width of panel holding selecable buttons.
    selectable_width = 1 + (len(tiles) // selectable_height)
    selectable_width = 6
    ## End ##

    row = 2
    col_start = (screen_size[0] // set_size[0]) - selectable_width - 2
    col = 0

    for tile in tiles:

        button = Button()
        button.tile = tile
        button.image = tile.image
        button.rect = button.image.get_rect()

        column = (col_start + col)
        button.cell = (column, row)
        button.pos = (column * set_size[0], row * set_size[1])
        button.rect.topleft = button.pos

        button.type = 'select'

        buttons.append(button)

        col = col + 1
        if col > selectable_width:
            col = 0
            row = row + 1

    return buttons



## Hellper classes.
class Grid:


    def __init__(self, cell_width=set_size[0], cell_height=set_size[1]):

        self.width = cell_width
        self.height = cell_height
        self.toggled = False


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

        self.area = None
        self.image = pygame.Surface(size)
        self.rect = pygame.Rect(*pos, *size)
        self.cell = cell_pos(pos)

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
        self.type = 'toggle'
        self.toggled = False

        self.text = None
        self.name = 'Button'
        self.color = WHITE
        self.image.fill(self.color)

        self.tile = None



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


