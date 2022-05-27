import pygame
from os import path

font_dir = path.join(path.dirname(__file__), 'arcadeclassic')
print(font_dir)


class Caption(pygame.sprite.Sprite):
    def __init__(self, capture, fontsize, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.capture = capture
        self.font = pygame.font.Font(path.join(font_dir, 'ARCADECLASSIC.TTF'), fontsize)
        self.image = self.font.render(capture, False, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (x+3, y)

    def change_color(self, color):
        self.image = self.font.render(self.capture, False, color)