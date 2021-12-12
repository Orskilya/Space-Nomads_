import pygame
import os
from classes.ship import Ship


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


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


if __name__ == '__main__':
    fps = 60

    # Pygame
    pygame.init()
    size = width, height = 1024, 1024
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()

    # Variables
    move = [0, 0]
    running = True

    # Sprites
    # Groups
    all_sprites = pygame.sprite.Group()
    planets = pygame.sprite.Group()
    ships = pygame.sprite.Group()
    # Images
    player_sprite = pygame.sprite.Sprite()
    player_sprite.image = load_image('player_ship.jpg', color_key='white')
    player_sprite.rect = player_sprite.image.get_rect()
    all_sprites.add(player_sprite)
    ships.add(player_sprite)
    player_sprite.rect.x = 10
    player_sprite.rect.y = 10

    sun_sprite = pygame.sprite.Sprite()
    sun_sprite.image = load_image('Sun.png', (400, 400))
    sun_sprite.rect = sun_sprite.image.get_rect()
    all_sprites.add(sun_sprite)
    planets.add(sun_sprite)
    sun_sprite.rect.x = 250
    sun_sprite.rect.y = 250

    # Classes
    ship = Ship(player_sprite, [100, 100], 200 / fps)

    while running:
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
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
