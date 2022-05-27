import pygame
from button import Button
from caption import Caption
from os import path
img_dir = path.join(path.dirname(__file__), 'img')


class Pause(pygame.sprite.Sprite):
    def __init__(self, size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(path.join(img_dir, 'pause.png')).convert(), (400, 350))
        self.rect = self.image.get_rect()
        self.name = Caption('PAUSE', 120, size[0]/2, size[1]/2-100)
        self.rect.center = (size[0]/2, size[1]/2)
        self.button_con = Button((370, 50), 'CONTINUE', self.rect.centerx, self.rect.centery, 50)
        self.button_ex = Button((370, 50), 'EXIT', self.rect.centerx, self.rect.centery+100, 50)
        self.buttons = pygame.sprite.Group()
        self.buttons.add(self.button_con)
        self.buttons.add(self.button_ex)
        self.captions = pygame.sprite.Group()
        self.captions.add(self.button_con.caption)
        self.captions.add(self.button_ex.caption)
        self.captions.add(self.name)


def pause(screen):
    buttons = Pause(screen.get_size())
    menu = pygame.sprite.Group()
    menu.add(buttons)
    running = True
    while running:
        xm, ym = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if buttons.button_con.rect.collidepoint((xm, ym)):
                    return False
                elif buttons.button_ex.rect.collidepoint((xm, ym)):
                    return True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
            elif event.type == pygame.MOUSEMOTION:
                if buttons.button_con.rect.collidepoint((xm, ym)):
                    buttons.button_con.state(True)
                elif buttons.button_ex.rect.collidepoint((xm, ym)):
                    buttons.button_ex.state(True)
                else:
                    buttons.button_ex.state(False)
                    buttons.button_con.state(False)

        buttons.buttons.update()

        menu.draw(screen)
        buttons.buttons.draw(screen)
        buttons.captions.draw(screen)

        pygame.display.flip()

    pygame.quit()
