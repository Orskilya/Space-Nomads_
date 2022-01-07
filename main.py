import ctypes
import sys
import Ships
import Objects
import os
import pygame
import Equipments


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
    def __init__(self):
        self.font = pygame.font.SysFont('Arialms', 60)
        self.text = self.font.render('Press "Space" to land', 1, pygame.Color('Green'))

    def planet_collide(self):
        for sprites in planets:
            if pygame.sprite.collide_mask(hero_ship, sprites):
                screen.blit(self.text, (30, 40))


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
                    self.quit()
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
                                self.quit()
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

    def quit(self):
        pygame.quit()
        sys.exit()

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
                        AU * 7.2, 100, all_sprites, planets)
uranus = Objects.Planet(load_image('Uranus.png'), 50, 5, [220, 220], [WIDTH // 2, HEIGHT // 2],
                        AU * 8 + 750, 100, all_sprites, planets)
neptune = Objects.Planet(load_image('Neptune.png'), 50, 5, [200, 200], [WIDTH // 2, HEIGHT // 2],
                         AU * 10 + 750, 100, all_sprites, planets)
station = Objects.Station(load_image('Station.png', color_key=-1), 1, 1, [760, 525], [
    AU * 4.2 + 750 + WIDTH // 2, 800], all_sprites)

hero_ship = Ships.NomadShip(load_image('hero_ship.png', (50, 50)), [WIDTH // 2, HEIGHT // 2],
                            100, 100, [Equipments.TestGun(load_image('Bullet.png', (50, 50)),
                                                          (ships, all_sprites), 100, 100)], camera,
                            SIZE, all_sprites, ships)

kristalid_test = Ships.Kristalid(load_image('Kristalid_ship.png', (150, 150), -1),
                                 [0, 0], 100, 100, [], all_sprites, ships)

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
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            hero_ship.update(event, 'shoot')

    screen.fill((0, 0, 0))
    all_sprites.update(hero_coord=[hero_ship.rect.x, hero_ship.rect.y])
    for sprite in all_sprites:
        if sprite != hero_ship:
            camera.apply(sprite)
    camera.stop_move()
    all_sprites.draw(screen)
    landing.planet_collide()
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
