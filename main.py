import time
import random
from test_game import game
import pygame
from objects.button import Button
from objects.caption import Caption
from windows.help_menu import help_menu
from windows.records import records
from os import path
from parsers.load_files import TableHandler

img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')
WIDTH = 1200
HEIGHT = 720
FPS = 60

BLACK = (0, 0, 0)

wait = time.time()


class Menu(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.name = Caption('SPACE INVADERS', 140, WIDTH/2+10, 90)
        self.button_start = Button((450, 70), 'START', x/2, y/2-100, 70)
        self.button_records = Button((450, 70), 'RECORDS', x/2, y/2, 70)
        self.button_help = Button((450, 70), 'HELP', x/2, y/2 + 100, 70)
        self.button_exit = Button((450, 70), 'EXIT', x/2, y/2 + 200, 70)
        self.buttons = pygame.sprite.Group()
        self.buttons.add(self.button_start)
        self.buttons.add(self.button_records)
        self.buttons.add(self.button_help)
        self.buttons.add(self.button_exit)
        self.captions = pygame.sprite.Group()
        self.captions.add(self.name)
        self.captions.add(self.button_start.caption)
        self.captions.add(self.button_records.caption)
        self.captions.add(self.button_help.caption)
        self.captions.add(self.button_exit.caption)


class Menumobs(pygame.sprite.Sprite):
    def __init__(self, x, y, sprite):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(sprite, (30, 40))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedx = 3

    def update(self):
        self.rect.x += self.speedx
        if self.rect.x > WIDTH:
            self.kill()


def load_records():
    table = {}
    record_table = TableHandler()
    record_table.parser.setContentHandler(record_table)
    record_table.parser.parse('config/record_table.xml')
    for each_record in record_table.records:
        temp = {each_record[0]: (each_record[1], each_record[2])}
        table.update(temp)
    return table


pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menu")
background = pygame.image.load(path.join(img_dir, 'background.jpg')).convert()
background_rect = background.get_rect()
clock = pygame.time.Clock()
menu = Menu(WIDTH, HEIGHT)
song = pygame.mixer.Sound(path.join(snd_dir, '03-i_am_citizen_insane.mp3'))
song.set_volume(0.1)
song.play(loops=-1)
t = load_records()
score_list = []
for i in t.values():
    score_list.append(int(i[0]))
max_score = max(score_list)
print(max_score)
sprite_list = [pygame.image.load(path.join(img_dir, 'amob1.png')).convert(),
               pygame.image.load(path.join(img_dir, 'mob1.png')).convert(),
               pygame.image.load(path.join(img_dir, 'mob21.png')).convert(),
               pygame.image.load(path.join(img_dir, 'mob31.png')).convert(),
               pygame.image.load(path.join(img_dir, 'mob41.png')).convert(),
               pygame.image.load(path.join(img_dir, 'mob51.png')).convert(),
               pygame.image.load(path.join(img_dir, 'mob61.png')).convert(),
               pygame.image.load(path.join(img_dir, 'mob62.png')).convert()]
all_sprites = pygame.sprite.Group()
running = True

while running:
    clock.tick(FPS)
    if random.randrange(0, 400) == 0:
        b = Menumobs(0, random.randrange(0, HEIGHT), sprite_list[random.randrange(0, 8)])
        all_sprites.add(b)
    xm, ym = pygame.mouse.get_pos()
    buttom1 = pygame.Rect(50, 100, 200, 50)
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if menu.button_start.rect.collidepoint((xm, ym)):
                song.stop()
                game(int(max_score), t)
                song.play()
            elif menu.button_records.rect.collidepoint((xm, ym)):
                records(screen, t)
            elif menu.button_help.rect.collidepoint((xm, ym)):
                help_menu(screen)
            elif menu.button_exit.rect.collidepoint((xm, ym)):
                running = False
        elif event.type == pygame.MOUSEMOTION:
            if menu.button_start.rect.collidepoint((xm, ym)):
                menu.button_start.state(True)
            elif menu.button_records.rect.collidepoint((xm, ym)):
                menu.button_records.state(True)
            elif menu.button_help.rect.collidepoint((xm, ym)):
                menu.button_help.state(True)
            elif menu.button_exit.rect.collidepoint((xm, ym)):
                menu.button_exit.state(True)
            else:
                menu.button_start.state(False)
                menu.button_records.state(False)
                menu.button_help.state(False)
                menu.button_exit.state(False)

    all_sprites.update()
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    menu.buttons.draw(screen)
    menu.captions.draw(screen)
    pygame.display.flip()
pygame.quit()
