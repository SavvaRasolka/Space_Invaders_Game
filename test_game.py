import time
import pygame
import random
from os import path
from pause_game import pause
from win import win
from load_waves import WavesHandler
from mobs import Mob, AnotherMob, LaserMob, BonusMob, Ufo
from bonus import dropbonus
from player import Player
from explosion import Explosion


img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')
font_dir = path.join(path.dirname(__file__), 'arcadeclassic')
config_dir = path.join(path.dirname(__file__), 'config')
WIDTH = 1200
HEIGHT = 720
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(path.join(font_dir, 'ARCADECLASSIC.TTF'), size)
    text_surface = font.render(text, False, WHITE)
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


class BorderLine(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((WIDTH, 4))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, HEIGHT - 15)


def mob_from_file(wave, mobs_group, mobullets, allsprites, bonusmobs, sprite_dict):
    start_time = time.time()
    mobes = WavesHandler()
    mobes.parser.setContentHandler(mobes)
    mobes.parser.parse('config/wave' + str(wave) + '.xml')
    pos_x = 0
    pos_y = 0
    progress = 0
    for each_mob in mobes.mobs:
        progress += 1
        if each_mob[0] == 'mob':
            m = Mob(40 + 70 * pos_x, 90 + 40 * pos_y, mobs_group, start_time, int(each_mob[1]), int(each_mob[3]),
                    sprite_dict[each_mob[2]])
            mobs_group.add(m)
            allsprites.add(m)
        elif each_mob[0] == 'amob':
            m = AnotherMob(40 + 70 * pos_x, 90 + 40 * pos_y, mobs_group, mobullets, allsprites, start_time,
                           int(each_mob[1]), int(each_mob[3]), sprite_dict[each_mob[2]])
            mobs_group.add(m)
            allsprites.add(m)
        elif each_mob[0] == 'bonusmob':
            m = BonusMob(40 + 70 * pos_x, 90 + 40 * pos_y, mobs_group, start_time)
            bonusmobs.add(m)
            allsprites.add(m)
        elif each_mob[0] == 'lasermob':
            m = LaserMob(40 + 70 * pos_x, 90 + 40 * pos_y, mobs_group, mobullets, allsprites, start_time,
                         int(each_mob[1]), int(each_mob[3]), sprite_dict[each_mob[2]])
            mobs_group.add(m)
            allsprites.add(m)
        if pos_x == 10:
            pos_x = 0
            pos_y += 1
        else:
            pos_x += 1
    return mobs_group, bonusmobs, allsprites


