import pygame
from constants import *
import tile_map as tm
from hellper import *
from typewriter import *



## Testing ##
pygame.init()
screen = pygame.display.set_mode(screen_size)
grid = Grid()
grid.toggled = True

background = pygame.Surface(screen.get_size())
background.fill(MY_BLUE)

set_path = set_path + which_set
tile_map = tm.Tile_map(set_path, set_size)
#tile_map.tile_set = tile_map.tile_set.convert_alpha()


## Convert tiles ##
tiles = []
for tile in tile_map.tiles:
    new_tile = Tile()
    new_tile.area = tile.area
    new_tile.image.blit(tile_map.tile_sheet, (0, 0), tile.area)
    new_tile.image = new_tile.image.convert_alpha()
    tiles.append(new_tile)
tile_map.tiles = tiles


## Typewriter and text rendering ##
tp = Typewriter()

tracker_x = 4
tracker_y = (screen_size[1] - set_size[1]) + 2
tracker_pos = (tracker_x, tracker_y)

tracker = Text(tp.write('(0, 0)'))
tracker.rect.topleft = tracker_pos

grid_text = Text(tp.write('G'))
grid_text.rect.topleft = (7, 4)

clear_text = Text(tp.write('C'))
clear_text.rect.topleft = (7, 4)

eraser_text = Text(tp.write('E'))
eraser_text.rect.topleft = (8, 4)

export_text = Text(tp.write('X'))
export_text.rect.topleft = (9, 4)


## Toggle buttons ##
x_cell = 32
y_cell = 0
b_pos = (x_cell * set_size[0], y_cell)
b_eraser = Button(pos=b_pos)
b_eraser.name = 'Eraser'
b_eraser.image.blit(eraser_text.image, eraser_text.rect)

x_cell = 33
b_pos = (x_cell * set_size[0], y_cell)
b_clear = Button(pos=b_pos)
b_clear.name = 'Clear'
b_clear.image.blit(clear_text.image, clear_text.rect)

x_cell = 35
b_pos = (x_cell * set_size[0], y_cell)
b_grid = Button(pos=b_pos)
b_grid.toggled = True
b_grid.name = 'Grid'
b_grid.image.blit(grid_text.image, grid_text.rect)

x_cell = 38
b_pos = (x_cell * set_size[0], y_cell)
b_export = Button(pos=b_pos)
b_export.name = 'Export'
b_export.image.blit(export_text.image, export_text.rect)


toggle_buttons = [b_eraser, b_clear, b_grid, b_export]


## Select buttons ##
select_buttons = craft_tile_buttons(tiles)


## All button cell positions ##
button_cells = [button.cell for button in toggle_buttons + select_buttons]


## Groups for toggle and select buttons ##
toggle_buttons_group = pygame.sprite.Group(toggle_buttons)
select_buttons_group = pygame.sprite.Group(select_buttons)


## Group of created map tiles ##
map_tiles = pygame.sprite.Group()


## Mouse ##
mouse = Mouse()



## Main Game Loop ##
running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False
            break

        ## Track mouse cell position ##
        if event.type == pygame.MOUSEMOTION:

            mouse.pos = event.pos
            mouse.cell = cell_pos(mouse.pos)
            text = tp.write(str(mouse.cell))
            tracker.rewrite(text)

        if event.type == pygame.MOUSEBUTTONDOWN:

            ## Left click pressed ##
            if event.button == 1:

                mouse.left_down = cell_pos(event.pos)
                mouse.cell_clicked = None

            ## Right click pressed ##
            elif event.button == 3:

                mouse.right_down = cell_pos(event.pos)
                mouse.cell_clicked = None

        if event.type == pygame.MOUSEBUTTONUP:

            ## Left click released ##
            if event.button == 1:

                mouse.left_up = cell_pos(event.pos)

                if mouse.left_up == mouse.left_down:

                    mouse.cell_clicked = mouse.cell

            ## Right click released ##
            if event.button == 3:
                pass


    ## Blit background and buttons ##
    screen.blit(background, (0, 0))
    toggle_buttons_group.draw(screen)
    select_buttons_group.draw(screen)


    ## Determine if cell_clicked is button or if should place tile ##
    buttons = toggle_buttons + select_buttons
    button_clicked = get_button_clicked(buttons, mouse)

    if button_clicked:# and not mouse.tile:

        ## Check if toggle button was clicked ##
        if button_clicked.type == 'toggle':

            button_clicked.toggled = button_clicked.toggled ^ True

            name = button_clicked.name

            if name == 'Eraser':
                print(name, '=', button_clicked.toggled)

            elif name == 'Clear':
                print(name)
                map_tiles.empty()

            elif name == 'Export':
                print(name)
                export_map(map_tiles.sprites())

        ## Check if select button was clicked ##
        elif button_clicked.type == 'select':

            tile = Tile()
            tile.image.blit(button_clicked.image, (0, 0))
            tile.image = tile.image.convert_alpha()
            tile.pos = mouse.cell_clicked
            tile.area = button_clicked.tile.area

            mouse.tile = tile
            mouse.cell_clicked = None

        mouse.cell_clicked = None

    ## If neither toggle nor select button was clicked ##
    elif mouse.cell_clicked:

        if mouse.tile or b_eraser.toggled:

            ## Determine if existing tile or if empty cell ##
            clicked_tile = None
            for tile in map_tiles:

                if mouse.cell_clicked == cell_pos(tile.rect.topleft):

                    clicked_tile = tile

            ## If cell has existing tile, remove it ##
            if clicked_tile:

                map_tiles.remove(clicked_tile)

            ## Place mouse.tile on empty(ied) cell ##
            if mouse.tile:

                pix_pos = pixel_pos(mouse.cell_clicked)
                new_tile = Tile()
                new_tile.image.blit(mouse.tile.image, (0, 0))
                new_tile.rect = new_tile.image.get_rect()
                new_tile.rect.topleft = pix_pos
                new_tile.cell = cell_pos(pix_pos)
                new_tile.area = mouse.tile.area
                map_tiles.add(new_tile)
        
        mouse.cell_clicked = None


    ## Cancel mouse action on right click ##
    if mouse.right_down:

        mouse.reset()
        b_eraser.toggled = False


    ## Draw map tiles ##
    map_tiles.draw(screen)


    ## Draw grid lines ##
    grid.toggled = b_grid.toggled

    if grid.toggled:

        grid.draw(screen)


    ## Draw selected tile at mouse location ##
    if mouse.tile:

        sub_x, sub_y = mouse.pos
        offset_x, offset_y = (set_size[0] // 2, set_size[1] // 2)
        sub_pos = (sub_x - offset_x, sub_y - offset_y)
        screen.blit(mouse.tile.image, sub_pos)


    ## Draw text (mouse.pos coordinates at screen.bottomleft)
    screen.blit(tracker.image, tracker.rect)
    pygame.display.flip()


pygame.quit()


