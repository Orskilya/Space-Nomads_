import ctypes
import sys
import Ships
import Objects
import os
import pygame
import Equipments
from random import randrange
from math import radians
import Hero


class Camera:
    def __init__(self):
        self.dx = -(AU * 1.7 + 750)
        self.dy = 0

    def apply(self, obj):
        if str(obj) == 'Планета':
            obj.center[0] = sun.rect.x + sun.size[0] // 2
            obj.center[1] = sun.rect.y + sun.size[1] // 2
        elif sprite == bg:
            if self.dx < 0:
                obj.rect.x += -((-self.dx) // 3)
            else:
                obj.rect.x += self.dx // 3
            if self.dy < 0:
                obj.rect.y += -((-self.dy) // 3)
            else:
                obj.rect.y += self.dy // 3
        elif str(sprite) == 'Пуля':
            obj.start_point[0] += self.dx
            obj.start_point[1] += self.dy
        elif str(obj) == 'Кристалид':
            if not obj.first:
                obj.start_point[0] += self.dx
                obj.start_point[1] += self.dy
            obj.rect.x += self.dx
            obj.rect.y += self.dy
        else:
            obj.rect.x += self.dx
            obj.rect.y += self.dy

    def update(self, target):
        self.dx = target.dx
        self.dy = target.dy

    def stop_move(self):
        self.dx = 0
        self.dy = 0


def quit():
    pygame.quit()
    sys.exit()


def load_image(name, size_of_sprite=None, color_key=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    if size_of_sprite:
        image = pygame.transform.scale(image, (size_of_sprite[0], size_of_sprite[1]))
    if color_key is not None:
        image = image.convert()
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


class Landing:
    global WIDTH, HEIGHT, FPS, LANGUAGE, hero

    def __init__(self):
        self.font = pygame.font.SysFont('Arialms', 29)
        self.current_window = 'government'
        self.current_song = pygame.mixer.Sound('soundtracks/planet.mp3')
        self.new_game = True
        self.text = self.font.render('Press "Space" to land', True, pygame.Color('Yellow'))
        self.object = None
        self.button_type = None
        self.market_buttons = None

    def planet_collide(self):
        for sprite in planets:
            if pygame.sprite.collide_mask(hero.ship, sprite):
                screen.blit(self.text, (WIDTH * 0.42, HEIGHT * 0.507))
                return sprite
        if pygame.sprite.collide_mask(hero.ship, station):
            screen.blit(self.text, (WIDTH * 0.43, HEIGHT * 0.507))
            return station

    def cycle(self, object):
        self.object = object
        if str(self.object) == 'station':
            self.bg_names = ('government_st', 'station_bg')
            self.current_song = pygame.mixer.Sound('soundtracks/station.mp3')
            self.song_play = True
        else:
            self.bg_names = ('government', 'planet_bg')
            self.current_song = pygame.mixer.Sound('soundtracks/planet.mp3')
            self.song_play = True
        if self.new_game:
            self.current_bg = self.bg_names[0]
            self.new_game = False
        else:
            self.current_bg = self.bg_names[1]
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # button push
                    pos = event.pos
                    if HEIGHT * 0.9 <= pos[1] <= HEIGHT:
                        if WIDTH * 0.5 - 2 * WIDTH * 0.055 <= pos[0] <= WIDTH * 0.5 - WIDTH * 0.055:
                            self.current_window = 'government'
                            self.current_bg = self.bg_names[0]
                        elif WIDTH * 0.5 - WIDTH * 0.055 <= pos[0] <= WIDTH * 0.5:
                            self.current_window = 'shop'
                            self.current_bg = self.bg_names[1]
                        elif WIDTH * 0.5 <= pos[0] <= WIDTH * 0.5 + WIDTH * 0.055:
                            self.current_window = 'market'
                            self.current_bg = self.bg_names[1]
                        elif WIDTH * 0.5 - WIDTH * 0.055 <= pos[
                            0] <= WIDTH * 0.5 + 2 * WIDTH * 0.055:
                            self.current_window = 'main'
                            self.current_bg = self.bg_names[1]
                            self.button_type = None
                            self.current_song.stop()
                            return True  # undocking
                if event.type == pygame.MOUSEMOTION:
                    pos = event.pos
                    if HEIGHT - 100 <= pos[1] <= HEIGHT:
                        if WIDTH * 0.5 - 2 * WIDTH * 0.055 <= pos[0] <= WIDTH * 0.5 - WIDTH * 0.055:
                            self.button_type = (WIDTH * 0.5 - 2 * WIDTH * 0.055, HEIGHT * 0.85, 0)
                        elif WIDTH * 0.5 - WIDTH * 0.055 <= pos[0] <= WIDTH * 0.5:
                            self.button_type = (WIDTH * 0.5 - WIDTH * 0.055, HEIGHT * 0.85, 1)
                        elif WIDTH * 0.5 <= pos[0] <= WIDTH * 0.5 + WIDTH * 0.055:
                            self.button_type = (WIDTH * 0.5, HEIGHT * 0.85, 2)
                        elif WIDTH * 0.5 - WIDTH * 0.055 <= pos[
                            0] <= WIDTH * 0.5 + 2 * WIDTH * 0.055:
                            self.button_type = (WIDTH * 0.5 + WIDTH * 0.055, HEIGHT * 0.85, 3)
                        else:
                            self.button_type = None
                    else:
                        self.button_type = None
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.market_buttons:
                    pos = event.pos
                    if self.market_buttons['x'][0][0] <= pos[0] <= self.market_buttons['x'][0][1]:
                        if self.market_buttons['y'][0] <= pos[1] <= self.market_buttons['y'][1] or \
                                self.market_buttons['y'][0] + self.market_buttons['y_step'] <= pos[
                            1] <= self.market_buttons['y'][1] + self.market_buttons['y_step'] or \
                                self.market_buttons['y'][0] + 2 * self.market_buttons['y_step'] <= \
                                pos[
                                    1] <= self.market_buttons['y'][1] + 2 * self.market_buttons[
                            'y_step'] or \
                                self.market_buttons['y'][0] + 3 * self.market_buttons['y_step'] <= \
                                pos[
                                    1] <= self.market_buttons['y'][1] + 3 * self.market_buttons[
                            'y_step'] or \
                                self.market_buttons['y'][0] + 4 * self.market_buttons['y_step'] <= \
                                pos[
                                    1] <= self.market_buttons['y'][1] + 4 * self.market_buttons[
                            'y_step'] or \
                                self.market_buttons['y'][0] + 5 * self.market_buttons['y_step'] <= \
                                pos[
                                    1] <= self.market_buttons['y'][1] + 5 * self.market_buttons[
                            'y_step'] or \
                                self.market_buttons['y'][0] + 6 * self.market_buttons['y_step'] <= \
                                pos[
                                    1] <= self.market_buttons['y'][1] + 6 * self.market_buttons[
                            'y_step']:
                            print(1)
                    elif self.market_buttons['x'][1][0] <= pos[0] <= self.market_buttons['x'][1][1]:
                        if self.market_buttons['y'][0] <= pos[1] <= self.market_buttons['y'][1] or \
                                self.market_buttons['y'][0] + self.market_buttons['y_step'] <= pos[
                            1] <= self.market_buttons['y'][1] + self.market_buttons['y_step'] or \
                                self.market_buttons['y'][0] + 2 * self.market_buttons['y_step'] <= \
                                pos[
                                    1] <= self.market_buttons['y'][1] + 2 * self.market_buttons[
                            'y_step'] or \
                                self.market_buttons['y'][0] + 3 * self.market_buttons['y_step'] <= \
                                pos[
                                    1] <= self.market_buttons['y'][1] + 3 * self.market_buttons[
                            'y_step'] or \
                                self.market_buttons['y'][0] + 4 * self.market_buttons['y_step'] <= \
                                pos[
                                    1] <= self.market_buttons['y'][1] + 4 * self.market_buttons[
                            'y_step'] or \
                                self.market_buttons['y'][0] + 5 * self.market_buttons['y_step'] <= \
                                pos[
                                    1] <= self.market_buttons['y'][1] + 5 * self.market_buttons[
                            'y_step'] or \
                                self.market_buttons['y'][0] + 6 * self.market_buttons['y_step'] <= \
                                pos[
                                    1] <= self.market_buttons['y'][1] + 6 * self.market_buttons[
                            'y_step']:
                            print(2)
            if self.song_play:
                self.current_song.play()
                self.song_play = False
            self.update_window(self.button_type)
            pygame.display.flip()
            clock.tick(FPS)

    def update_window(self, button_type):
        bg = pygame.transform.scale(load_image(self.current_bg + '.png'), SIZE)
        screen.blit(bg, (0, 0))

        # buttons, money and space
        pygame.draw.rect(screen, pygame.Color('#FFFFFF'),
                         (WIDTH * 0.6, HEIGHT * 0.94, WIDTH * 0.4, HEIGHT * 0.2), 0)
        pygame.draw.rect(screen, pygame.Color('#04859D'),
                         (WIDTH * 0.6, HEIGHT * 0.945, WIDTH * 0.4, HEIGHT * 0.2), 0)
        # money
        pygame.draw.rect(screen, pygame.Color('#000000'),
                         (WIDTH * 0.75, HEIGHT * 0.958, WIDTH * 0.07, HEIGHT * 0.03), 0,
                         border_radius=100)
        font = pygame.font.SysFont('Arialms', 20)
        money_img = load_image('money.png', (20, 20))
        screen.blit(money_img, (WIDTH * 0.754, HEIGHT * 0.9595))
        screen.blit(font.render(str(hero.get_money()), True, pygame.Color('white')),
                    (WIDTH * 0.77, HEIGHT * 0.956))
        # space
        pygame.draw.rect(screen, pygame.Color('#000000'),
                         (WIDTH * 0.83, HEIGHT * 0.958, WIDTH * 0.05, HEIGHT * 0.03), 0,
                         border_radius=100)
        space_img = load_image('cube.png', (20, 20))
        screen.blit(space_img, (WIDTH * 0.834, HEIGHT * 0.9595))
        screen.blit(font.render(str(hero.get_ship().get_space()), True, pygame.Color('white')),
                    (WIDTH * 0.85, HEIGHT * 0.956))

        pygame.draw.ellipse(screen, pygame.Color('#FFFFFF'),
                            (WIDTH * 0.27, HEIGHT * 0.88, WIDTH * 0.44, HEIGHT * 0.25), 0)
        pygame.draw.ellipse(screen, pygame.Color('#04859D'),
                            (WIDTH * 0.28, HEIGHT * 0.89, WIDTH * 0.44, HEIGHT * 0.25), 0)
        buttons = [pygame.transform.scale(load_image('government_icon.png'),
                                          (WIDTH * 0.055, WIDTH * 0.055)),
                   pygame.transform.scale(load_image('shop_icon.png'),
                                          (WIDTH * 0.055, WIDTH * 0.055)),
                   pygame.transform.scale(load_image('market_icon.png'),
                                          (WIDTH * 0.055, WIDTH * 0.055)),
                   pygame.transform.scale(load_image('undocking_icon.png'),
                                          (WIDTH * 0.055, WIDTH * 0.055))]

        button_cord_x = WIDTH * 0.5 - 200
        for button in buttons:
            screen.blit(button, (button_cord_x, HEIGHT * 0.9))
            button_cord_x += 100

        if self.current_window != 'main':
            eval('self.' + self.current_window + '()')

        if button_type:
            pygame.draw.rect(screen, pygame.Color('#FFFFFF'),
                             (button_type[0], button_type[1], WIDTH * 0.128, HEIGHT * 0.05),
                             border_radius=50)
            pygame.draw.rect(screen, pygame.Color('#04859D'),
                             (button_type[0] + 5, button_type[1] + 5, WIDTH * 0.128 - 10,
                              HEIGHT * 0.05 - 10), border_radius=50)

            with open(f'data/ico_text {LANGUAGE}.txt', 'r', encoding='utf-8') as f:
                text = list(map(lambda x: x.rstrip(), f.readlines()))

            screen.blit(self.font.render(text[button_type[2]], True, pygame.Color('White')),
                        (button_type[0] + 10, button_type[1]))

    def government(self):
        with open(f'data/Dialog planets {LANGUAGE}.txt', 'r', encoding='utf-8') as f:
            text = map(lambda x: x.rstrip, f.readlines())

        pygame.draw.rect(screen, pygame.Color('#C8DFE3'),
                         (WIDTH * 0.06, HEIGHT * 0.06, WIDTH * 0.381, HEIGHT * 0.77))
        pygame.draw.line(screen, pygame.Color('Blue'), (WIDTH * 0.06, HEIGHT * 0.65),
                         (WIDTH * 0.44, HEIGHT * 0.65), 5)
        frame = pygame.transform.scale(load_image('frame.png'), (WIDTH * 0.4, HEIGHT * 1.1))
        screen.blit(frame, (WIDTH * 0.05, - HEIGHT * 0.1))

    def shop(self):
        pygame.draw.rect(screen, pygame.Color('#04859D'),
                         (WIDTH * 0.1, HEIGHT * 0.2, WIDTH * 0.8, HEIGHT * 0.6), border_radius=30)
        pygame.draw.rect(screen, pygame.Color('#C8DFE3'),
                         (WIDTH * 0.11, HEIGHT * 0.22, WIDTH * 0.779, HEIGHT * 0.56),
                         border_radius=30)
        pygame.draw.rect(screen, pygame.Color('#333333'),
                         (WIDTH * 0.1101, HEIGHT * 0.2201, WIDTH * 0.779, HEIGHT * 0.56), 3,
                         border_radius=30)

        equipment = self.object.get_shop()
        x_position = WIDTH * 0.12
        y_position = HEIGHT * 0.25
        for type in equipment:
            for i in type:
                screen.blit(load_image(i.get_img(), (100, 100), -1), (x_position, y_position))
                if x_position + WIDTH * 0.1 > WIDTH * 0.9:
                    x_position = WIDTH * 0.12
                    y_position += HEIGHT * 0.15
                else:
                    x_position += WIDTH * 0.1

    def market(self):
        self.market_buttons = {'x': ((WIDTH * 0.55, WIDTH * 0.62), (WIDTH * 0.63, WIDTH * 0.7)),
                               'y': (HEIGHT * 0.25, HEIGHT * 0.29),
                               'y_step': WIDTH * 0.05}
        button_names = {'EN': 'Buy', 'RU': 'Купить', 'KR': '구입'}
        button_names_2 = {'EN': 'Sell', 'RU': 'Продать', 'KR': '팔다'}

        # shop bg
        pygame.draw.rect(screen, pygame.Color('#04859D'),
                         (WIDTH * 0.28, HEIGHT * 0.15, WIDTH * 0.44, HEIGHT * 0.69),
                         border_radius=30)
        pygame.draw.rect(screen, pygame.Color('#C8DFE3'),
                         (WIDTH * 0.29, HEIGHT * 0.17, WIDTH * 0.42, HEIGHT * 0.65),
                         border_radius=30)
        pygame.draw.rect(screen, pygame.Color('#333333'),
                         (WIDTH * 0.2901, HEIGHT * 0.1701, WIDTH * 0.42, HEIGHT * 0.65), 3,
                         border_radius=30)

        # buy-sell buttons
        y_position = HEIGHT * 0.25
        for _ in range(6):
            pygame.draw.rect(screen, pygame.Color('#04859D'),
                             (WIDTH * 0.55, y_position, WIDTH * 0.07, HEIGHT * 0.04),
                             border_radius=100)
            text = self.font.render(button_names[LANGUAGE], True, pygame.Color('white'))
            screen.blit(text, (WIDTH * 0.56, y_position))

            pygame.draw.rect(screen, pygame.Color('#04859D'),
                             (WIDTH * 0.63, y_position, WIDTH * 0.075, HEIGHT * 0.04),
                             border_radius=100)
            text = self.font.render(button_names_2[LANGUAGE], True, pygame.Color('white'))
            screen.blit(text, (WIDTH * 0.64, y_position))
            y_position += WIDTH * 0.05

        #  icons and prices
        y_position = HEIGHT * 0.25
        products = self.object.products()
        for product in products:
            product_icon = pygame.transform.scale(load_image(product + '_icon.png'),
                                                  (WIDTH * 0.032, WIDTH * 0.032))
            screen.blit(product_icon, (WIDTH * 0.31, y_position))

            x_position = WIDTH * 0.38
            flag = True
            for price in products[product]:
                string_rendered = self.font.render(str(price), True, pygame.Color('black'))
                if flag:
                    string_len = string_rendered.get_width()
                    flag = False
                screen.blit(string_rendered, (x_position, y_position))
                x_position += WIDTH * 0.04 + string_len

            y_position += WIDTH * 0.05

        with open(f'data/market {LANGUAGE}.txt', 'r', encoding='utf-8') as f:
            text = map(lambda x: x.rstrip(), f.readlines())

        if LANGUAGE == 'KR':
            x_position = WIDTH * 0.39
        else:
            x_position = WIDTH * 0.35
        a = 1
        for word in text:
            string_rendered = self.font.render(word, True, pygame.Color('black'))
            screen.blit(string_rendered, (x_position, HEIGHT * 0.2))
            if a == 2:
                space = self.font.render('buy', True, pygame.Color('black'))
                x_position += WIDTH * 0.04 + space.get_width()
            else:
                x_position += WIDTH * 0.04 + string_rendered.get_width()

            a += 1


class Lobby:
    def __init__(self):
        self.buttons_type = 'Main Menu'
        self.bg = pygame.transform.scale(load_image('lobby_bg.png'), SIZE)
        screen.blit(self.bg, (0, 0))

        self.update_window()
        self.cycle()

    def cycle(self):
        global FPS, LANGUAGE
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # button push
                    pos = event.pos
                    if 250 >= pos[0] >= 30:
                        if self.buttons_type == 'Main Menu':
                            if HEIGHT * 0.3 <= pos[1] <= HEIGHT * 0.3 + self.buttons.height:
                                self.ent()  # start new game
                                return
                            elif HEIGHT * 0.3 + self.buttons.height + 15 <= pos[1] \
                                    <= HEIGHT * 0.3 + 2 * self.buttons.height + 15:
                                return  # continue last save
                            elif HEIGHT * 0.3 + 2 * self.buttons.height + 30 <= pos[1] \
                                    <= HEIGHT * 0.3 + 3 * self.buttons.height + 30:
                                self.buttons_type = 'Options'
                                self.update_window()
                            elif HEIGHT * 0.3 + 3 * self.buttons.height + 45 <= pos[1] \
                                    <= HEIGHT * 0.3 + 4 * self.buttons.height + 45:
                                pass
                            elif HEIGHT * 0.3 + 4 * self.buttons.height + 60 <= pos[1] \
                                    <= HEIGHT * 0.3 + 5 * self.buttons.height + 60:
                                quit()
                        elif self.buttons_type == 'Options':
                            if HEIGHT * 0.3 + self.buttons.height + 15 <= pos[1] \
                                    <= HEIGHT * 0.3 + 2 * self.buttons.height + 15:
                                LANGUAGE = 'KR'
                                self.update_window()
                            elif HEIGHT * 0.3 + 2 * self.buttons.height + 30 <= pos[1] \
                                    <= HEIGHT * 0.3 + 3 * self.buttons.height + 30:
                                LANGUAGE = 'EN'
                                self.update_window()
                            elif HEIGHT * 0.3 + 3 * self.buttons.height + 45 <= pos[1] \
                                    <= HEIGHT * 0.3 + 4 * self.buttons.height + 45:
                                LANGUAGE = 'RU'
                                self.update_window()
                            elif HEIGHT * 0.3 + 4 * self.buttons.height + 60 <= pos[1] \
                                    <= HEIGHT * 0.3 + 5 * self.buttons.height + 60:
                                self.buttons_type = 'Main Menu'
                                self.update_window()
                elif event.type == pygame.MOUSEMOTION:  # changing color of the button
                    pos = event.pos
                    if 250 >= pos[0] >= 30:
                        if self.buttons_type == 'Main Menu':
                            if HEIGHT * 0.3 <= pos[1] <= HEIGHT * 0.3 + self.buttons.height:
                                self.update_window(1)
                            elif HEIGHT * 0.3 + self.buttons.height + 15 <= pos[1] \
                                    <= HEIGHT * 0.3 + 2 * self.buttons.height + 15:
                                self.update_window(2)
                            elif HEIGHT * 0.3 + 2 * self.buttons.height + 30 <= pos[1] \
                                    <= HEIGHT * 0.3 + 3 * self.buttons.height + 30:
                                self.update_window(3)
                            elif HEIGHT * 0.3 + 3 * self.buttons.height + 45 <= pos[1] \
                                    <= HEIGHT * 0.3 + 4 * self.buttons.height + 45:
                                self.update_window(4)
                            elif HEIGHT * 0.3 + 4 * self.buttons.height + 60 <= pos[1] \
                                    <= HEIGHT * 0.3 + 5 * self.buttons.height + 60:
                                self.update_window(5)
                            else:
                                self.update_window()
                        elif self.buttons_type == 'Options':
                            if HEIGHT * 0.3 + self.buttons.height + 15 <= pos[1] \
                                    <= HEIGHT * 0.3 + 2 * self.buttons.height + 15:
                                self.update_window(2)
                            elif HEIGHT * 0.3 + 2 * self.buttons.height + 30 <= pos[1] \
                                    <= HEIGHT * 0.3 + 3 * self.buttons.height + 30:
                                self.update_window(3)
                            elif HEIGHT * 0.3 + 3 * self.buttons.height + 45 <= pos[1] \
                                    <= HEIGHT * 0.3 + 4 * self.buttons.height + 45:
                                self.update_window(4)
                            elif HEIGHT * 0.3 + 4 * self.buttons.height + 60 <= pos[1] \
                                    <= HEIGHT * 0.3 + 5 * self.buttons.height + 60:
                                self.update_window(5)
                            else:
                                self.update_window()
                    else:
                        self.update_window()

            pygame.display.flip()
            clock.tick(FPS)

    def update_window(self, current_button=None):  # rendering
        global LANGUAGE, HEIGHT
        screen.fill((0, 0, 0))
        screen.blit(self.bg, (0, 0))
        font = pygame.font.SysFont('Arialms', 50)

        with open(f'data/{self.buttons_type} {LANGUAGE}.txt', 'r', encoding='utf-8') as f:
            self.buttons = map(lambda x: x.rstrip(), f.readlines())

        self.text_coord = HEIGHT * 0.3
        button = 1
        for line in self.buttons:
            if current_button == button:
                string_rendered = font.render(line, True, pygame.Color('yellow'))
                current_button = None
            else:
                string_rendered = font.render(line, True, pygame.Color('white'))
            self.buttons = string_rendered.get_rect()
            self.text_coord += 10
            self.buttons.top = self.text_coord
            self.buttons.x = 30
            self.text_coord += self.buttons.height
            screen.blit(string_rendered, self.buttons)
            button += 1

    def ent(self):
        global LANGUAGE, FPS, WIDTH, HEIGHT
        self.bg = pygame.transform.scale(load_image('ent_bg.png'), SIZE)
        screen.fill((0, 0, 0))
        screen.blit(self.bg, (0, 0))
        font = pygame.font.SysFont('Arialms', 40)

        with open(f'data/ENT {LANGUAGE}.txt', 'r', encoding='utf-8') as f:
            start_game = f.readline().rstrip()
            self.buttons = map(lambda x: x.rstrip(), f.readlines())

        self.text_coord = HEIGHT * 0.15
        button = 1
        for line in self.buttons:
            string_rendered = font.render(line, True, pygame.Color('white'))
            self.buttons = string_rendered.get_rect()
            self.text_coord += 10
            self.buttons.top = self.text_coord
            self.buttons.x = 30
            self.text_coord += self.buttons.height
            screen.blit(string_rendered, self.buttons)
            button += 1

        screen.blit(font.render(start_game, True, pygame.Color('white')),
                    (WIDTH * 0.3, HEIGHT * 0.9))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    return
            pygame.display.flip()
            clock.tick(FPS)


def mini_map():
    pygame.draw.rect(screen, pygame.Color('black'), (WIDTH * 0.9, 0, WIDTH * 0.1, WIDTH * 0.1))
    pygame.draw.rect(screen, pygame.Color('#04859D'), (WIDTH * 0.9, 0, WIDTH * 0.1, WIDTH * 0.1), 3)


# PG
FPS = 60
LANGUAGE = 'EN'
AU = 815
pygame.init()
user32 = ctypes.windll.user32
SIZE = WIDTH, HEIGHT = user32.GetSystemMetrics(0) - 100, user32.GetSystemMetrics(1) - 100
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()
song = pygame.mixer.Sound('soundtracks/space_theme.mp3')

# lobby
lobby = Lobby()
landing = Landing()

# Группы спрайтов
all_sprites = pygame.sprite.Group()
planets = pygame.sprite.Group()
ships = pygame.sprite.Group()
stations = pygame.sprite.Group()
enemy = pygame.sprite.Group()
hero_group = pygame.sprite.Group()
camera = Camera()

# Объекты
bg = pygame.sprite.Sprite()
bg.image = pygame.transform.scale(load_image('Space Background.png'), (9000, 9000))
bg.rect = bg.image.get_rect()
all_sprites.add(bg)
bg.rect.x = bg.rect.x = -4500 + (AU * 1.7 + 750) // 2
bg.rect.y = -4500

sun = Objects.Star(load_image('Sun.png'), 25, 10, [1500, 1500], [WIDTH // 2, HEIGHT // 2],
                   all_sprites)
mercury = Objects.Planet(load_image('Mercury.png'), 50, 5, [80, 80], [WIDTH // 2, HEIGHT // 2],
                         AU * 0.387 + 750, 100, radians(randrange(0, 360)), all_sprites, planets)
venus = Objects.Planet(load_image('Venus.png'), 50, 5, [260, 260], [WIDTH // 2, HEIGHT // 2],
                       AU * 0.9 + 750, 100, radians(randrange(0, 360)), all_sprites, planets)
earth = Objects.Planet(load_image('Earth.png'), 50, 5, [280, 280], [WIDTH // 2, HEIGHT // 2],
                       AU * 1.7 + 750, 100, 0, all_sprites, planets)
mars = Objects.Planet(load_image('Mars.png'), 50, 5, [170, 170], [WIDTH // 2, HEIGHT // 2],
                      AU * 2.5 + 750, 100, radians(randrange(0, 360)), all_sprites, planets)
jupiter = Objects.Planet(load_image('Jupiter.png'), 50, 5, [400, 400], [WIDTH // 2, HEIGHT // 2],
                         AU * 5.2 + 750, 100, radians(randrange(0, 360)), all_sprites, planets)
saturn = Objects.Planet(load_image('Saturn.png'), 25, 10, [800, 800], [WIDTH // 2, HEIGHT // 2],
                        AU * 8.2, 100, radians(randrange(0, 360)), all_sprites, planets)
uranus = Objects.Planet(load_image('Uranus.png'), 50, 5, [220, 220], [WIDTH // 2, HEIGHT // 2],
                        AU * 9 + 750, 100, radians(randrange(0, 360)), all_sprites, planets)
neptune = Objects.Planet(load_image('Neptune.png'), 50, 5, [200, 200], [WIDTH // 2, HEIGHT // 2],
                         AU * 11 + 750, 100, radians(randrange(0, 360)), all_sprites, planets)
station = Objects.Station(load_image('Station.png', color_key=-1), 1, 1, [760, 525],
                          [AU * 5.2 + 750, HEIGHT // 2], all_sprites, stations)
hero = Hero.Hero(
    Ships.NomadShip(load_image('Nomad_ship_fly.png', (64, 64)), [WIDTH // 2, HEIGHT // 2],
                    500, 100, [Equipments.PhotonGun(3, (enemy, all_sprites),
                                                    load_image('photon_bullet.png', (50, 50))),
                               Equipments.Engine(3), ],
                    camera,
                    SIZE, all_sprites, ships, hero_group), 1000000, None)
kristalids = []
for sprite in all_sprites:
    if sprite != hero.ship:
        camera.apply(sprite)
camera.stop_move()

# main cycle
running = True
song_p = True
while running:
    while len(kristalids) != 20:
        spawn_coord = [randrange(-9700, 9700), randrange(-9700, 9700)]
        if (spawn_coord[0] >= AU * 2.5 + 750 or spawn_coord[0] <= -(AU * 2.5 + 750)) and (
                spawn_coord[1] <= -(AU * 2.5 + 750) or spawn_coord[1] <= -(AU * 2.5 + 750)):
            kristalids.append(Ships.Kristalid(load_image('Kristalid_ship.png', (150, 150), -1),
                                              spawn_coord,
                                              100, 100, [
                                                  Equipments.PhotonGun(0, (enemy, all_sprites),
                                                                       load_image(
                                                                           'photon_bullet.png',
                                                                           (50, 50)))],
                                              all_sprites, ships, enemy))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            if event.key == pygame.K_w or event.key == pygame.K_a or event.key == pygame.K_s or \
                    event.key == pygame.K_d:
                hero.ship.update(event, 'fly')
            elif landing.planet_collide() and event.key == pygame.K_SPACE:
                hero.ship.keys.clear()
                song.stop()
                song_p = landing.cycle(landing.planet_collide())
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            hero.ship.update(event, 'shoot')
    screen.fill((0, 0, 0))
    all_sprites.update(hero_coord=[hero.ship.rect.x, hero.ship.rect.y])
    for sprite in all_sprites:
        if sprite != hero.ship:
            camera.apply(sprite)
    if song_p:
        song.play()
        song_p = False
    camera.stop_move()
    all_sprites.draw(screen)
    landing.planet_collide()
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