def game(max_score, table):
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Space Invaders")
    sprite_dict = {'mob': [pygame.image.load(path.join(img_dir, 'mob1.png')).convert(),
                           pygame.image.load(path.join(img_dir, 'mob2.png')).convert()],
                   'mob1': [pygame.image.load(path.join(img_dir, 'mob11.png')).convert(),
                            pygame.image.load(path.join(img_dir, 'mob12.png')).convert()],
                   'mob2': [pygame.image.load(path.join(img_dir, 'mob21.png')).convert(),
                            pygame.image.load(path.join(img_dir, 'mob22.png')).convert()],
                   'mob3': [pygame.image.load(path.join(img_dir, 'mob31.png')).convert(),
                            pygame.image.load(path.join(img_dir, 'mob32.png')).convert()],
                   'mob4': [pygame.image.load(path.join(img_dir, 'mob41.png')).convert(),
                            pygame.image.load(path.join(img_dir, 'mob42.png')).convert()],
                   'mob5': [pygame.image.load(path.join(img_dir, 'mob51.png')).convert(),
                            pygame.image.load(path.join(img_dir, 'mob52.png')).convert()],
                   'mob6': [pygame.image.load(path.join(img_dir, 'mob61.png')).convert(),
                            pygame.image.load(path.join(img_dir, 'mob62.png')).convert()],
                   'amob': [pygame.image.load(path.join(img_dir, 'amob1.png')).convert(),
                            pygame.image.load(path.join(img_dir, 'amob2.png')).convert()],
                   }
    background = pygame.image.load(path.join(img_dir, 'background.jpg')).convert()
    background_rect = background.get_rect()
    los_border = BorderLine()
    clock = pygame.time.Clock()
    bullets = pygame.sprite.Group()
    mobbullets = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    mobs = pygame.sprite.Group()
    bonusmobs = pygame.sprite.Group()
    bonuses = pygame.sprite.Group()
    ufos = pygame.sprite.Group()
    player = Player()
    all_sprites.add(player)
    all_sprites.add(los_border)
    score = 0
    wave_num = 1
    mobs, bonusmobs, all_sprites = mob_from_file(wave_num, mobs, mobbullets, all_sprites, bonusmobs, sprite_dict)
    song = pygame.mixer.Sound(path.join(snd_dir, 'Radiohead-Subterranean Homesick Alien (8-bit).mp3'))
    song.set_volume(0.1)
    song.play(loops=-1)
    running = True

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    all_sprites, bullets = player.shoot(all_sprites, bullets)
                if event.key == pygame.K_ESCAPE:
                    if pause(screen):
                        song.stop()
                        return

        all_sprites.update()
        losing = pygame.sprite.spritecollide(los_border, mobs, True)
        for losed in losing:
            song.stop()
            if max_score >= score:
                score = False
            if win(screen, score, wave_num, 'YOU LOSE', table):
                return
        blosing = pygame.sprite.spritecollide(los_border, bonusmobs, True)
        for losed in blosing:
            song.stop()
            if max_score >= score:
                score = False
            if win(screen, score, wave_num, 'YOU LOSE', table):
                return
        if player.health == 0:
            song.stop()
            if max_score >= score:
                score = False
            if win(screen, score, wave_num, 'YOU LOSE', table):
                return
        if len(mobs)+len(bonusmobs) == 0:
            wave_num += 1
            if wave_num == 21:
                song.stop()
                if win(screen, score, wave_num-1, 'YOU WIN', table):
                    return
            else:
                mobs, bonusmobs, all_sprites = mob_from_file(wave_num, mobs, mobbullets, all_sprites, bonusmobs,
                                                             sprite_dict)
        if random.randrange(0, 2200) == 0:
            ufo = Ufo()
            all_sprites.add(ufo)
            ufos.add(ufo)

        hitsmobs = pygame.sprite.groupcollide(bullets, mobs, True, False)
        for hits in hitsmobs.values():
            for hit in hits:
                expl = Explosion(hit.rect.center)
                all_sprites.add(expl)
                score = hit.damage(score)

        hitsplayer = pygame.sprite.spritecollide(player, mobbullets, True)
        for hit in hitsplayer:
            expl = Explosion(hit.rect.center)
            all_sprites.add(expl)
            player.damage()

        hitbullets = pygame.sprite.groupcollide(mobbullets, bullets, True, True)
        for hit in hitbullets:
            expl = Explosion(hit.rect.center)
            all_sprites.add(expl)

        hitbonusmob = pygame.sprite.groupcollide(bullets, bonusmobs, True, True)
        for hites in hitbonusmob.values():
            for hit in hites:
                expl = Explosion(hit.rect.center)
                all_sprites.add(expl)
                all_sprites, bonuses = dropbonus(hit.rect.x, hit.rect.y, all_sprites, bonuses)
                score = hit.damage(score)

        takebonus = pygame.sprite.spritecollide(player, bonuses, True)
        for hit in takebonus:
            player.bonusupdate(time.time())

        hitufo = pygame.sprite.groupcollide(ufos, bullets, True, True)
        for hit in hitufo:
            expl = Explosion(hit.rect.center)
            all_sprites.add(expl)
            score += 300

        screen.fill(BLACK)
        screen.blit(background, background_rect)
        all_sprites.draw(screen)
        draw_text(screen, 'SCORE ' + str(score), 28, 80, 5)
        draw_text(screen, 'WAVE' + str(wave_num), 28, 200, 5)
        pygame.draw.line(screen, (255, 255, 255), (0, 35), (WIDTH, 35), 4)
        for life in range(player.health):
            draw_life(screen, 1100 + life * 30, 0)
        if player.bonus == 1:
            pygame.draw.line(screen, BLUE, (0, HEIGHT - 10), (WIDTH - 125 * (time.time() - player.timer), HEIGHT - 10),
                             4)
        if player.bonus == 2:
            pygame.draw.line(screen, RED, (0, HEIGHT - 10), (WIDTH - 125 * (time.time() - player.timer), HEIGHT - 10),
                             4)
        pygame.display.flip()
    pygame.quit()
