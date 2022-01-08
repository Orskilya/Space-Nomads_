from math import cos, sin, pi
from random import randrange
import pygame
import math

fps = 60

products = ('product', 'medicine', 'alchogol', 'luxury', 'tech', 'weapon')
equipments = (1,)  # tuple. Add to main code


class Object(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, size, coord, *group):
        super().__init__(*group)
        self.coord = coord  # list
        self.size = size
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.image = pygame.transform.scale(self.image, (self.size[0], self.size[1]))
        self.rect = self.rect.move(coord[0] - self.size[0] // 2, coord[1] - self.size[1] // 2)
        self.mask = pygame.mask.from_surface(self.image)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))


class Planet(Object):
    def __init__(self, sheet, columns, rows, size, coord, radius, speed, grad, *group):
        super().__init__(sheet, columns, rows, size, coord, *group)
        global products, equipments
        self.grad = grad
        self.radius = radius
        self.center = coord.copy()
        self.angular_speed = (speed / self.radius) * (pi / 180)
        self.shop = []  # list
        self.market = {i: [randrange(100, 300), randrange(80, 200), randrange(70, 190)] for i in
                       products}  # name: number, purchase, selling
        self.count = 0
        self.images_speed = 6

    def update(self, **kwargs):
        self.coord[0] = self.center[0] + cos(self.grad) * self.radius - self.size[0] // 2
        self.coord[1] = self.center[1] + sin(self.grad) * self.radius - self.size[1] // 2
        self.rect.x = self.coord[0]
        self.rect.y = self.coord[1]
        self.grad += self.angular_speed
        if self.count == 0:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.image = pygame.transform.scale(self.image, (self.size[0], self.size[1]))
            self.mask = pygame.mask.from_surface(self.image)
        self.count = (self.count + 1) % self.images_speed

    def market_items(self):  # increasing number of the products
        for i in self.market.keys():
            self.market[i][0] += 10

    def products(self):
        return self.market

    def __str__(self):
        return 'Планета'


class Star(Object):
    def __init__(self, sheet, columns, rows, size, coord, *group):
        super().__init__(sheet, columns, rows, size, coord, *group)
        self.damage = 30
        self.count = 0
        self.images_speed = 5

    def get_damage(self):
        return self.damage

    def update(self, **kwargs):
        if self.count == 0:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.image = pygame.transform.scale(self.image, (self.size[0], self.size[1]))
            self.mask = pygame.mask.from_surface(self.image)
        self.count = (self.count + 1) % self.images_speed


class Station(Object):
    def __init__(self, sheet, columns, rows, size, coord, *group):
        super().__init__(sheet, columns, rows, size, coord, *group)
        self.shop = []  # list
        self.market = {i: [randrange(20, 100), randrange(90, 300), randrange(90, 330)] for i in
                       products}  # name: number, purchase, selling

    def __str__(self):
        return 'station'

    def market_items(self):  # increasing number of the products
        for i in self.market.keys():
            self.market[i][0] += 10

    def products(self):
        return self.market


class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, coord, owner, target, speed, maximum, damage, ships, *group):
        super().__init__(*group)
        self.maximum = maximum
        self.speed = speed
        self.start_point = coord
        self.owner = owner
        self.damage = damage
        self.image = image
        self.ships = ships
        self.rect = self.image.get_rect()
        self.rect.x = coord[0]
        self.rect.y = coord[1]
        if target[0] - self.start_point[0] == 0:
            self.null = True
        else:
            self.null = False
            self.angle = math.atan((target[1] - self.start_point[1]) /
                                   (target[0] - self.start_point[0]))
        self.d = 0
        if target[0] < self.start_point[0]:
            self.minus = True
        else:
            self.minus = False

    def update(self, **kwargs):
        if self.minus:
            self.d -= self.speed
        else:
            self.d += self.speed
        if self.null:
            self.rect.center = round(self.start_point[0]), round(self.d / fps) + self.start_point[1]
        else:
            self.rect.center = round(self.d * math.cos(self.angle) / fps) + self.start_point[0], \
                               round(self.d * math.sin(self.angle) / fps) + self.start_point[1]

    def __str__(self):
        return 'Пуля'