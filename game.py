import time

import pygame
import random
from os import path
img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')
WIDTH = 1200
HEIGHT = 720
FPS = 60

# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
wait = time.time()


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font('E:\PPVIS\lab3python\\arcadeclassic\ARCADECLASSIC.TTF', size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def draw_life(surf, x, y):
    icon = pygame.image.load(path.join(img_dir, 'heart.png')).convert()
    icon = pygame.transform.scale(icon, (35, 35))
    icon.set_colorkey(BLACK)
    icon_rect = icon.get_rect()
    icon_rect.midtop = (x, y)
    surf.blit(icon, icon_rect)


def dropbonus(x, y):
    bonus = Bonus(x, y)
    all_sprites.add(bonus)
    bonuses.add(bonus)


class Bonus(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bonus_img, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speedy = 3

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.speedy = 0
        self.health = 3
        self.bonus = 0
        self.timer = 0

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
        print(self.bonus)

    def shoot(self):
        if self.bonus == 0:
            if len(bullets) == 0:
                bullet = Bullet(self.rect.centerx, self.rect.top, 0)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
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
                shoot_sound.play()
        elif self.bonus == 2:
            if len(bullets) < 3:
                bullet = Bullet(self.rect.centerx, self.rect.top, 0)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()

    def damage(self):
        self.health -= 1
        if self.health == 0:
            self.kill()
            death_player.play()
            song.stop()
            endsong = pygame.mixer.Sound(path.join(snd_dir, 'Quinton Sung-Exit Music (Radiohead 8-bit).mp3'))
            endsong.set_volume(0.1)
            endsong.play()
        else:
            damage_player.play()


class Tower(pygame.sprite.Sprite):
    def __init__(self, x ,y, spritelist):
        self.anim = spritelist
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(self.anim[0], (30, 40))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.health = 2

    def damage(self):
        self.health -= 1
        if self.health == 0:
            self.kill()
        else:
            self.image = pygame.transform.scale(self.anim[1], (30, 30))
            self.image.set_colorkey(BLACK)



class Mob(pygame.sprite.Sprite):
    def __init__(self, x, y, spritelist):
        self.initx = x
        self.anim = spritelist
        self.timer = time.time()
        #self.inity = y
        self.animaindex = True
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(self.anim[0], (30, 40))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speedx = 20

    def update(self):
        if time.time() - self.timer > 0.2*((len(mobs)+len(amobs))//5)+0.1:
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


class HeavyMob(Mob):
    def __init__(self, x, y, wait, spritelist):
        self.initx = x
        self.anim = spritelist
        self.timer = wait
        #self.inity = y
        self.animaindex = True
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(self.anim[0], (30, 40))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        #self.pos = (self.rect.x, self.rect.y)
        self.speedx = 20
        self.health = 3

    def damage(self):
        self.health -= 1
        if self.health == 0:
            self.kill()
            death_player.play()
        else:
            damage_player.play()


class AnotherMob(Mob):
    def shoot(self):
        a = random.randrange(0, (len(mobs)+len(amobs))*120)
        if a == 0:
            bullet = MobBullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            mobbullets.add(bullet)
            mobshot_snd.play()

    def update(self):
        self.shoot()
        if time.time() - self.timer > 0.2*((len(mobs)+len(amobs))//5)+0.1:
            #pygame.time.get_ticks() = 0
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
        #self.rect.y += self.speedy
            if self.rect.right > 440 + self.initx:
                self.speedx *= -1
                self.rect.y += 40

            if self.rect.left < 0 + self.initx:
                self.speedx *= -1
                self.rect.y += 40


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


class MobBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bulletsprite, (15, 25))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y + 50
        self.rect.centerx = x
        self.speedy = 5

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()


class Ufo(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(ufo_img, (50, 50))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (0, 50)
        self.speedx = 5
        ufo_snd.play()

    def update(self):
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.kill()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, sprite):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(sprite, (50, 50))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 60

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == 20:
                self.kill()
            else:
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center


# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
background = pygame.image.load(path.join(img_dir, 'background.jpg')).convert()
background_rect = background.get_rect()
clock = pygame.time.Clock()
player_img = pygame.image.load(path.join(img_dir, 'player_space.png')).convert()
mob_img = [pygame.image.load(path.join(img_dir, 'mob1.png')).convert(), pygame.image.load(path.join(img_dir, 'mob2.png')).convert()]
mob_img2 = [pygame.image.load(path.join(img_dir, 'mob21.png')).convert(), pygame.image.load(path.join(img_dir, 'mob22.png')).convert()]
mob_img3 = [pygame.image.load(path.join(img_dir, 'mob31.png')).convert(), pygame.image.load(path.join(img_dir, 'mob32.png')).convert()]
mob_img4 = [pygame.image.load(path.join(img_dir, 'mob41.png')).convert(), pygame.image.load(path.join(img_dir, 'mob42.png')).convert()]
mob_img5 = [pygame.image.load(path.join(img_dir, 'mob51.png')).convert(), pygame.image.load(path.join(img_dir, 'mob52.png')).convert()]
mob_img6 = [pygame.image.load(path.join(img_dir, 'mob61.png')).convert(), pygame.image.load(path.join(img_dir, 'mob62.png')).convert()]
amob_img = [pygame.image.load(path.join(img_dir, 'amob1.png')).convert(), pygame.image.load(path.join(img_dir, 'amob2.png')).convert()]
bonus_mob_img = [pygame.image.load(path.join(img_dir, 'bonusmob1.png')).convert(), pygame.image.load(path.join(img_dir, 'bonusmob2.png')).convert()]
tower_img = [pygame.image.load(path.join(img_dir, 'bonusmob1.png')).convert(),pygame.image.load(path.join(img_dir, 'bonusmob2.png')).convert()]
bulletsprite = pygame.image.load(path.join(img_dir, 'mobshoot.png')).convert()
explosion_anim = pygame.image.load(path.join(img_dir, 'boom.png')).convert()
ufo_img = pygame.image.load(path.join(img_dir, 'ufo.png')).convert()
hert = pygame.image.load(path.join(img_dir, 'heart.png')).convert()
bonus_img = pygame.image.load(path.join(img_dir, 'bonus.png')).convert()
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'teleport.mp3'))
shoot_sound.set_volume(0.1)
mobshot_snd = pygame.mixer.Sound(path.join(snd_dir, 'botshot.mp3'))
mobshot_snd.set_volume(0.1)
mobmurder = pygame.mixer.Sound(path.join(snd_dir, 'boom1.mp3'))
mobmurder.set_volume(0.1)
ufo_snd = pygame.mixer.Sound(path.join(snd_dir, 'ufo.mp3'))
ufo_snd.set_volume(0.05)
bonus_snd = pygame.mixer.Sound(path.join(snd_dir, 'bonus.mp3'))
bonus_snd.set_volume(0.1)
death_player = pygame.mixer.Sound(path.join(snd_dir, 'death.mp3'))
death_player.set_volume(0.5)
damage_player = pygame.mixer.Sound(path.join(snd_dir, 'damage.wav'))
damage_player.set_volume(0.4)
song = pygame.mixer.Sound(path.join(snd_dir, 'Radiohead-Subterranean Homesick Alien (8-bit).mp3'))
song.set_volume(0.1)
bullets = pygame.sprite.Group()
mobbullets = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
player = Player()
mobs = pygame.sprite.Group()
amobs = pygame.sprite.Group()
bonusmobs = pygame.sprite.Group()
bonuses = pygame.sprite.Group()
ufos = pygame.sprite.Group()
towers = pygame.sprite.Group()
all_sprites.add(player)
score = 0
for i in range(11):
    m = AnotherMob(40 + 70 * i, 90, amob_img)
    all_sprites.add(m)
    amobs.add(m)
for i in range(11):
    m = Mob(40 + 70 * i, 130, bonus_mob_img)
    all_sprites.add(m)
    bonusmobs.add(m)
for ind in range(3):
    for i in range(11):
        m = Mob(40 + 70 * i, 40 * (ind+2)+ 100, mob_img)
        all_sprites.add(m)
        mobs.add(m)
for ind in range(3):
    for i in range(3):
        t = Tower(60 + 30*i, 1000+30*ind, tower_img)
        all_sprites.add(t)
        towers.add(t)
song.play(loops=-1)
# Цикл игры
running = True

while running:
    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # Обновление
    all_sprites.update()
    if random.randrange(0, 1200) == 0:
        ufo = Ufo()
        all_sprites.add(ufo)
        ufos.add(ufo)
    hitsmobs = pygame.sprite.groupcollide(mobs, bullets, True, True)
    print(hitsmobs)
    for hit in hitsmobs:
        expl = Explosion(hit.rect.center, explosion_anim)
        all_sprites.add(expl)
        score += 10
        mobmurder.play()
    hitamobs = pygame.sprite.groupcollide(amobs, bullets, True, True)
    for hit in hitamobs:
        expl = Explosion(hit.rect.center, explosion_anim)
        all_sprites.add(expl)
        score += 30
        mobmurder.play()
    hitsplayer = pygame.sprite.spritecollide(player, mobbullets, True)
    for hit in hitsplayer:
        expl = Explosion(hit.rect.center, explosion_anim)
        all_sprites.add(expl)
        player.damage()
    hitbullets = pygame.sprite.groupcollide(mobbullets, bullets, True, True)
    for hit in hitbullets:
        expl = Explosion(hit.rect.center, explosion_anim)
        all_sprites.add(expl)
    hitbonusmob = pygame.sprite.groupcollide(bonusmobs, bullets, True, True)
    for hit in hitbonusmob:
        expl = Explosion(hit.rect.center, explosion_anim)
        all_sprites.add(expl)
        dropbonus(hit.rect.x, hit.rect.y)
        mobmurder.play()
    takebonus = pygame.sprite.spritecollide(player, bonuses, True)
    for hit in takebonus:
        player.bonusupdate(time.time())
        bonus_snd.play()

    hitufo = pygame.sprite.groupcollide(ufos, bullets, True, True)
    for hit in hitufo:
        expl = Explosion(hit.rect.center, explosion_anim)
        all_sprites.add(expl)
        score += 300

    hittower = pygame.sprite.groupcollide(towers, bullets, False, True)
   # for hit in hittower:



    # Рендеринг
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, 'SCORE ' + str(score), 28, 80, 5)
    pygame.draw.line(screen, (255, 255, 255), (0, 35), (WIDTH, 35), 4)
    pygame.draw.line(screen, GREEN, (0, HEIGHT - 15), (WIDTH, HEIGHT - 15), 4)
    for life in range(player.health):
        draw_life(screen, 1100+life*30, 0)
    if player.bonus == 1:
        pygame.draw.line(screen, BLUE, (0, HEIGHT - 10), (WIDTH-80*(time.time()-player.timer), HEIGHT - 10), 4)
    if player.bonus == 2:
        pygame.draw.line(screen, RED, (0, HEIGHT - 10), (WIDTH-80*(time.time()-player.timer), HEIGHT - 10), 4)
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()
pygame.quit()