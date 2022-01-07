import ctypes
import sys
import Ships
import Objects
import os
import pygame


class Camera:
    def __init__(self):
        self.dx = - (AU * 1.7 + 750)
        self.dy = 0

    def apply(self, obj):
        if str(obj) == 'Планета':
            obj.center[0] = sun.rect.x + sun.size[0] // 2
            obj.center[1] = sun.rect.y + sun.size[1] // 2
        if sprite == bg:
            if self.dx < 0:
                obj.rect.x += -((-self.dx) // 2)
            else:
                obj.rect.x += self.dx // 2
            if self.dy < 0:
                obj.rect.y += -((-self.dy) // 2)
            else:
                obj.rect.y += self.dy // 2
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
    global WIDTH, HEIGHT, FPS, LANGUAGE

    def __init__(self):
        self.current_window = self.current_bg = 'government'
        self.font = pygame.font.SysFont('Arialms', 30)
        self.text = self.font.render('Press "Space" to land', True, pygame.Color('Yellow'))
        self.planet = None

        #  with open(f'Icon_names {LANGUAGE}', 'r', encoding='utf-8') as f:
        #      pass

    def planet_collide(self):
        for sprite in planets:
            if pygame.sprite.collide_mask(hero_ship, sprite):
                screen.blit(self.text, (WIDTH // 2 - 150, HEIGHT // 2 + 20))
                return sprite

    def cycle(self, planet):
        self.planet = planet
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # button push
                    pos = event.pos
                    if HEIGHT - 100 <= pos[1] <= HEIGHT:
                        if WIDTH * 0.5 - 200 <= pos[0] <= WIDTH * 0.5 - 100:
                            self.current_window = self.current_bg = 'government'
                        elif WIDTH * 0.5 - 100 <= pos[0] <= WIDTH * 0.5:
                            self.current_window = 'shop'
                            self.current_bg = 'planet_bg'
                        elif WIDTH * 0.5 <= pos[0] <= WIDTH * 0.5 + 100:
                            self.current_window = 'market'
                            self.current_bg = 'planet_bg'
                        elif WIDTH * 0.5 + 100 <= pos[0] <= WIDTH * 0.5 + 200:
                            self.current_window = self.current_bg = 'planet_bg'
                            return  # undocking

            self.update_window()
            pygame.display.flip()
            clock.tick(FPS)

    def update_window(self):
        bg = pygame.transform.scale(load_image(self.current_bg + '.png'), SIZE)
        screen.blit(bg, (0, 0))

        # buttons
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

        if self.current_window != 'planet_bg':
            eval('self.' + self.current_window + '()')

    def government(self):
        with open(f'data/Dialog planets {LANGUAGE}.txt') as f:
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

    def market(self):
        font = pygame.font.SysFont('Arialms', 30)
        pygame.draw.rect(screen, pygame.Color('#04859D'),
                         (WIDTH * 0.28, HEIGHT * 0.15, WIDTH * 0.44, HEIGHT * 0.69),
                         border_radius=30)
        pygame.draw.rect(screen, pygame.Color('#C8DFE3'),
                         (WIDTH * 0.29, HEIGHT * 0.17, WIDTH * 0.42, HEIGHT * 0.65),
                         border_radius=30)
        pygame.draw.rect(screen, pygame.Color('#333333'),
                         (WIDTH * 0.2901, HEIGHT * 0.1701, WIDTH * 0.42, HEIGHT * 0.65), 3,
                         border_radius=30)

        #  icons and prices
        y_position = HEIGHT * 0.25
        products = self.planet.products()
        for product in products:
            product_icon = pygame.transform.scale(load_image(product + '_icon.png'),
                                                  (WIDTH * 0.032, WIDTH * 0.032))
            screen.blit(product_icon, (WIDTH * 0.31, y_position))

            x_position = WIDTH * 0.43
            flag = True
            for price in products[product]:
                string_rendered = font.render(str(price), True, pygame.Color('black'))
                if flag:
                    string_len = string_rendered.get_width()
                    flag = False
                screen.blit(string_rendered, (x_position, y_position))
                x_position += WIDTH * 0.04 + string_len

            y_position += WIDTH * 0.05

        with open(f'data/market {LANGUAGE}.txt', 'r', encoding='utf-8') as f:
            text = map(lambda x: x.rstrip(), f.readlines())

        x_position = WIDTH * 0.4
        a = 1
        for word in text:
            string_rendered = font.render(word, True, pygame.Color('black'))
            screen.blit(string_rendered, (x_position, HEIGHT * 0.2))
            if a == 2:
                space = font.render('buy', True, pygame.Color('black'))
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
                    self.quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    return
            pygame.display.flip()
            clock.tick(FPS)


# PG
FPS = 60
LANGUAGE = 'EN'
AU = 815
pygame.init()
user32 = ctypes.windll.user32
SIZE = WIDTH, HEIGHT = user32.GetSystemMetrics(0) - 100, user32.GetSystemMetrics(1) - 100
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

# lobby
lobby = Lobby()
lobby = None
landing = Landing()

# Группы спрайтов
all_sprites = pygame.sprite.Group()
planets = pygame.sprite.Group()
ships = pygame.sprite.Group()
background = pygame.sprite.Group()
camera = Camera()

# Объекты
bg = pygame.sprite.Sprite()
bg.image = pygame.transform.scale(load_image('Space Background.png'), (9000, 9000))
bg.rect = bg.image.get_rect()
all_sprites.add(bg)
bg.rect.x = -4500 + (AU * 1.7 + 750) // 2
bg.rect.y = -4500

sun = Objects.Star(load_image('Sun.png'), 25, 10, [1500, 1500], [WIDTH // 2, HEIGHT // 2],
                   all_sprites)
mercury = Objects.Planet(load_image('Mercury.png'), 50, 5, [80, 80], [WIDTH // 2, HEIGHT // 2],
                         AU * 0.387 + 750, 100, all_sprites, planets)
venus = Objects.Planet(load_image('Venus.png'), 50, 5, [260, 260], [WIDTH // 2, HEIGHT // 2],
                       AU * 0.9 + 750, 100, all_sprites, planets)
earth = Objects.Planet(load_image('Earth.png'), 50, 5, [280, 280], [WIDTH // 2, HEIGHT // 2],
                       AU * 1.7 + 750, 100, all_sprites, planets)
mars = Objects.Planet(load_image('Mars.png'), 50, 5, [170, 170], [WIDTH // 2, HEIGHT // 2],
                      AU * 2.5 + 750, 100, all_sprites, planets)
jupiter = Objects.Planet(load_image('Jupiter.png'), 50, 5, [400, 400], [WIDTH // 2, HEIGHT // 2],
                         AU * 5.2 + 750, 100, all_sprites, planets)
saturn = Objects.Planet(load_image('Saturn.png'), 25, 10, [800, 800], [WIDTH // 2, HEIGHT // 2],
                        AU * 8.2, 100, all_sprites, planets)
uranus = Objects.Planet(load_image('Uranus.png'), 50, 5, [220, 220], [WIDTH // 2, HEIGHT // 2],
                        AU * 9 + 750, 100, all_sprites, planets)
neptune = Objects.Planet(load_image('Neptune.png'), 50, 5, [200, 200], [WIDTH // 2, HEIGHT // 2],
                         AU * 11 + 750, 100, all_sprites, planets)

hero_ship = Ships.Ship(load_image('hero_ship.png', (50, 50)), [WIDTH // 2, HEIGHT // 2], 100, 100,
                       None, camera, all_sprites)

# main cycle
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            if event.key == pygame.K_w or event.key == pygame.K_a or event.key == pygame.K_s or \
                    event.key == pygame.K_d:
                hero_ship.update(event, 'fly')
            elif landing.planet_collide() and event.key == pygame.K_SPACE:
                hero_ship.keys.clear()
                landing.cycle(landing.planet_collide())
    screen.fill((0, 0, 0))
    all_sprites.update()
    for sprite in all_sprites:
        if sprite != hero_ship:
            camera.apply(sprite)
    camera.stop_move()
    all_sprites.draw(screen)
    landing.planet_collide()
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
