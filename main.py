import pygame
import os
from classes.ship import Ship


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    if color_key is not None:
        image = image.convert()
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


if __name__ == '__main__':
    fps = 60
    # Pygame
    pygame.init()
    size = width, height = 1024, 1024
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    ship = Ship(screen, [100, 100], 200 / fps)
    # Variables
    move = [0, 0]
    running = True
    # Sprites
    all_sprites = pygame.sprite.Group()
    # Classes
    ship.render()
    while running:
        ship.move(move[0], move[1])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if int(event.key) == ord('w') and not move[0] == 1:
                    move[0] = -1
                elif int(event.key) == ord('s') and not move[0] == -1:
                    move[0] = 1
                if int(event.key) == ord('a') and not move[1] == 1:
                    move[1] = -1
                elif int(event.key) == ord('d') and not move[1] == -1:
                    move[1] = 1
            elif event.type == pygame.KEYUP:
                if int(event.key) == ord('w'):
                    move[0] = 0
                elif int(event.key) == ord('s'):
                    move[0] = 0
                if int(event.key) == ord('a'):
                    move[1] = 0
                elif int(event.key) == ord('d'):
                    move[1] = 0
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()
