import pygame
from button import Button, Caption
from save_files import save_to_file
from os import path

WHITE = (255, 255, 255)

img_dir = path.join(path.dirname(__file__), 'img')
font_dir = path.join(path.dirname(__file__), 'arcadeclassic')
snd_dir = path.join(path.dirname(__file__), 'snd')


class TypeNameWindow(pygame.sprite.Sprite):
    def __init__(self, size):
        pygame.sprite.Sprite.__init__(self)
        self.message = Caption('NEW HIGH SCORE', 60, size[0] / 2, 200)
        self.error_message = Caption('maximum size of name is 11', 20, size[0] / 2 - 85, 410)
        self.error_message.change_color((255, 0, 0))
        self.caption_input = Caption('INPUT NAME', 30, size[0] / 2 - 130, 300)
        self.input_text = ''
        self.input_rect = pygame.Rect(size[0] / 2 - 210, size[1] / 2 - 35, 350, 70)
        self.image = pygame.transform.scale(pygame.image.load(path.join(img_dir, 'pause.png')).convert(), (700, 500))
        self.rect = self.image.get_rect()
        self.rect.center = (size[0] / 2, size[1] / 2)
        self.button_ex = Button((370, 50), 'EXIT', self.rect.centerx, self.rect.centery + 150, 50)
        self.buttons = pygame.sprite.Group()
        self.buttons.add(self.button_ex)
        self.captions = pygame.sprite.Group()
        self.captions.add(self.button_ex.caption)
        self.captions.add(self.message)
        self.captions.add(self.caption_input)
        self.captions.add(self.input_text)

    def update(self, text):
        self.captions.remove(self.input_text)
        self.input_text = Caption(text, 50, self.input_rect.x + 14 * len(text), self.input_rect.y + 35)
        self.input_text.change_color((0, 0, 0))
        self.captions.add(self.input_text)


class ButtonEntry(pygame.sprite.Sprite):
    def __init__(self, size, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.centre = (x, y)
        self.image_off = pygame.transform.scale(pygame.image.load(path.join(img_dir, 'save_off.png')).convert(), size)
        self.image_on = pygame.transform.scale(pygame.image.load(path.join(img_dir, 'save_on.png')).convert(), size)
        self.state(False)

    def state(self, state):
        if state:
            self.image = self.image_on
        else:
            self.image = self.image_off
        self.rect = self.image.get_rect()
        self.rect.center = self.centre


def check_amount_of_scores(tab):
    if len(tab) >= 6:
        min_scores = []
        for i in tab.values():
            min_scores.append(int(i[0]))
        min_score = min(min_scores)
        for key, value in tab.items():
            print(key)
            print(value)
            if value[0] == str(min_score):
                temp_key = key
        tab.pop(temp_key)
    return tab


def typename(screen, score, wave, table):
    input_name = ''
    buttons = TypeNameWindow(screen.get_size())
    savebutton = ButtonEntry((70, 70), buttons.input_rect.right + 30, buttons.input_rect.centery)
    menu = pygame.sprite.Group()
    menu.add(buttons)
    menu.add(savebutton)
    running = True
    while running:
        xm, ym = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if buttons.button_ex.rect.collidepoint((xm, ym)):
                    return
                if savebutton.rect.collidepoint((xm, ym)):
                    one_record = {input_name: (score, wave)}
                    table.update(one_record)
                    table = check_amount_of_scores(table)
                    save_to_file(table)
                    return
            elif event.type == pygame.MOUSEMOTION:
                if buttons.button_ex.rect.collidepoint((xm, ym)):
                    buttons.button_ex.state(True)
                else:
                    buttons.button_ex.state(False)
                if savebutton.rect.collidepoint((xm, ym)):
                    savebutton.state(True)
                else:
                    savebutton.state(False)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    input_name = input_name[:-1]
                else:
                    if len(input_name) > 10:
                        buttons.buttons.add(buttons.error_message)
                    else:
                        buttons.buttons.remove(buttons.error_message)
                        input_name += event.unicode

        buttons.buttons.update()
        buttons.update(input_name)
        menu.draw(screen)
        buttons.buttons.draw(screen)
        pygame.draw.rect(screen, WHITE, buttons.input_rect)
        buttons.captions.draw(screen)
        pygame.display.flip()
    pygame.quit()
