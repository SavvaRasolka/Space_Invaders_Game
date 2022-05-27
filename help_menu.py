import pygame
from button import Button
from caption import Caption
from os import path

img_dir = path.join(path.dirname(__file__), 'img')
font_dir = path.join(path.dirname(__file__), 'arcadeclassic')
snd_dir = path.join(path.dirname(__file__), 'snd')


class HelpMenu(pygame.sprite.Sprite):
    def __init__(self, size):
        pygame.sprite.Sprite.__init__(self)
        self.message = Caption('HELP', 80, size[0] / 2, 120)
        self.image = pygame.transform.scale(pygame.image.load(path.join(img_dir, 'help.png')).convert(), (1000, 620))
        self.rect = self.image.get_rect()
        self.rect.center = (size[0] / 2, size[1] / 2)
        self.button_ex = Button((370, 50), 'EXIT', self.rect.centerx, self.rect.centery+200, 50)
        self.buttons = pygame.sprite.Group()
        self.buttons.add(self.button_ex)
        self.captions = pygame.sprite.Group()
        self.captions.add(self.button_ex.caption)
        self.captions.add(self.message)


def help_menu(screen):
    buttons = HelpMenu(screen.get_size())
    menu = pygame.sprite.Group()
    menu.add(buttons)
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
