import pygame
import random
import time
from os import path

img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

WIDTH = 1200
HEIGHT = 720

BLACK = (0, 0, 0)
RED = (255, 0, 0)


class Mob(pygame.sprite.Sprite):
    def __init__(self, x, y, mobs, start_time, health, cost, anim):
        self.initx = x
        self.anim = anim
        self.death_sound = pygame.mixer.Sound(path.join(snd_dir, 'boom1.mp3'))
        self.death_sound.set_volume(0.1)
        self.damage_sound = pygame.mixer.Sound(path.join(snd_dir, 'bot_damage.wav'))
        self.damage_sound.set_volume(0.2)
        self.timer = start_time
        self.animaindex = True
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(self.anim[0], (30, 40))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mobs = mobs
        self.speedx = 20
        self.health = health
        self.cost = cost

    def update(self):
        if time.time() - self.timer > 0.2 * ((len(self.mobs)) // 5) + 0.1:
            if self.animaindex:
                self.image = pygame.transform.scale(self.anim[1], (30, 40))
                self.image.set_colorkey(BLACK)
                self.animaindex = False
            else:
                self.image = pygame.transform.scale(self.anim[0], (30, 40))
                self.image.set_colorkey(BLACK)
                self.animaindex = True
            self.timer = time.time()
            self.rect.x += self.speedx
            if self.rect.right > 440 + self.initx:
                self.speedx *= -1
                self.rect.y += 40

            if self.rect.left < 0 + self.initx:
                self.speedx *= -1
                self.rect.y += 40

    def add_points(self, points):
        points += self.cost
        return points

    def damage(self, points):
        self.health -= 1
        if self.health == 0:
            self.death_sound.play()
            self.kill()
            points = self.add_points(points)
            return points
        else:
            self.damage_sound.play()
            return points


class BonusMob(Mob):
    def __init__(self, x, y, mobs, start_time):
        self.initx = x
        self.anim = [pygame.image.load(path.join(img_dir, 'bonusmob1.png')).convert(),
                     pygame.image.load(path.join(img_dir, 'bonusmob2.png')).convert()]
        self.death_sound = pygame.mixer.Sound(path.join(snd_dir, 'boom1.mp3'))
        self.death_sound.set_volume(0.2)
        self.timer = start_time
        self.animaindex = True
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(self.anim[0], (30, 40))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mobs = mobs
        self.speedx = 20
        self.health = 1
        self.cost = 20


class AnotherMob(Mob):
    def __init__(self, x, y, mobs, mobbullets, all_sprites, start_time, health, cost, anim):
        self.initx = x
        self.anim = anim
        self.death_sound = pygame.mixer.Sound(path.join(snd_dir, 'boom1.mp3'))
        self.death_sound.set_volume(0.2)
        self.damage_sound = pygame.mixer.Sound(path.join(snd_dir, 'bot_damage.wav'))
        self.damage_sound.set_volume(0.2)
        self.timer = start_time
        self.animaindex = True
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(self.anim[0], (30, 40))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mobs = mobs
        self.speedx = 20
        self.mobullets = mobbullets
        self.allspr = all_sprites
        self.health = health
        self.cost = cost

    def shoot(self, all_sprites, mobbullets):
        a = random.randrange(0, (len(self.mobs)) * 120)
        if a == 0:
            bullet = MobBullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            mobbullets.add(bullet)
            return all_sprites, mobbullets
        else:
            return all_sprites, mobbullets

    def update(self):
        allsprites, mobbullets = self.shoot(self.allspr, self.mobullets)
        if time.time() - self.timer > 0.2 * ((len(self.mobs)) // 5) + 0.1:
            if self.animaindex:
                self.image = pygame.transform.scale(self.anim[1], (30, 40))
                self.image.set_colorkey(BLACK)
                self.animaindex = False
            else:
                self.image = pygame.transform.scale(self.anim[0], (30, 40))
                self.image.set_colorkey(BLACK)
                self.animaindex = True
            self.timer = time.time()
            self.rect.x += self.speedx
            if self.rect.right > 440 + self.initx:
                self.speedx *= -1
                self.rect.y += 40

            if self.rect.left < 0 + self.initx:
                self.speedx *= -1
                self.rect.y += 40
        return allsprites, mobbullets


class LaserMob(AnotherMob):
    def shoot(self, all_sprites, mobbullets):
        a = random.randrange(0, (len(self.mobs)) * 120)
        if a == 0:
            bullet = LaserBullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            mobbullets.add(bullet)
            return all_sprites, mobbullets
        else:
            return all_sprites, mobbullets


class MobBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(path.join(img_dir, 'mobshoot.png')).convert(), (25, 45))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y + 50
        self.rect.centerx = x
        self.speedy = 5
        self.bul_sound = pygame.mixer.Sound(path.join(snd_dir, 'botshot.mp3'))
        self.bul_sound.set_volume(0.1)
        self.bul_sound.play()

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()


class LaserBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((5, 70))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = 10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()


class Ufo(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(path.join(img_dir, 'ufo.png')).convert(), (50, 50))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (0, 50)
        self.speedx = 5
        self.ufo_sound = pygame.mixer.Sound(path.join(snd_dir, 'ufo.mp3'))
        self.ufo_sound.set_volume(0.05)
        self.ufo_sound.play()

    def update(self):
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.kill()
