import pygame
from os import path
from caption import Caption

img_dir = path.join(path.dirname(__file__), 'img')


class Button(pygame.sprite.Sprite):
    def __init__(self, size, capture, x, y, fontsize):
        pygame.sprite.Sprite.__init__(self)
        self.caption = Caption(capture, fontsize, x, y)
        self.centre = (x, y)
        self.image_off = pygame.transform.scale(pygame.image.load(path.join(img_dir, 'button_off.png')).convert(), size)
        self.image_off.set_colorkey((0, 0, 0))
        self.image_on = pygame.transform.scale(pygame.image.load(path.join(img_dir, 'button_on.png')).convert(), size)
        self.image_on.set_colorkey((0, 0, 0))
        self.state(False)

    def state(self, state):
        if state:
            self.image = self.image_on
        else:
            self.image = self.image_off
        self.rect = self.image.get_rect()
        self.rect.center = self.centre
