import ctypes
import sys
import Ships
import Objects
import os
import pygame
import pygame.gfxdraw
import Equipments
from random import randrange
from math import radians
import Hero
import sqlite3


class Camera:
    def __init__(self):
        self.dx = -(AU * 1.7 + 750)
        self.dy = 0

    def apply(self, obj):
        if str(obj) == 'Планета':
            obj.center[0] = sun.rect.x + sun.size[0] // 2
            obj.center[1] = sun.rect.y + sun.size[1] // 2
        elif obj == bg:
            if self.dx < 0:
                obj.rect.x += -((-self.dx) // 3)
            else:
                obj.rect.x += self.dx // 3
            if self.dy < 0:
                obj.rect.y += -((-self.dy) // 3)
            else:
                obj.rect.y += self.dy // 3
        elif str(obj) == 'Пуля':
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
    global WIDTH, HEIGHT, FPS, LANGUAGE, hero, TRANSLATOR

    def __init__(self):
        self.font = pygame.font.SysFont('Arialms', 29)
        self.current_window = 'government'
        self.current_song = pygame.mixer.Sound('soundtracks/planet.mp3')
        self.new_game = True
        self.text = self.font.render('Press "Space" to land', True, pygame.Color('Yellow'))
        self.object = None
        self.button_type = None
        self.market_buttons = None
        self.shop_buttons = None
        self.shop_info = None
        self.government_buttons = None
        self.repairing = None
        self.wait = None
        self.government_design = None

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
            self.current_song = pygame.mixer.Sound('soundtracks/Coolio.mp3')
            self.song_play = True
        if self.new_game:
            self.current_bg = self.bg_names[0]
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
                            self.new_game = False
                            self.current_bg = self.bg_names[0]
                            self.market_buttons = None
                            self.shop_buttons = None
                            self.shop_info = None
                            self.repairing = None
                            self.wait = None
                            self.government_design = None
                        elif WIDTH * 0.5 - WIDTH * 0.055 <= pos[0] <= WIDTH * 0.5:
                            self.current_window = 'shop'
                            self.new_game = False
                            self.current_bg = self.bg_names[1]
                            self.government_buttons = None
                            self.market_buttons = None
                            self.shop_info = None
                            self.repairing = None
                            self.wait = None
                            self.government_design = None
                        elif WIDTH * 0.5 <= pos[0] <= WIDTH * 0.5 + WIDTH * 0.055:
                            self.current_window = 'market'
                            self.new_game = False
                            self.current_bg = self.bg_names[1]
                            self.government_buttons = None
                            self.shop_buttons = None
                            self.shop_info = None
                            self.repairing = None
                            self.wait = None
                            self.government_design = None
                        elif WIDTH * 0.5 - WIDTH * 0.055 <= pos[
                            0] <= WIDTH * 0.5 + 2 * WIDTH * 0.055:
                            self.current_window = 'main'
                            self.new_game = False
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
                if event.type == pygame.MOUSEBUTTONDOWN and \
                        event.button == 1 and self.market_buttons:
                    pos = event.pos
                    if self.market_buttons['x'][0][0] <= pos[0] <= self.market_buttons['x'][0][1]:
                        if self.market_buttons['y'][0] <= pos[1] <= self.market_buttons['y'][1]:
                            self.market_operations('product')
                        elif self.market_buttons['y'][0] + self.market_buttons['y_step'] <= pos[1] <= \
                                self.market_buttons['y'][1] + self.market_buttons['y_step']:
                            self.market_operations('medicine')
                        elif self.market_buttons['y'][0] + 2 * self.market_buttons['y_step'] <= pos[
                            1] <= self.market_buttons['y'][1] + 2 * self.market_buttons['y_step']:
                            self.market_operations('alchogol')
                        elif self.market_buttons['y'][0] + 3 * self.market_buttons['y_step'] <= pos[
                            1] <= self.market_buttons['y'][1] + 3 * self.market_buttons['y_step']:
                            self.market_operations('luxury')
                        elif self.market_buttons['y'][0] + 4 * self.market_buttons['y_step'] <= pos[
                            1] <= self.market_buttons['y'][1] + 4 * self.market_buttons['y_step']:
                            self.market_operations('tech')
                        elif self.market_buttons['y'][0] + 5 * self.market_buttons['y_step'] <= pos[
                            1] <= self.market_buttons['y'][1] + 5 * self.market_buttons['y_step']:
                            self.market_operations('weapon')
                    elif self.market_buttons['x'][1][0] <= pos[0] <= self.market_buttons['x'][1][1]:
                        if self.market_buttons['y'][0] <= pos[1] <= self.market_buttons['y'][1]:
                            self.market_operations('product', True)
                        elif self.market_buttons['y'][0] + self.market_buttons['y_step'] <= pos[1] <= \
                                self.market_buttons['y'][1] + self.market_buttons['y_step']:
                            self.market_operations('medicine', True)
                        elif self.market_buttons['y'][0] + 2 * self.market_buttons['y_step'] <= pos[
                            1] <= self.market_buttons['y'][1] + 2 * self.market_buttons['y_step']:
                            self.market_operations('alchogol', True)
                        elif self.market_buttons['y'][0] + 3 * self.market_buttons['y_step'] <= pos[
                            1] <= self.market_buttons['y'][1] + 3 * self.market_buttons['y_step']:
                            self.market_operations('luxury', True)
                        elif self.market_buttons['y'][0] + 4 * self.market_buttons['y_step'] <= pos[
                            1] <= self.market_buttons['y'][1] + 4 * self.market_buttons['y_step']:
                            self.market_operations('tech', True)
                        elif self.market_buttons['y'][0] + 5 * self.market_buttons['y_step'] <= pos[
                            1] <= self.market_buttons['y'][1] + 5 * self.market_buttons['y_step']:
                            self.market_operations('weapon', True)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.shop_buttons:
                    pos = event.pos
                    for row in self.shop_buttons.keys():
                        if self.shop_buttons[row]['y'][0] <= pos[1] <= self.shop_buttons[row]['y'][
                            1]:
                            for i in range(self.shop_buttons[row]['amount']):
                                if self.shop_buttons[row]['x'][0] + i * self.shop_buttons[row][
                                    'step'] <= pos[0] <= self.shop_buttons[row]['x'][1] + i * \
                                        self.shop_buttons[row]['step']:
                                    item = self.object.shopping(i + 8 * int(row[-1]))
                                    error = pygame.mixer.Sound('soundtracks/error.mp3')
                                    selling = pygame.mixer.Sound('soundtracks/selling.mp3')
                                    price, mass = item.get_price(), item.get_mass()
                                    if hero.buy(price, mass):
                                        selling.play()
                                        self.object.shop_change(i + 8 * int(row[-1]))
                                        hero.money_change(-price)
                                        hero.get_ship().change_space(mass,
                                                                     hero.get_ship().get_equipment(
                                                                         item.get_type()).get_mass())
                                    else:
                                        error.play()

                                    if str(item) in 'photon absorber destructor':
                                        item.set_bullet_img(
                                            load_image(str(item) + '_bullet.png', item.get_size(),
                                                       -1))
                                        item.set_groups(enemy, all_sprites)

                                    hero.get_ship().new_equipment(item)
                if event.type == pygame.MOUSEMOTION and self.shop_buttons:
                    pos = event.pos
                    flag = False
                    for row in self.shop_buttons.keys():
                        if flag:
                            break
                        if self.shop_buttons[row]['y'][0] <= pos[1] <= self.shop_buttons[row]['y'][
                            1]:
                            flag = True
                            for i in range(self.shop_buttons[row]['amount']):
                                if self.shop_buttons[row]['x'][0] + i * self.shop_buttons[row][
                                    'step'] <= pos[0] <= self.shop_buttons[row]['x'][1] + i * \
                                        self.shop_buttons[row]['step']:
                                    self.shop_info = [self.object.get_shop()[i + 8 * int(row[-1])], (
                                        self.shop_buttons[row]['x'][0] + i * self.shop_buttons[row][
                                            'step'], self.shop_buttons[row]['y'][0])]
                        else:
                            self.shop_info = None
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.government_buttons:
                    pos = event.pos
                    if WIDTH * 0.07 <= pos[0] <= WIDTH * 0.38:
                        if len(self.government_buttons) == 2:
                            if self.government_buttons[0][0] <= pos[1] <= self.government_buttons[0][
                                1]:
                                self.repairing = True
                            elif self.government_buttons[1][0] <= pos[1] <= \
                                    self.government_buttons[1][1]:
                                self.current_window = 'main'
                                self.new_game = False
                                self.current_bg = self.bg_names[1]
                        else:
                            if self.government_buttons[0][0] <= pos[1] <= self.government_buttons[0][
                                1]:
                                self.current_window = 'government'
                                self.repairing = False
                                self.new_game = False
                                self.current_bg = self.bg_names[0]
                                self.wait = False
                if event.type == pygame.MOUSEMOTION and self.government_buttons:
                    pos = event.pos
                    if WIDTH * 0.07 <= pos[0] <= WIDTH * 0.38:
                        if len(self.government_buttons) == 2:
                            if self.government_buttons[0][0] <= pos[1] <= self.government_buttons[0][
                                1]:
                                self.government_design = pygame.Rect(WIDTH * 0.06,
                                                                     HEIGHT * 0.665,
                                                                     WIDTH * 0.38, HEIGHT * 0.02)
                            elif self.government_buttons[1][0] <= pos[1] <= \
                                    self.government_buttons[1][1]:
                                self.government_design = pygame.Rect(WIDTH * 0.06,
                                                                     HEIGHT * 0.695,
                                                                     WIDTH * 0.38, HEIGHT * 0.02)
                            else:
                                self.government_design = None
                        else:
                            if self.government_buttons[0][0] <= pos[1] <= self.government_buttons[0][
                                1]:
                                self.government_design = pygame.Rect(WIDTH * 0.06,
                                                                     HEIGHT * 0.665,
                                                                     WIDTH * 0.38, HEIGHT * 0.02)
                            else:
                                self.government_design = None
                    else:
                        self.government_design = None

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
        font = pygame.font.SysFont('Arialms', 20)
        pygame.draw.rect(screen, pygame.Color('#C8DFE3'),
                         (WIDTH * 0.06, HEIGHT * 0.06, WIDTH * 0.381, HEIGHT * 0.77))
        pygame.draw.line(screen, pygame.Color('Blue'), (WIDTH * 0.06, HEIGHT * 0.65),
                         (WIDTH * 0.44, HEIGHT * 0.65), 5)
        if self.government_design:
            pygame.gfxdraw.box(screen, self.government_design, (100, 100, 100, 230))
        frame = pygame.transform.scale(load_image('frame.png'), (WIDTH * 0.4, HEIGHT * 1.1))
        screen.blit(frame, (WIDTH * 0.05, - HEIGHT * 0.1))

        if self.new_game:
            with open(f'data/Starting phrase {LANGUAGE}.txt', 'r', encoding='utf-8') as f:
                hero_text = (f.readline().rstrip(),)
                government_text = map(lambda x: x.rstrip(), f.readlines())
                self.government_buttons = ((HEIGHT * 0.66, HEIGHT * 0.69),)
        elif self.repairing:
            if hero.get_ship().get_hull() != 500:
                with open(f'data/repair {LANGUAGE}.txt', 'r', encoding='utf-8') as f:
                    hero_text = (f.readline().rstrip(),)
                    government_text = map(lambda x: x.rstrip(), f.readlines())
                    self.government_buttons = ((HEIGHT * 0.66, HEIGHT * 0.69),)
                    hero.get_ship().repair()
                    hero.money_change(-500)
                    self.wait = True
            elif self.wait:
                with open(f'data/repair {LANGUAGE}.txt', 'r', encoding='utf-8') as f:
                    hero_text = (f.readline().rstrip(),)
                    government_text = map(lambda x: x.rstrip(), f.readlines())
                    self.government_buttons = ((HEIGHT * 0.66, HEIGHT * 0.69),)
            else:
                with open(f'data/repair fall {LANGUAGE}.txt', 'r', encoding='utf-8') as f:
                    hero_text = (f.readline().rstrip(),)
                    government_text = (f.readline().rstrip(),)
                    self.government_buttons = ((HEIGHT * 0.66, HEIGHT * 0.69),)
        else:
            with open(f'data/Dialog planets {LANGUAGE}.txt', 'r', encoding='utf-8') as f:
                government_text = (f.readline().rstrip(),)
                hero_text = map(lambda x: x.rstrip(), f.readlines())
                self.government_buttons = ((HEIGHT * 0.66, HEIGHT * 0.69),
                                           (HEIGHT * 0.69, HEIGHT * 0.72))
        y_pos = HEIGHT * 0.13
        for line in government_text:
            string_render = font.render(line, True, pygame.Color('black'))
            screen.blit(string_render, (WIDTH * 0.07, y_pos))
            y_pos += HEIGHT * 0.03

        y_pos = HEIGHT * 0.66
        for line in hero_text:
            string_render = font.render(line, True, pygame.Color('black'))
            screen.blit(string_render, (WIDTH * 0.07, y_pos))
            y_pos += HEIGHT * 0.03

    def shop(self):
        self.shop_buttons = {
            'row0': {'x': (WIDTH * 0.12, WIDTH * 0.175),
                     'y': (HEIGHT * 0.25, HEIGHT * 0.25 + WIDTH * 0.055),
                     'step': WIDTH * 0.1, 'amount': 0}}
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
        row = 0
        for i in equipment:
            screen.blit(load_image(i.get_img(), (WIDTH * 0.055, WIDTH * 0.055), -1),
                        (x_position, y_position))
            if hero.get_money() >= i.get_price() and hero.get_ship().get_space() >= i.get_mass():
                color = pygame.Color('green')
            else:
                color = pygame.Color('red')
            pygame.draw.rect(screen, color, (
                x_position - 10, y_position - 10, WIDTH * 0.055 + 20, WIDTH * 0.055 + 20), 5)
            self.shop_buttons[f'row{row}']['amount'] += 1
            if x_position + WIDTH * 0.1 > WIDTH * 0.9:
                x_position = WIDTH * 0.12
                y_position += HEIGHT * 0.15
                row += 1
                self.shop_buttons[f'row{row}'] = {'x': (WIDTH * 0.12, WIDTH * 0.175),
                                                  'y': (y_position, y_position + WIDTH * 0.055),
                                                  'step': WIDTH * 0.1,
                                                  'amount': 0}
            else:
                x_position += WIDTH * 0.1

        if self.shop_info:
            font = pygame.font.SysFont('Arialms', 20)
            pygame.gfxdraw.box(screen,
                               pygame.Rect(self.shop_info[1][0] - 100, self.shop_info[1][1] - 100,
                                           300, 300), (51, 51, 51, 230))
            features = self.shop_info[0].get_features()
            step = 0
            for i in features:
                text = self.font.render(i + ' ' + str(features[i]), True, pygame.Color('white'))
                screen.blit(text, (self.shop_info[1][0] - 85, self.shop_info[1][1] + step))
                step += 30

            name = self.font.render(self.shop_info[0].get_name(), True, pygame.Color('white'))
            screen.blit(name, (self.shop_info[1][0] - 85, self.shop_info[1][1] - 85))
            screen.blit(load_image('money.png', (20, 20)),
                        (self.shop_info[1][0] + 50, self.shop_info[1][1] + 160))
            money = font.render(str(self.shop_info[0].get_price()), True, pygame.Color('white'))
            screen.blit(money, (self.shop_info[1][0] + 70, self.shop_info[1][1] + 155))
            screen.blit(load_image('cube.png', (20, 20)),
                        (self.shop_info[1][0] + 130, self.shop_info[1][1] + 160))
            mass = font.render(str(self.shop_info[0].get_mass()), True, pygame.Color('white'))
            screen.blit(mass, (self.shop_info[1][0] + 150, self.shop_info[1][1] + 155))

    def market(self):
        self.market_buttons = {'x': ((WIDTH * 0.55, WIDTH * 0.62), (WIDTH * 0.63, WIDTH * 0.7)),
                               'y': (HEIGHT * 0.25, HEIGHT * 0.29),
                               'y_step': WIDTH * 0.05}
        button_names = {'en': 'Buy', 'ru': 'Купить', 'ko': '구입'}
        button_names_2 = {'en': 'Sell', 'ru': 'Продать', 'ko': '팔다'}

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

        if LANGUAGE == 'ko':
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

    def market_operations(self, item, selling=False):
        if selling:
            hero.money_change(hero.get_ship().get_hold()[item] * self.object.get_market()[item][2])
            hero.get_ship().change_space(0, hero.get_ship().get_hold()[item])
            self.object.market_change(item, hero.get_ship().get_hold()[item], True)
            hero.get_ship().hold_upgraide(item, add=False)
        else:
            self.bying()

    def bying(self):
        rect_width = 0
        rect_x = WIDTH * 0.37
        rect_y = HEIGHT * 0.437
        square_wx, square_wy = 15, 30
        rect_color = pygame.Color('green')
        rect_rect = ((rect_x, rect_y), (square_wx, square_wy))
        x1 = x2 = y1 = y2 = 0

        while True:
            pygame.draw.rect(screen, pygame.Color('#04859D'),
                             (WIDTH * 0.3, HEIGHT * 0.4, WIDTH * 0.4, HEIGHT * 0.1),
                             border_radius=30)
            pygame.draw.rect(screen, pygame.Color('#C8DFE3'),
                             (WIDTH * 0.305, HEIGHT * 0.41, WIDTH * 0.39, HEIGHT * 0.081),
                             border_radius=30)
            pygame.draw.rect(screen, pygame.Color('#333333'),
                             (WIDTH * 0.305, HEIGHT * 0.41, WIDTH * 0.39, HEIGHT * 0.081), 3,
                             border_radius=30)
            pygame.draw.rect(screen, pygame.Color('gray'),
                             (WIDTH * 0.37, HEIGHT * 0.44, WIDTH * 0.2, HEIGHT * 0.02),
                             border_radius=5)
            space = load_image('cube.png', (20, 20))
            money = load_image('money.png', (20, 20))
            plus = load_image('plus.png', (20, 20))
            minus = load_image('minus.png', (20, 20))
            screen.blit(space, (WIDTH * 0.31, HEIGHT * 0.44))
            screen.blit(money, (WIDTH * 0.585, HEIGHT * 0.44))
            screen.blit(minus, (WIDTH * 0.355, HEIGHT * 0.44))
            screen.blit(plus, (WIDTH * 0.573, HEIGHT * 0.44))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x1, y1 = event.pos
                    if 0 <= y1 <= 300:
                        if (x1 < rect_x) or (x1 > rect_x + square_wx) or (y1 < rect_y) or \
                                (y1 > rect_y + square_wy):
                            x1 = y1 = 0
                if event.type == pygame.MOUSEBUTTONUP:
                    rect_x += x2
                    x1 = x2 = y1 = y2 = 0
                if event.type == pygame.MOUSEMOTION and x1 > 0:
                    pos = event.pos
                    if WIDTH * 0.37 <= pos[0] <= WIDTH * 0.57:
                        x2 = event.pos[0] - x1

            rect_rect = ((rect_x + x2, rect_y + y2), (square_wx, square_wy))
            pygame.draw.rect(screen, rect_color, rect_rect, rect_width)
            pygame.display.flip()
            clock.tick(60)


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
                                start_game()
                                return
                            elif HEIGHT * 0.3 + self.buttons.height + 15 <= pos[1] \
                                    <= HEIGHT * 0.3 + 2 * self.buttons.height + 15:
                                tuition()
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
                                LANGUAGE = 'ko'
                                self.update_window()
                            elif HEIGHT * 0.3 + 2 * self.buttons.height + 30 <= pos[1] \
                                    <= HEIGHT * 0.3 + 3 * self.buttons.height + 30:
                                LANGUAGE = 'en'
                                self.update_window()
                            elif HEIGHT * 0.3 + 3 * self.buttons.height + 45 <= pos[1] \
                                    <= HEIGHT * 0.3 + 4 * self.buttons.height + 45:
                                LANGUAGE = 'ru'
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

        self.input_name()

        self.bg = pygame.transform.scale(load_image('ent_bg.png'), SIZE)
        font = pygame.font.SysFont('Arialms', 40)

        def print_text(y):
            with open(f'data/ENT {LANGUAGE}.txt', 'r', encoding='utf-8') as f:
                self.buttons = map(lambda x: x.rstrip(), f.readlines())

            self.text_coord = y
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

        y = HEIGHT
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    return
            clock.tick(FPS)
            screen.blit(self.bg, (0, 0))
            print_text(y)
            if y >= HEIGHT * 0.1:
                y -= 1
            else:
                if LANGUAGE == 'ko':
                    screen.blit(font.render('지침', True, pygame.Color('white')),
                                (WIDTH * 0.5, HEIGHT * 0.9))
                elif LANGUAGE == 'en':
                    screen.blit(font.render('Please, press "Space" to start the game!', True,
                                            pygame.Color('white')), (WIDTH * 0.3, HEIGHT * 0.9))
                else:
                    screen.blit(font.render('Пожалуйста, нажмите "Пробел", чтобы начать игру!', True,
                                            pygame.Color('white')), (WIDTH * 0.25, HEIGHT * 0.9))
            pygame.display.flip()

    def input_name(self):
        global LANGUAGE, FPS, WIDTH, HEIGHT, name
        self.bg = pygame.transform.scale(load_image('ent_bg.png'), SIZE)
        timer = 0
        font = pygame.font.SysFont('Arialms', 40)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    elif event.key == pygame.K_KP_ENTER:
                        if name:
                            return
                    elif len(name) < 10:
                        name += event.unicode
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and name:
                    pos = event.pos
                    if HEIGHT * 0.43 <= pos[1] <= HEIGHT * 0.47 and \
                            WIDTH * 0.54 <= pos[0] <= WIDTH * 0.64:
                        return

            clock.tick(FPS)
            timer = (timer + 1) % FPS
            screen.blit(self.bg, (0, 0))
            pygame.draw.rect(screen, pygame.Color('#04859D'),
                             (WIDTH * 0.3, HEIGHT * 0.4, WIDTH * 0.4, HEIGHT * 0.1),
                             border_radius=30)
            pygame.draw.rect(screen, pygame.Color('#C8DFE3'),
                             (WIDTH * 0.305, HEIGHT * 0.41, WIDTH * 0.39, HEIGHT * 0.081),
                             border_radius=30)
            pygame.draw.rect(screen, pygame.Color('#333333'),
                             (WIDTH * 0.305, HEIGHT * 0.41, WIDTH * 0.39, HEIGHT * 0.081), 3,
                             border_radius=30)
            pygame.draw.rect(screen, pygame.Color('white'),
                             (WIDTH * 0.34, HEIGHT * 0.43, WIDTH * 0.2, HEIGHT * 0.04),
                             border_top_left_radius=5, border_bottom_left_radius=5)
            pygame.draw.rect(screen, pygame.Color('#04859D'),
                             (WIDTH * 0.54, HEIGHT * 0.43, WIDTH * 0.1, HEIGHT * 0.04),
                             border_top_right_radius=5, border_bottom_right_radius=5)
            pygame.draw.rect(screen, pygame.Color('#333333'),
                             (WIDTH * 0.34, HEIGHT * 0.43, WIDTH * 0.2, HEIGHT * 0.04), 2,
                             border_top_left_radius=5, border_bottom_left_radius=5)

            input_label = font.render(name, True, pygame.Color('#333333'))
            screen.blit(input_label, (WIDTH * 0.344, HEIGHT * 0.42))
            cursor_pos = input_label.get_width()

            if 0 <= timer <= 29:
                pygame.draw.line(screen, pygame.Color('#333333'),
                                 (WIDTH * 0.344 + cursor_pos, HEIGHT * 0.436),
                                 (WIDTH * 0.344 + cursor_pos, HEIGHT * 0.462), 2)

            if LANGUAGE == 'ko':
                screen.blit(font.render('확인', True, pygame.Color('white')),
                            (WIDTH * 0.567, HEIGHT * 0.424))
            elif LANGUAGE == 'en':
                screen.blit(font.render('Ok', True,
                                        pygame.Color('white')), (WIDTH * 0.575, HEIGHT * 0.424))
            else:
                screen.blit(font.render('Готово', True,
                                        pygame.Color('white')), (WIDTH * 0.555, HEIGHT * 0.424))

            pygame.display.flip()


def game_over():
    global LANGUAGE, SIZE
    font = pygame.font.SysFont('Arialms', 40)
    death_screen = pygame.transform.scale(load_image('death.png'), SIZE)
    screen.blit(death_screen, (0, 0))
    with open(f'data/Game_over {LANGUAGE}.txt', 'r', encoding='utf-8') as f:
        text = map(lambda x: x.rstrip(), f.readlines())

    text_coord = HEIGHT * 0.3
    for line in text:
        string_rendered = font.render(line, True, pygame.Color('white'))
        text = string_rendered.get_rect()
        text_coord += 10
        text.top = text_coord
        text.x = WIDTH * 0.3
        text_coord += text.height
        screen.blit(string_rendered, text)

    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()


def win():
    bg = pygame.transform.scale(load_image('jump.png'), SIZE)
    font = pygame.font.SysFont('Arialms', 40)

    def print_text(y):
        with open(f'data/win {LANGUAGE}.txt', 'r', encoding='utf-8') as f:
            buttons = map(lambda x: x.rstrip(), f.readlines())

        text_coord = y
        button = 1
        for line in buttons:
            string_rendered = font.render(line, True, pygame.Color('white'))
            buttons = string_rendered.get_rect()
            text_coord += 10
            buttons.top = text_coord
            buttons.x = 30
            text_coord += buttons.height
            screen.blit(string_rendered, buttons)
            button += 1

    y = HEIGHT
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                a = Lobby()
        clock.tick(FPS)
        screen.blit(bg, (0, 0))
        print_text(y)
        if y >= HEIGHT * 0.2:
            y -= 1
        pygame.display.flip()


def writing_record(win_='No'):
    con = sqlite3.connect('data/scores.db')
    cursor = con.cursor()
    cursor.execute(
        f'INSERT INTO Score(name, score, win) VALUES("{hero.name}", {hero.score}, "{win_}")')
    con.commit()


def mini_map():
    minimap.fill((0, 0, 0))
    minimap_ship_coord = hero.ship.coord[0] // res + 200, hero.ship.coord[1] // res + 200
    minimap_objects.update(coord=minimap_ship_coord)
    minimap_objects.draw(minimap)
    screen.blit(minimap, (WIDTH - res * 2 - 10, 10))
    pygame.draw.rect(screen, pygame.Color('#04859D'), (WIDTH - res * 2 - 20, 0, res * 2 + 20,
                                                       res * 2 + 20), 4)


def render_hp():
    for ship in ships:
        if ship == hero.ship:
            hp = font.render(str(int(hero.ship.hull)), True, pygame.Color('blue'))
            screen.blit(hp, (20, 40))
        else:
            hp = font.render(str(int(ship.hull)), True, pygame.Color('blue'))
            screen.blit(hp, (ship.rect.x + ship.size[0] // 2 - 35, ship.rect.y + ship.size[1] - 20))


def tuition():
    start_game(True)
    tuition_kristalid = Ships.Kristalid(load_image('Kristalid_ship.png', (150, 150), -1),
                                        [-camera.dx, 0], 1, 0, [Equipments.Engine(0)], hero,
                                        all_sprites, ships, enemy)
    tuition_running = True
    while tuition_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_a or event.key == pygame.K_s or \
                        event.key == pygame.K_d:
                    hero.ship.update(event, 'fly')
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                hero.ship.update(event, 'shoot')
        screen.fill((0, 0, 0))
        all_sprites.update(hero_coord=[hero.ship.rect.x + hero.ship.size[0] // 2, hero.ship.rect.y +
                                       hero.ship.size[1] // 2])
        for sprite in all_sprites:
            if sprite != hero.ship:
                camera.apply(sprite)
        camera.stop_move()
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


# PG
FPS = 60
LANGUAGE = 'en'
AU = 815
pygame.init()
user32 = ctypes.windll.user32
SIZE = WIDTH, HEIGHT = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()
song = pygame.mixer.Sound('soundtracks/space_theme.mp3')
star_damage_time = 0
kristalids = list()
font = pygame.font.SysFont('Arialms', 60)
res = 50


def start_game(tui=False):
    global all_sprites, planets, ships, station, enemy, hero_group, minimap_objects, camera, bg, sun,\
        mercury, earth, mars, jupiter, saturn, uranus, neptune, station, hero, minimap, \
        sun_minimap, mercury_minimap, venus_minimap, earth_minimap, mars_minimap, jupiter_minimap, \
        saturn_minimap, uranus_minimap, neptune_minimap, ship_minimap, star_damage_time, kristalids, \
        station_minimap, h
    star_damage_time = 0
    kristalids = list()
    # Группы спрайтов
    all_sprites = pygame.sprite.Group()
    planets = pygame.sprite.Group()
    ships = pygame.sprite.Group()
    stations = pygame.sprite.Group()
    enemy = pygame.sprite.Group()
    hero_group = pygame.sprite.Group()
    minimap_objects = pygame.sprite.Group()
    camera = Camera()
    # Объекты
    bg = pygame.sprite.Sprite()
    bg.image = pygame.transform.scale(load_image('Space Background.png'), (10000, 10000))
    bg.rect = bg.image.get_rect()
    all_sprites.add(bg)
    bg.rect.x = bg.rect.x = -5000 + WIDTH // 2
    bg.rect.y = -5000 + HEIGHT // 2

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
    if not tui:
        jupiter = Objects.Planet(load_image('Jupiter.png'), 50, 5, [400, 400],
                                 [WIDTH // 2, HEIGHT // 2],
                                 AU * 5.2 + 750, 100, radians(randrange(0, 360)), all_sprites,
                                 planets)
        saturn = Objects.Planet(load_image('Saturn.png'), 25, 10, [800, 800],
                                [WIDTH // 2, HEIGHT // 2],
                                AU * 8.2, 100, radians(randrange(0, 360)), all_sprites, planets)
        uranus = Objects.Planet(load_image('Uranus.png'), 50, 5, [220, 220],
                                [WIDTH // 2, HEIGHT // 2],
                                AU * 9 + 750, 100, radians(randrange(0, 360)), all_sprites, planets)
        neptune = Objects.Planet(load_image('Neptune.png'), 50, 5, [200, 200],
                                 [WIDTH // 2, HEIGHT // 2],
                                 AU * 11 + 750, 100, radians(randrange(0, 360)), all_sprites,
                                 planets)
        station = Objects.Station(load_image('Station.png', color_key=-1), 1, 1, [760, 525],
                                  [AU * 5.2 + 750, HEIGHT // 2], all_sprites, stations)
    image = (
        load_image('Nomad_ship_fly.png', (64, 64)), load_image('Nomad_ship_stop.png', (64, 64)))
    hero_images = (image[0], pygame.transform.rotate(image[0], 45),
                   pygame.transform.rotate(image[0], 90),
                   pygame.transform.rotate(image[0], 135),
                   pygame.transform.rotate(image[0], 180),
                   pygame.transform.rotate(image[0], 225),
                   pygame.transform.rotate(image[0], 270),
                   pygame.transform.rotate(image[0], 315),
                   image[1], pygame.transform.rotate(image[1], 45),
                   pygame.transform.rotate(image[1], 90),
                   pygame.transform.rotate(image[1], 135),
                   pygame.transform.rotate(image[1], 180),
                   pygame.transform.rotate(image[1], 225),
                   pygame.transform.rotate(image[1], 270),
                   pygame.transform.rotate(image[1], 315))
    if tui:
        hero = Hero.Hero(
            Ships.NomadShip(hero_images, [-camera.dx, 0],
                            500, 0, [Equipments.Destructor(3, (enemy, all_sprites),
                                                          load_image('destructor_bullet.png',
                                                                     (50, 40))),
                                     Equipments.Engine(2), Equipments.FuelTank(0),
                                     Equipments.Grab(0),
                                     Equipments.Shield()],
                            camera,
                            SIZE, all_sprites, ships, hero_group), 1000000, name)
    if not tui:
        # Объекты мини карты
        hero = Hero.Hero(
            Ships.NomadShip(hero_images, [-camera.dx, 0],
                            500, 0, [Equipments.PhotonGun(0, (enemy, all_sprites),
                                                          load_image('photon_bullet.png', (50, 50))),
                                     Equipments.Engine(0), Equipments.FuelTank(0),
                                     Equipments.Grab(0),
                                     Equipments.Shield()],
                            camera,
                            SIZE, all_sprites, ships, hero_group), 1000000, name)
        minimap = pygame.Surface((10000 / (res / 2), 10000 / (res / 2)))
        h = (10000 / (res / 2)) / 2
        sun_minimap = Objects.MiniMapStar(load_image('Sun.png'), 25, 10, [1500 / res, 1500 / res],
                                          [h, h],
                                          minimap_objects)
        mercury_minimap = Objects.MiniMapPlanet(load_image('Mercury.png'), 50, 5,
                                                [80 / (res / 2) + 2, 80 / (res / 2) + 2], [h, h],
                                                (AU * 0.387 + 750) / res, 100 / res, mercury.grad,
                                                minimap_objects)
        venus_minimap = Objects.MiniMapPlanet(load_image('Venus.png'), 50, 5,
                                              [260 / (res / 2), 260 / (res / 2)], [h, h],
                                              (AU * 0.9 + 750) / res, 100 / res, venus.grad,
                                              minimap_objects)
        earth_minimap = Objects.MiniMapPlanet(load_image('Earth.png'), 50, 5,
                                              [280 / (res / 2), 280 / (res / 2)], [h, h],
                                              (AU * 1.7 + 750) / res, 100 / res, 0, minimap_objects)
        mars_minimap = Objects.MiniMapPlanet(load_image('Mars.png'), 50, 5,
                                             [170 / (res / 2), 170 / (res / 2)], [h, h],
                                             (AU * 2.5 + 750) / res, 100 / res, mars.grad,
                                             minimap_objects)
        jupiter_minimap = Objects.MiniMapPlanet(load_image('Jupiter.png'), 50, 5,
                                                [400 / (res / 2), 400 / (res / 2)], [h, h],
                                                (AU * 5.2 + 750) / res, 100 / res, jupiter.grad,
                                                minimap_objects)
        saturn_minimap = Objects.MiniMapPlanet(load_image('Saturn.png'), 25, 10,
                                               [800 / (res / 2), 800 / (res / 2)], [h, h],
                                               AU * 8.2 / res, 100 / res, saturn.grad,
                                               minimap_objects)
        uranus_minimap = Objects.MiniMapPlanet(load_image('Uranus.png'), 50, 5,
                                               [220 / (res / 2), 220 / (res / 2)], [h, h],
                                               (AU * 9 + 750) / res, 100 / res, uranus.grad,
                                               minimap_objects)
        neptune_minimap = Objects.MiniMapPlanet(load_image('Neptune.png'), 50, 5,
                                                [200 / (res / 2), 200 / (res / 2)], [h, h],
                                                (AU * 11 + 750) / res, 100 / res, neptune.grad,
                                                minimap_objects)
        station_minimap = Objects.MiniMapStation(load_image('Station.png', color_key=-1), 1, 1,
                                                 [760 / res, 525 / res],
                                                 [(AU * 5.2 + 750) / res + 175, h],
                                                 minimap_objects)
        minimap_ship_coord = hero.ship.coord[0] // 25 + h, hero.ship.coord[1] // 25 + h
        ship_minimap = Objects.MiniMapShip(image[0], (10, 10), minimap_ship_coord, minimap_objects)


# lobby
name = ''
lobby = Lobby()
landing = Landing()

# main cycle
running = True
song_p = True
while running:
    while len(kristalids) != 30:
        spawn_coord = [randrange(-9700, 9700), randrange(-9700, 9700)]
        if (spawn_coord[0] >= AU * 2.5 + 750 or spawn_coord[0] <= -(AU * 2.5 + 750)) and (
                spawn_coord[1] >= AU * 2.5 + 750 or spawn_coord[1] <= -(AU * 2.5 + 750)):
            kristalids.append(Ships.Kristalid(load_image('Kristalid_ship.png', (150, 150), -1),
                                              spawn_coord,
                                              500, 0, [
                                                  Equipments.Destructor(1, (hero_group, all_sprites),
                                                                        load_image(
                                                                            'destructor_bullet.png',
                                                                            (50, 40), -1)),
                                              Equipments.Engine(0)],
                                              hero, all_sprites, ships, enemy))
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
            elif hero.ship.end_jump and \
                    (event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT):
                win()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            hero.ship.update(event, 'shoot')
    screen.fill((0, 0, 0))
    if hero.ship.death_flag:
        game_over()
    all_sprites.update(hero_coord=[hero.ship.rect.x + hero.ship.size[0] // 2, hero.ship.rect.y +
                                   hero.ship.size[1] // 2])
    for sprite in all_sprites:
        if sprite != hero.ship:
            camera.apply(sprite)
    if star_damage_time == 0 and pygame.sprite.collide_mask(sun, hero.ship):
        hero.ship.get_damage(sun.get_damage())
    star_damage_time = (star_damage_time + 1) % FPS
    if song_p:
        song.play()
        song_p = False
    camera.stop_move()
    all_sprites.draw(screen)
    landing.planet_collide()
    render_hp()
    if hero.ship.end_jump:
        text = font.render(str('Вы можете совершить прыжок!(Нажмите "Shift")'),
                           True, pygame.Color('blue'))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 10 + text.get_height()))
    mini_map()
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
