import pygame
import math

fps = 60


class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, coord, owner, target_coord, speed, maximum, damage, enemy, *group):
        super().__init__(*group)
        self.maximum = maximum
        self.speed = speed
        self.start_point = coord
        self.owner = owner
        self.damage = damage
        self.image = image
        self.enemy = enemy
        self.rect = self.image.get_rect()
        self.rect.x = coord[0]
        self.rect.y = coord[1]
        self.mask = pygame.mask.from_surface(self.image)
        if target_coord[0] - self.start_point[0] == 0:
            self.null = True
        else:
            self.null = False
            self.angle = math.atan((target_coord[1] - self.start_point[1]) /
                                   (target_coord[0] - self.start_point[0]))
        self.d = 0
        if target_coord[0] < self.start_point[0]:
            self.minus = True
        else:
            self.minus = False

    def update(self, **kwargs):
        if self.minus:
            self.d -= self.speed / fps
        else:
            self.d += self.speed / fps
        if self.null:
            self.rect.center = round(self.start_point[0]), round(self.d) + self.start_point[1]
        else:
            self.rect.center = round(self.d * math.cos(self.angle)) + self.start_point[0], \
                               round(self.d * math.sin(self.angle)) + self.start_point[1]
        if self.d > self.maximum or self.d < -self.maximum:
            self.kill()
        for sprite in self.enemy:
            if pygame.sprite.collide_mask(self, sprite):
                self.kill()
                sprite.kill()

    def __str__(self):
        return 'Пуля'
