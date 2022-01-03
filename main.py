import ctypes
import sys
import Ships
import Objects
import os
import pygame


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


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


class Lobby:
    def __init__(self):
        self.buttons_type = 'Main Menu'
        self.bg = pygame.transform.scale(load_image('lobby_bg.png'), SIZE)
        screen.blit(self.bg, (0, 0))

        self.font = pygame.font.SysFont('Arialms', 50)
        self.update_buttons()
        self.cycle()

    def cycle(self):
        global FPS, LANGUAGE
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = event.pos
                    if 200 >= pos[0] >= 30:
                        if self.buttons_type == 'Main Menu':
                            if HEIGHT * 0.3 <= pos[1] <= HEIGHT * 0.3 + self.buttons.height:
                                return  # start new game
                            elif HEIGHT * 0.3 + self.buttons.height + 15 <= pos[1] \
                                    <= HEIGHT * 0.3 + 2 * self.buttons.height + 15:
                                return  # continue last save
                            elif HEIGHT * 0.3 + 2 * self.buttons.height + 30 <= pos[1] \
                                    <= HEIGHT * 0.3 + 3 * self.buttons.height + 30:
                                self.buttons_type = 'Options'
                                self.update_buttons()
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
                                self.update_buttons()
                            elif HEIGHT * 0.3 + 2 * self.buttons.height + 30 <= pos[1] \
                                    <= HEIGHT * 0.3 + 3 * self.buttons.height + 30:
                                LANGUAGE = 'EN'
                                self.update_buttons()
                            elif HEIGHT * 0.3 + 3 * self.buttons.height + 45 <= pos[1] \
                                    <= HEIGHT * 0.3 + 4 * self.buttons.height + 45:
                                LANGUAGE = 'RU'
                                self.update_buttons()
                            elif HEIGHT * 0.3 + 4 * self.buttons.height + 60 <= pos[1] \
                                    <= HEIGHT * 0.3 + 5 * self.buttons.height + 60:
                                self.buttons_type = 'Main Menu'
                                self.update_buttons()

            pygame.display.flip()
            clock.tick(FPS)

    def update_buttons(self):
        global LANGUAGE
        screen.fill((0, 0, 0))
        screen.blit(self.bg, (0, 0))

        with open(f'data/{self.buttons_type} {LANGUAGE}.txt', 'r', encoding='utf-8') as f:
            self.buttons = map(lambda x: x.rstrip(), f.readlines())

        self.text_coord = HEIGHT * 0.3
        for line in self.buttons:
            string_rendered = self.font.render(line, 1, pygame.Color('white'))
            self.buttons = string_rendered.get_rect()
            self.text_coord += 10
            self.buttons.top = self.text_coord
            self.buttons.x = 30
            self.text_coord += self.buttons.height
            screen.blit(string_rendered, self.buttons)

    def quit(self):
        pygame.quit()
        sys.exit()


# PG
FPS = 60
LANGUAGE = 'EN'
pygame.init()
user32 = ctypes.windll.user32
SIZE = WIDTH, HEIGHT = user32.GetSystemMetrics(0) - 100, user32.GetSystemMetrics(1) - 100
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

# lobby
lobby = Lobby()

# Группы спрайтов
all_sprites = pygame.sprite.Group()
planets = pygame.sprite.Group()
ships = pygame.sprite.Group()
camera = Camera()

# Объекты
sun = Objects.Star(load_image('Sun.png'), 25, 10, [400, 400], [WIDTH // 2, HEIGHT // 2],
                   all_sprites)
mercury = Objects.Planet(load_image('Mercury.png'), 50, 5, [100, 100], [WIDTH // 2, HEIGHT // 2],
                         250, 100, all_sprites)
venus = Objects.Planet(load_image('Venus.png'), 50, 5, [150, 150], [WIDTH // 2, HEIGHT // 2],
                       400, 100, all_sprites)
earth = Objects.Planet(load_image('Earth.png'), 50, 5, [200, 200], [WIDTH // 2, HEIGHT // 2], 600,
                       100, all_sprites)
mars = Objects.Planet(load_image('Mars.png'), 50, 5, [150, 150], [WIDTH // 2, HEIGHT // 2], 800,
                      100, all_sprites)
jupiter = Objects.Planet(load_image('Jupiter.png'), 50, 5, [200, 200], [WIDTH // 2, HEIGHT // 2],
                         1200, 100, all_sprites)
saturn = Objects.Planet(load_image('Saturn.png'), 21, 12, [200, 200], [WIDTH // 2, HEIGHT // 2],
                        1600, 100, all_sprites)
uranus = Objects.Planet(load_image('Uranus.png'), 50, 5, [200, 200], [WIDTH // 2, HEIGHT // 2], 2000,
                        100, all_sprites)
neptune = Objects.Planet(load_image('Neptune.png'), 50, 5, [200, 200], [WIDTH // 2, HEIGHT // 2],
                         2400, 100, all_sprites)

hero_ship = Ships.Ship(load_image('hero_ship.png', (50, 50)), [WIDTH // 2, HEIGHT // 2], 100, 100,
                       None, all_sprites)

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
    screen.fill((0, 0, 0))
    all_sprites.update()
    #     camera.update(hero_ship)
    #     for sprite in all_sprites:
    #         camera.apply(sprite)
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
