import pygame
import Ships
import os
import pygame


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
size = width, height = 1024, 1024
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
# Группы спрайтов
all_sprites = pygame.sprite.Group()
planets = pygame.sprite.Group()
ships = pygame.sprite.Group()
fps = 60
# Объекты
hero_ship = Ships.Ship(load_image('hero_ship.png', (150, 150)), [0, 0], 100, 100, None,
                       all_sprites)
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
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(fps)
pygame.quit()
