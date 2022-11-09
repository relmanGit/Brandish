import os
import pygame
from component import *


class Entity(pygame.sprite.Sprite):


    def __init__(self, width=32, height=32):
        super().__init__()

        self.components = []
        self.active_animation = 'idle'
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect()


    def add_component(self, TComponent):

        component = TComponent(self)
        class_name = component.__class__.__name__

        if isinstance(component, Component):
            var_name = class_name#.lower()
            code = f'self.{var_name} = TComponent(self)'
            exec(code)
            self.components.append(class_name)

        else:
            print('FAIL: entity.add_component')


    def update(self):

        for component_name in self.components:
            code = f'self.{component_name}.update()'
            exec(code)

        if not self.image:
            self._temp_image()


    def _temp_image(self):

        width, height = (64, 64)
        self.image = pygame.Surface((width, height))
        RED = (255, 0 ,0)
        self.image.fill(RED)


