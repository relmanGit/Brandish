import os
import pygame
from component import *



## How to use:
'''
(1) Load sprite sheets.
(2) Construct animation_single[s] from sprite sheets.
(3) Add animation_single[s] to animation component.
'''


def craft_animation(entity, path):

    if 'Animation' not in entity.components:
        entity.add_component(Animation)

    sprite_sheets_dict = load_sheets(path)

    for animation_type in sprite_sheets_dict:

        sheet = sprite_sheets_dict[animation_type]
        single_animation = Animation_single(sheet)
        single_animation.type = animation_type
        entity.Animation.add(single_animation)


def load_sheets(path):

    sprite_sheet_dict = {}
    animation_types = os.listdir(path)
            
    for animation_type in animation_types:

        file = path + f'{animation_type}/0.png'
        sprite_sheet_dict[f'{animation_type}'] = pygame.image.load(file)

    return sprite_sheet_dict



class Animation(Component):


    def __init__(self, owner):
        super().__init__(owner)

        self.animations = {}


    def add(self, animation_single):

        animation_type = animation_single.type
        self.animations[animation_type] = animation_single


    def update(self):

        active_animation = self.owner.active_animation

        if active_animation not in self.animations.keys():

            return

        animation = self.animations[active_animation]
        animation.update()

        self.owner.image = animation.image



class Animation_single():


    def __init__(self, sprite_sheet, size=(32, 32)):

        self.sprite_sheet = sprite_sheet
        self.type = None

        sheet_width = sprite_sheet.get_rect().width
        self.num_sprites = sheet_width // size[0]

        self.speed = 0.10
        self.current_sprite = 0

        self.image = pygame.Surface(size)


    def __get_subsurface_rect(self):

        ## x position of the current sprite on the sprite sheet
        sprite_x = int(self.current_sprite) * self.image.get_rect().width
        topleft = (sprite_x, 0)

        size = self.image.get_rect().size

        area = (*topleft, *size)
        rect = pygame.Rect(*area)

        return rect


    def update(self):
        
        if self.current_sprite >= self.num_sprites:

            self.current_sprite = 0

        rect = self.__get_subsurface_rect()
        self.image = self.sprite_sheet.subsurface(rect)

        self.current_sprite += self.speed


