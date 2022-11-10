import pygame


BLACK = (0, 0, 0)



class Typewriter:


    def __init__(self, font_name='arial', font_size=24, font_color=BLACK):

        self.name = 'myname'
        self.font = pygame.font.SysFont(font_name, font_size)
        self.font_color = font_color
        self.text = None


    def write(self, string):

        text_surface = self.font.render(string, True, self.font_color)
        text = Text(text_surface)

        return text_surface



class Text:


    def __init__(self, text_surface):

        self.image = text_surface
        self.rect = self.image.get_rect()


    def rewrite(self, text_surface):

        pos = self.rect.topleft

        self.image = text_surface
        self.rect = self.image.get_rect()
        self.rect.topleft = pos



