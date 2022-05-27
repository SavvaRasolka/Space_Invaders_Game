import pygame
import time
import random
from os import path
img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

WIDTH = 1200
HEIGHT = 720

WHITE = (255, 255, 255)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(path.join(img_dir, 'player_space.png')).convert(),
                                            (50, 38))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.speedy = 0
        self.health = 3
        self.bonus = 0
        self.timer = 0
        self.damage_sound = pygame.mixer.Sound(path.join(snd_dir, 'damage.wav'))
        self.damage_sound.set_volume(0.4)
        self.death_sound = pygame.mixer.Sound(path.join(snd_dir, 'death.mp3'))
        self.death_sound.set_volume(0.5)
        self.bonus_sound = pygame.mixer.Sound(path.join(snd_dir, 'bonus.mp3'))
        self.bonus_sound.set_volume(0.1)
        self.shot_sound = pygame.mixer.Sound(path.join(snd_dir, 'teleport.mp3'))
        self.shot_sound.set_volume(0.1)

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if time.time() - self.timer > 10:
            self.bonus = 0

    def bonusupdate(self, wait):
        self.timer = wait
        self.bonus = random.randrange(1, 3)
        self.bonus_sound.play()

    def shoot(self, all_sprites, bullets):
        if self.bonus == 0:
            if len(bullets) == 0:
                bullet = Bullet(self.rect.centerx, self.rect.top, 0)
                all_sprites.add(bullet)
                bullets.add(bullet)
                self.shot_sound.play()
                return all_sprites, bullets
            else:
                return all_sprites, bullets
        elif self.bonus == 1:
            if len(bullets) == 0:
                bullet1 = Bullet(self.rect.centerx, self.rect.top, 1.5)
                all_sprites.add(bullet1)
                bullets.add(bullet1)
                bullet2 = Bullet(self.rect.centerx, self.rect.top, -1)
                all_sprites.add(bullet2)
                bullets.add(bullet2)
                bullet3 = Bullet(self.rect.centerx, self.rect.top, 0)
                all_sprites.add(bullet3)
                bullets.add(bullet3)
                self.shot_sound.play()
                return all_sprites, bullets
            else:
                return all_sprites, bullets
        elif self.bonus == 2:
            if len(bullets) < 3:
                bullet = Bullet(self.rect.centerx, self.rect.top, 0)
                all_sprites.add(bullet)
                bullets.add(bullet)
                self.shot_sound.play()
                return all_sprites, bullets
            else:
                return all_sprites, bullets

    def damage(self):
        self.health -= 1
        if self.health == 0:
            self.kill()
            self.death_sound.play()
        else:
            self.damage_sound.play()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((3, 20))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
        self.speedx = speed

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top < 35:
            self.kill()