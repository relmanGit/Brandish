import pygame
from constants import *
from animation import *
from hellper import *
from entity import *



## Testing ##
pygame.init()
#screen_size = (SCREEN_WIDTH*2, SCREEN_HEIGHT*2.1)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen_size = screen.get_size()
grid = Grid()
grid.toggled = True

clock = pygame.time.Clock()

background = pygame.Surface(screen.get_size())
background.fill(MY_BLUE)

set_path = set_path + which_set
tile_map = tm.Tile_map(set_path, set_size)
#tile_map.tile_set = tile_map.tile_set.convert_alpha()


## Text rendering ##
font = pygame.font.SysFont('Arial', 24)
font_color = BLACK

tracker = font.render('(0, 0)', True, font_color)
tracker_rect = tracker.get_rect()

tracker_x = 4
tracker_y = (screen_size[1] - set_size[1]) + 2
tracker_pos = (tracker_x, tracker_y)

tracker_rect.topleft = tracker_pos


## Mouse ##
mouse = Mouse()


## Entity stuff ##
Player = Entity()
player_path = '../assets/img/buddy_guy/'

enemies = []
num_enemies = 2

for i in range(num_enemies):

    e = Entity()
    e.rect = e.rect.move(((i + 1) * set_size[0], 0 ))
    enemies.append(e)

enemy_path = '../assets/img/buddy_guy/'


## Animation ##
craft_animation(Player, player_path)

for e in enemies:
    craft_animation(e, enemy_path)

entities = enemies + [Player]
entities_group = pygame.sprite.Group(entities)



## Main Game Loop ##
running = True

while running:

    clock.tick(FPS)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False
            break

        if event.type == pygame.MOUSEMOTION:

            mouse.pos = event.pos
            mouse.cell = cell_pos(mouse.pos)

            tracker = font.render(str(mouse.cell), True, font_color)
            tracker_rect.topleft = tracker_pos

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

    ## Blit background ##
    screen.blit(background, (0, 0))

    ## Update and blit characters group ##
    entities_group.update()
    entities_group.draw(screen)

    ## Mouse cancel ##
    if mouse.right_down:

        mouse.reset()

    ## Draw grid lines ##
    if grid.toggled:

        grid.draw(screen)

    ## Draw selected tile at mouse location ##
    if mouse.tile:

        sub_x, sub_y = mouse.pos
        offset_x, offset_y = (set_size[0] // 2, set_size[1] // 2)
        sub_pos = (sub_x - offset_x, sub_y - offset_y)
        screen.blit(mouse.tile.image, sub_pos)

    ## Draw text (mouse.pos coordinates at screen.bottomleft)
    screen.blit(tracker, tracker_rect)
    pygame.display.flip()

pygame.quit()


