import pygame
from os import path

img_dir = path.join(path.dirname(__file__), 'img')

BLACK = (0, 0, 0)


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(path.join(img_dir, 'boom.png')).convert(), (50, 50))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0

    def update(self):
        self.frame += 1
        if self.frame == 60:
            self.kill()
        else:
            center = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = center
