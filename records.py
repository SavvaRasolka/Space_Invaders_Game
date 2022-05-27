import pygame
from button import Button
from caption import Caption
from os import path

img_dir = path.join(path.dirname(__file__), 'img')
font_dir = path.join(path.dirname(__file__), 'arcadeclassic')
snd_dir = path.join(path.dirname(__file__), 'snd')


class Records(pygame.sprite.Sprite):
    def __init__(self, size):
        pygame.sprite.Sprite.__init__(self)
        self.message = Caption('RECORDS', 80, size[0] / 2, 120)
        self.name = Caption('NAME', 50, size[0] / 2 - 200, 200)
        self.score = Caption('SCORE', 50, size[0] / 2, 200)
        self.wave = Caption('WAVE', 50, size[0] / 2 + 200, 200)
        self.image = pygame.transform.scale(pygame.image.load(path.join(img_dir, 'pause.png')).convert(), (800, 600))
        self.rect = self.image.get_rect()
        self.rect.center = (size[0] / 2, size[1] / 2)
        self.button_ex = Button((370, 50), 'EXIT', self.rect.centerx, self.rect.centery+200, 50)
        self.buttons = pygame.sprite.Group()
        self.buttons.add(self.button_ex)
        self.captions = pygame.sprite.Group()
        self.captions.add(self.button_ex.caption)
        self.captions.add(self.message)
        self.captions.add(self.name)
        self.captions.add(self.score)
        self.captions.add(self.wave)


def create_table(table, size, group):
    shift = 0
    for each_name in table:
        name = Caption(each_name, 30, size[0]/2 - 200, 250 + 50 * shift)
        score = Caption(str(table[each_name][0]), 30, size[0]/2, 250 + 50 * shift)
        wave = Caption(str(table[each_name][1]), 30, size[0]/2+200, 250 + 50 * shift)
        group.add(name)
        group.add(score)
        group.add(wave)
        shift += 1
    return group


def records(screen, t):
    buttons = Records(screen.get_size())
    menu = pygame.sprite.Group()
    menu.add(buttons)
    menu = create_table(t, screen.get_size(), menu)
    running = True
    while running:
        xm, ym = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if buttons.button_ex.rect.collidepoint((xm, ym)):
                    return True
            elif event.type == pygame.MOUSEMOTION:
                if buttons.button_ex.rect.collidepoint((xm, ym)):
                    buttons.button_ex.state(True)
                else:
                    buttons.button_ex.state(False)
        buttons.buttons.update()
        menu.draw(screen)
        buttons.buttons.draw(screen)
        buttons.captions.draw(screen)
        pygame.display.flip()
    pygame.quit()
