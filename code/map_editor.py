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



## Position manipulation hellper functions.
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
        self.rect = self.image.get_rect()

        self.image.fill(TRANSPARENT)
        self.image.set_colorkey(TRANSPARENT)



class Button(pygame.sprite.Sprite):


    def __init__(self, size=set_size, pos=(0, 0)):
        super().__init__()

        self.size = size
        self.pos = pos
        self.cell = cell_pos(self.pos)
        self.text_str = 'Default'
        self.image = pygame.Surface(self.size)
        self.rect = self.image.get_rect()

        self.name = 'Button'
        self.color = MY_RED
        self.image.fill(self.color)


## Testing
pygame.init()
screen = pygame.display.set_mode(screen_size)
grid = Grid()

background = pygame.Surface(screen.get_size())
background.fill(MY_BLUE)

set_path = set_path + which_set
tile_map = tm.Tile_map(set_path, set_size)
#tile_map.tile_set = tile_map.tile_set.convert_alpha()

## Convert tiles.
tiles = []
for tile in tile_map.tiles:
    new_tile = Tile()
    new_tile.image.blit(tile_map.tile_set, (0, 0), tile.area)
    new_tile.image = new_tile.image.convert_alpha()
    tiles.append(new_tile)
tile_map.tiles = tiles

## Create toggle buttons.
b_default = Button()
b_default.image.fill(MY_GREEN)
b_default.rect = b_default.image.get_rect()
b_default.pos = (18 * set_size[0], 0)
b_default.rect = b_default.rect.move(*b_default.pos)
b_default.name = 'default'

b_night = Button()
b_night.image.fill(BLUE)
b_night.rect = b_night.image.get_rect()
b_night.pos = (17 * set_size[0], 0)
b_night.rect = b_night.rect.move(*b_night.pos)
b_night.name = 'night'

b_hot = Button()
b_hot.image.fill(MY_RED)
b_hot.rect = b_hot.image.get_rect()
b_hot.pos = (16 * set_size[0], 0)
b_hot.rect = b_hot.rect.move(*b_hot.pos)
b_hot.name = 'hot'

toggle_buttons = [b_default, b_night, b_hot]

## Create select buttons.
select_buttons = []

sh_padding = 2  # selectable height padding
# cell_height of panel holding selectable buttons.
selectable_height = (screen_size[1] // set_size[1]) - sh_padding

# cell_width of panel holding selecable buttons.
selectable_width = 1 + (len(tiles) // selectable_height)
selectable_width = 6

row = 2
col_start = (screen_size[0] // set_size[0]) - selectable_width - 2
col = 0
for tile in tiles:
    button = Button()
    button.image = tile.image
    button.rect = button.image.get_rect()
    column = (col_start + col)
    button.pos = (column * set_size[0], row * set_size[1])
    button.rect = button.rect.move(*button.pos)
    select_buttons.append(button)
    col = col + 1
    if col > selectable_width:
        col = 0
        row = row + 1

## Groups for toggle and select buttons.
toggle_buttons_group = pygame.sprite.Group(toggle_buttons)
select_buttons_group = pygame.sprite.Group(select_buttons)

## Group of created map tiles.
map_tiles = pygame.sprite.Group()

## Text rendering.
font = pygame.font.SysFont('Arial', 16)
font_color = BLACK
text = font.render('(0, 0)', True, font_color)
text_rect = text.get_rect()
text_rect.bottomleft = (0, screen_size[1])




class Mouse:


    def __init__(self):
        
        self.pos = (0, 0)
        self.cell = (0, 0)
        self.left_down = None
        self.right_down = None
        self.left_up = None
        self.right_up = None
        self.cell_clicked = None
        self.tile = None


    def get_cell(self):

        pass


mouse = Mouse()


## Mouse control
mouse_pos = (0, 0)
mouse_cell = (0, 0)
mouse_down = None
mouse_up = None
cell_clicked = None
mouse_tile = None

## Main Game Loop
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

        if event.type == pygame.MOUSEMOTION:
            mouse_pos = event.pos
            mouse_cell = cell_pos(mouse_pos)

            text_str = str(mouse_cell)
            text = font.render(text_str, True, font_color)
            text_rect.bottomleft = (0, screen_size[1])
            '''
            mouse.pos = event.pos
            mouse.cell = cell_pos(mouse.cell)

            text_str = str(mouse_cell)
            text = font.render(text_str, True, font_color)
            text_rect.bottomleft = (0, screen_size[1])
            '''
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_down = cell_pos(event.pos)
            cell_clicked = None
            '''
            mouse.left_down = cell_pos(event.pos)
            mouse.cell_clicked = None
            '''
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_up = cell_pos(event.pos)
            if mouse_up == mouse_down:
                cell_clicked = mouse_cell
            '''
            mouse.left_up = cell_pos(event.pos)
            if mouse.left_up == mouse.right_up:
                mouse.cell_clicked = mouse.cell
            '''
    ## Blit background and buttons.
    screen.blit(background, (0, 0))
    toggle_buttons_group.draw(screen)
    select_buttons_group.draw(screen)

    if cell_clicked and not mouse_tile:

        ## Check if toggle button was clicked.
        done = False
        for button in toggle_buttons_group.sprites():
            button_cell = cell_pos(button.pos)

            if mouse.cell_clicked == button_cell:
                mouse.cell_clicked = None
                done = True
                break

        ## Check if select button was clicked.
        if not done:
            for button in select_buttons_group.sprites():
                button_cell = cell_pos(button.pos)

                if cell_clicked == button_cell:
                    '''
                    col, row = cell_clicked
                    area_pos = (col * set_size[0], row * set_size[1])
                    area = pygame.Rect(*area_pos, *set_size)
                    '''
                    tile = Tile()
                    tile.image.blit(button.image, (0, 0))
                    tile.image = tile.image.convert_alpha()
                    tile.pos = cell_clicked
                    mouse_tile = tile
                    cell_clicked = None
                    break
                '''
                if mouse.cell_clikced == button_cell:
                    tile = Tile()
                    tile.image.blit(button.image, (0, 0))
                    tile.image = tile.image.convert_alpha()
                    tile.pos = mouse.cell_clicked
                    mouse.tile = tile
                    mouse.cell_clicked = None
                    break
                '''
    elif cell_clicked and mouse_tile:
        
        temp = [map_tile.pos for map_tile in map_tiles]
        
        ## Place mouse_tile on cell_clicked.
        if cell_clicked not in [map_tile.pos for map_tile in map_tiles]:
            mouse_tile.rect = mouse_tile.rect.move(pixel_pos(cell_clicked))
            map_tiles.add(mouse_tile)

        mouse_tile = None
    
    ## Draw map tiles.
    map_tiles.draw(screen)

    ## Draw grid lines.
    grid.draw(screen)

    ## Draw selected tile at mouse location.
    if mouse_tile:
        sub_x, sub_y = mouse_pos
        offset_x, offset_y = (set_size[0] // 2, set_size[1] // 2)
        sub_pos = (sub_x - offset_x, sub_y - offset_y)
        screen.blit(mouse_tile.image, sub_pos)

    ## Draw text (mouse.pos at screen.bottomleft)
    screen.blit(text, text_rect)
    pygame.display.flip()

pygame.quit()


