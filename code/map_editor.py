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
    new_tile.image.blit(tile_map.tile_set, (0, 0), tile.area)
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


## Toggle buttons ##
x_cell = 34
y_cell = 0
b_cell = (x_cell * set_size[0], y_cell)
b_grid = Button(pos=b_cell)
b_grid.toggled = True
b_grid.name = 'Grid'
b_grid.image.blit(grid_text.image, grid_text.rect)

x_cell = 38
b_cell = (x_cell * set_size[0], y_cell)
b_clear = Button(pos=b_cell)
b_clear.name = 'Clear'
b_clear.image.blit(clear_text.image, clear_text.rect)

toggle_buttons = [b_grid, b_clear]


## Select buttons ##
x_cell = 32
b_cell = (x_cell * set_size[0], y_cell)
b_eraser = Button(pos=b_cell)
b_eraser.name = 'Eraser'
b_eraser.image.blit(eraser_text.image, eraser_text.rect)

select_buttons = [b_eraser] + craft_buttons(tiles)


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


    if mouse.cell_clicked and not mouse.tile:

        ## Check if toggle button was clicked ##
        done = False

        for button in toggle_buttons_group.sprites():

            button_cell = cell_pos(button.pos)

            if mouse.cell_clicked == button_cell:

                if button.toggled:
                    button.toggled = False
                else:
                    button.toggled = True

                mouse.cell_clicked = None
                done = True

                break

        ## Check if select button was clicked ##
        if not done:

            for button in select_buttons_group.sprites():

                button_cell = cell_pos(button.pos)

                if mouse.cell_clicked == button_cell:
                    '''
                    col, row = cell_clicked
                    area_pos = (col * set_size[0], row * set_size[1])
                    area = pygame.Rect(*area_pos, *set_size)
                    '''
                    tile = Tile()
                    tile.image.blit(button.image, (0, 0))
                    tile.image = tile.image.convert_alpha()
                    tile.pos = mouse.cell_clicked

                    mouse.tile = tile
                    mouse.cell_clicked = None

                    break

    elif mouse.cell_clicked and mouse.tile:

        ## Do not place mouse.tile on an existing button.cell ##
        if mouse.cell_clicked in button_cells:

            mouse.cell_clicked = None

        ## Place mouse.tile on mouse.cell_clicked ##
        elif mouse.cell_clicked not in [map_tile.pos for map_tile in map_tiles]:

            pix_pos = pixel_pos(mouse.cell_clicked)
            new_tile = Tile()
            new_tile.image.blit(mouse.tile.image, (0, 0))
            new_tile.rect = new_tile.image.get_rect()
            new_tile.rect.topleft = (0, 0)
            new_tile.rect = new_tile.rect.move(pix_pos)
            map_tiles.add(new_tile)
            mouse.cell_clicked = None


    ## Cancel mouse action on right click ##
    if mouse.right_down:

        mouse.reset()


    ## Check clear_screen button ##
    if b_clear.toggled:

        map_tiles.empty()
        b_clear.toggled = False


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


