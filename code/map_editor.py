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



## prompt class ##
class Prompt:


    ## prompt window size ##
    width = 6 * set_size[0]
    height = 3 * set_size[1]


    def __init__(self, size=(width, height), pos=(0, 0)):

        self.size = size
        self.pos = pos
        self.image = pygame.Surface(size)
        self.rect = pygame.Rect(*pos, *size)

        self.yes_button = None
        self.__make_yes_button()

        self.no_button = None
        self.__make_no_button()

        self.image.fill(WHITE)
        self.image.blit(self.yes_button.image, self.yes_button.rect)
        self.image.blit(self.no_button.image, self.no_button.rect)


    def __make_yes_button(self):

        width_t = 2
        w = width_t * set_size[0]
        h = set_size[1]
        y = int(set_size[1] * (3 / 2))

        text = Text(tp.write('Yes'))
        text.rect.topleft = (12, 4)

        size = (w, h)
        x = int(set_size[0] * (1 / 2))
        pos = (x, y)
        
        b = Button(size, pos)
        b.image.fill(MY_GREEN)
        b.image.blit(text.image, text.rect)
        
        self.yes_button = b


    def __make_no_button(self):

        width_t = 2
        w = width_t * set_size[0]
        h = set_size[1]
        y = int(set_size[1] * (3 / 2))

        text = Text(tp.write('No'))
        text.rect.topleft = (16, 4)

        size = (w, h)
        x = int(set_size[0] * (7 / 2))
        pos = (x, y)
        
        b = Button(size, pos)
        b.image.fill(MY_RED)
        b.image.blit(text.image, text.rect)

        self.no_button = b



## Build yes/no prompt window ##
prompt_text = Text(tp.write('Are you sure?'))
prompt_text.rect.topleft = (24, 8)

prompt_x = 25
prompt_y = 0
prompt_pos = (prompt_x * set_size[0], prompt_y * set_size[1])
prompt = Prompt(pos=prompt_pos)
prompt.image.blit(prompt_text.image, prompt_text.rect)


## Toggle buttons ##
x_cell = 32
y_cell = 0
b_pos = (x_cell * set_size[0], y_cell)
b_eraser = Button(pos=b_pos)
b_eraser.image.fill(ERASER_PINK)
b_eraser.name = 'Eraser'
b_eraser.image.blit(eraser_text.image, eraser_text.rect)

x_cell = 34
b_pos = (x_cell * set_size[0], y_cell)
b_clear = Button(pos=b_pos)
b_clear.image.fill(RED)
b_clear.name = 'Clear'
b_clear.image.blit(clear_text.image, clear_text.rect)

x_cell = 36
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
select_buttons = craft_tile_buttons(tile_map.tiles)


## All button cell positions ##
button_cells = [button.cell for button in toggle_buttons + select_buttons]


## Groups for toggle and select buttons ##
toggle_buttons_group = pygame.sprite.Group(toggle_buttons)
select_buttons_group = pygame.sprite.Group(select_buttons)


## Group of created map tiles ##
map_tiles = pygame.sprite.Group()


## Mouse ##
mouse = Mouse()


## Snapshot ##
snapshot = pygame.Surface(screen_size)



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

            ## prompt to verify clear ##
            elif name == 'Clear':
                print(name)

                answer = -1
                while answer < 0:

                    screen.blit(snapshot, (0, 0))
                    screen.blit(prompt.image, prompt.rect)
                    pygame.display.flip()

                    for event in pygame.event.get():

                        if event.type == pygame.MOUSEBUTTONDOWN:

                            mouse.pos = event.pos

                            ## yes button ##
                            b_temp = prompt.yes_button

                            b_yes_x = prompt.pos[0] + b_temp.pos[0]
                            b_yes_y = prompt.pos[1] + b_temp.pos[1]
                            b_yes_pos = (b_yes_x, b_yes_y)

                            b_yes_w = b_temp.size[0]
                            b_yes_h = b_temp.size[1]

                            ## no button ##
                            b_temp = prompt.no_button

                            b_no_x = prompt.pos[0] + b_temp.pos[0]
                            b_no_y = prompt.pos[1] + b_temp.pos[1]
                            b_no_pos = (b_no_x, b_no_y)

                            b_no_w = b_temp.size[0]
                            b_no_h = b_temp.size[1]

                            ## something here ##
                            if b_yes_x < mouse.pos[0] and \
                                    mouse.pos[0] < b_yes_x + b_yes_w:

                                if b_yes_y < mouse.pos[1] and \
                                        mouse.pos[1] < b_yes_y + b_yes_h:

                                    answer = 1

                            elif b_no_x < mouse.pos[0] and \
                                    mouse.pos[0] < b_no_x + b_no_w:

                                if b_no_y < mouse.pos[1] and \
                                        mouse.pos[1] < b_no_y + b_no_h:

                                    answer = 0

                if answer:

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
    snapshot.blit(screen, (0, 0))
    pygame.display.flip()


pygame.quit()


