import pygame
from os import path

img_dir = path.join(path.dirname(__file__), 'img')

HEIGHT = 720

BLACK = (0, 0, 0)


def dropbonus(x, y, all_sprites, bonuses):
    bonus = Bonus(x, y)
    all_sprites.add(bonus)
    bonuses.add(bonus)
    return all_sprites, bonuses


class Bonus(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(path.join(img_dir, 'bonus.png')).convert(), (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speedy = 3

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()
