import ctypes
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
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


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


# PG
pygame.init()
user32 = ctypes.windll.user32
size = width, height = user32.GetSystemMetrics(0) - 100, user32.GetSystemMetrics(1) - 100
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

# Группы спрайтов
all_sprites = pygame.sprite.Group()
planets = pygame.sprite.Group()
ships = pygame.sprite.Group()
fps = 60
camera = Camera()

# Объекты
sun = Objects.Star(load_image('Sun.png'), 25, 10, [400, 400], [width // 2, height // 2],
                   all_sprites)
mercury = Objects.Planet(load_image('Mercury.png'), 50, 5, [100, 100], [width // 2, height // 2],
                         250, 100, all_sprites)
venus = Objects.Planet(load_image('Venus.png'), 50, 5, [150, 150], [width // 2, height // 2],
                       400, 100, all_sprites)
earth = Objects.Planet(load_image('Earth.png'), 50, 5, [200, 200], [width // 2, height // 2], 600,
                       100, all_sprites)
mars = Objects.Planet(load_image('Mars.png'), 50, 5, [150, 150], [width // 2, height // 2], 800,
                      100, all_sprites)
jupiter = Objects.Planet(load_image('Jupiter.png'), 50, 5, [200, 200], [width // 2, height // 2],
                         1200, 100, all_sprites)
saturn = Objects.Planet(load_image('Saturn.png'), 21, 12, [200, 200], [width // 2, height // 2],
                        1600, 100, all_sprites)
uranus = Objects.Planet(load_image('Uranus.png'), 50, 5, [200, 200], [width // 2, height // 2], 2000,
                        100, all_sprites)
neptune = Objects.Planet(load_image('Neptune.png'), 50, 5, [200, 200], [width // 2, height // 2],
                         2400, 100, all_sprites)

hero_ship = Ships.Ship(load_image('hero_ship.png', (50, 50)), [width // 2, height // 2], 100, 100,
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
    clock.tick(fps)
pygame.quit()
